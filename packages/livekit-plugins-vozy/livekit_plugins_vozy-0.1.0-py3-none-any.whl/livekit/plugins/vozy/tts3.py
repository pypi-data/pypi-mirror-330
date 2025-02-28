from __future__ import annotations

import asyncio
import base64
import json
import wave
from dataclasses import dataclass
from io import BytesIO
from typing import Dict, List, Optional

import websockets
from livekit.agents import (
    DEFAULT_API_CONNECT_OPTIONS,
    APIConnectionError,
    APIConnectOptions,
    APIStatusError,
    tokenize,
    tts,
    utils,
)

from .log import logger

@dataclass
class VoiceSettings:
    speed: str
    engine: str

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
        base_url: str = "wss://ai-gateway-ws.prod.eksia.us-east-1.c1.vozy.co/api/v2",
        sample_rate: int = 8000,
        word_tokenizer: tokenize.WordTokenizer = tokenize.basic.WordTokenizer(),
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
            "base_url": f"{base_url}?apikey={api_key}",
            "sample_rate": sample_rate,
            "word_tokenizer": word_tokenizer,
        }

    def stream(
        self, *, conn_options: APIConnectOptions = DEFAULT_API_CONNECT_OPTIONS
    ) -> "VozySynthesizeStream":
        return VozySynthesizeStream(
            tts=self,
            conn_options=conn_options,
            opts=self._opts,
        )

class VozySynthesizeStream(tts.SynthesizeStream):
    def __init__(
        self,
        *,
        tts: TTS,
        conn_options: APIConnectOptions,
        opts: dict,
    ):
        super().__init__(tts=tts, conn_options=conn_options)
        self._opts = opts
        self._segments: List[Dict] = []

    def _extract_wav_frames_from_base64(self, base64_wav_str: str) -> bytes:
        audio_data = base64.b64decode(base64_wav_str)
        with wave.open(BytesIO(audio_data), 'rb') as input_wav:
            frames = input_wav.readframes(input_wav.getnframes())
        return frames

    def _build_message(self, text: str) -> str:
        voice = self._opts["voice"]
        config = {
            "vozy_k8s_language": voice.language,
            "vozy_k8s_speed": voice.settings.speed,
            "vozy_k8s_engine": voice.settings.engine,
        }
        if voice.settings.engine == "google":
            config["google_voice_name"] = voice.id
        return json.dumps({"text": text, "vozy_tts_config": config})

    async def _process_message(self, data: Dict, request_id: str):
        audio_stream = utils.audio.AudioByteStream(
            sample_rate=self._opts["sample_rate"],
            num_channels=1,
        )

        if data["type_segment"] == 0:
            # Audio segment
            audio_data = self._extract_wav_frames_from_base64(data["speech_data"]["audio"])
            for frame in audio_stream.write(audio_data):
                self._event_ch.send_nowait(
                    tts.SynthesizedAudio(
                        request_id=request_id,
                        frame=frame,
                    )
                )
        elif data["type_segment"] == 1:
            # Silence segment
            duration_ms = data["silence_data"]["duration_miliseconds"]
            num_samples = int(self._opts["sample_rate"] * (duration_ms / 1000))
            silence_data = b"\x00\x00" * num_samples
            for frame in audio_stream.write(silence_data):
                self._event_ch.send_nowait(
                    tts.SynthesizedAudio(
                        request_id=request_id,
                        frame=frame,
                    )
                )

    async def _run(self) -> None:
        request_id = utils.shortuuid()

        async with websockets.connect(self._opts["base_url"]) as ws:
            try:
                async for text in self._input_ch:
                    if isinstance(text, str):
                        message = self._build_message(text)
                        await ws.send(message)

                        async for msg in ws:
                            try:
                                data = json.loads(msg)
                                await self._process_message(data, request_id)
                            except json.JSONDecodeError as e:
                                raise APIStatusError(
                                    f"Invalid JSON response from Vozy: {e}",
                                    status_code=400,
                                    request_id=request_id,
                                )
            except websockets.exceptions.ConnectionClosed as e:
                if e.code != 1000:  # 1000 es cierre normal
                    raise APIConnectionError(f"WebSocket connection closed: {e}") from e
            except Exception as e:
                raise APIConnectionError(f"Error in Vozy TTS stream: {e}") from e 