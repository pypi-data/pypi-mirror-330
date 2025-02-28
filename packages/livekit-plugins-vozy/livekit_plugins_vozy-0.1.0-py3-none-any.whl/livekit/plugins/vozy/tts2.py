from __future__ import annotations

import asyncio
import dataclasses
import json
from dataclasses import dataclass
from typing import Any, List

import aiohttp
from livekit import rtc
from livekit.agents import (
    DEFAULT_API_CONNECT_OPTIONS,
    APIConnectionError,
    APIConnectOptions,
    APIStatusError,
    APITimeoutError,
    tokenize,
    tts,
    utils,
)

from .log import logger

@dataclass
class VoiceSettings:
    speed: float  # Ajusta según los parámetros que acepta Vozy
    pitch: float
    volume: float

@dataclass
class Voice:
    id: str
    name: str
    language: str
    settings: VoiceSettings | None = None

class TTS(tts.TTS):
    def __init__(
        self,
        *,
        api_key: str,
        voice: Voice,
        base_url: str = "wss://api.vozy.com/v1/tts/ws",  # Ajusta según la URL real de Vozy
        sample_rate: int = 24000,  # Ajusta según lo que soporte Vozy
        word_tokenizer: tokenize.WordTokenizer = tokenize.basic.WordTokenizer(),
        http_session: aiohttp.ClientSession | None = None,
    ) -> None:
        super().__init__(
            capabilities=tts.TTSCapabilities(
                streaming=True,
            ),
            sample_rate=sample_rate,
            num_channels=1,
        )

        self._opts = {
            "api_key": api_key,
            "voice": voice,
            "base_url": base_url,
            "sample_rate": sample_rate,
            "word_tokenizer": word_tokenizer,
        }
        self._session = http_session or utils.http_context.http_session()

    async def _connect_websocket(self) -> aiohttp.ClientWebSocketResponse:
        headers = {
            "Authorization": f"Bearer {self._opts['api_key']}",
            "Content-Type": "application/json",
        }
        return await self._session.ws_connect(
            self._opts["base_url"],
            headers=headers,
        )

    def stream(
        self, *, conn_options: APIConnectOptions = DEFAULT_API_CONNECT_OPTIONS
    ) -> "VozySynthesizeStream":
        return VozySynthesizeStream(
            tts=self,
            conn_options=conn_options,
            opts=self._opts,
            session=self._session,
        )

class VozySynthesizeStream(tts.SynthesizeStream):
    def __init__(
        self,
        *,
        tts: TTS,
        session: aiohttp.ClientSession,
        conn_options: APIConnectOptions,
        opts: dict,
    ):
        super().__init__(tts=tts, conn_options=conn_options)
        self._opts = opts
        self._session = session

    async def _run(self) -> None:
        ws = await self._opts["tts"]._connect_websocket()
        request_id = utils.shortuuid()

        async def send_task():
            try:
                async for text in self._input_ch:
                    if isinstance(text, str):
                        message = {
                            "text": text,
                            "voice_id": self._opts["voice"].id,
                            "settings": dataclasses.asdict(self._opts["voice"].settings) if self._opts["voice"].settings else {},
                        }
                        await ws.send_str(json.dumps(message))
            finally:
                await ws.close()

        async def receive_task():
            audio_stream = utils.audio.AudioByteStream(
                sample_rate=self._opts["sample_rate"],
                num_channels=1,
            )

            try:
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.BINARY:
                        # Procesa los datos de audio recibidos
                        for frame in audio_stream.write(msg.data):
                            self._event_ch.send_nowait(
                                tts.SynthesizedAudio(
                                    request_id=request_id,
                                    frame=frame,
                                )
                            )
                    elif msg.type == aiohttp.WSMsgType.TEXT:
                        # Maneja mensajes de control si los hay
                        data = json.loads(msg.data)
                        if "error" in data:
                            raise APIStatusError(
                                f"Vozy error: {data['error']}",
                                status_code=400,
                                request_id=request_id,
                            )
            except Exception as e:
                raise APIConnectionError() from e

        tasks = [
            asyncio.create_task(send_task()),
            asyncio.create_task(receive_task()),
        ]

        try:
            await asyncio.gather(*tasks)
        finally:
            await utils.aio.gracefully_cancel(*tasks) 