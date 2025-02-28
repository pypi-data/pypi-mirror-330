from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
import websockets
import json
import wave
from io import BytesIO
import base64

from livekit.agents import (
    DEFAULT_API_CONNECT_OPTIONS,
    APIConnectionError,
    APIConnectOptions,
    APIStatusError,
    APITimeoutError,
    tts,
    utils,
)

#from .log import logger
#from .models import TTSEncoding, TTSModels

@dataclass
class _TTSOptions:
    engine: str
    voice: str
    speed: str
    sample_rate: int
    audio_format: TTSEncoding

DEFAULT_WS_URL = "wss://ai-gateway-ws.prod.eksia.us-east-1.c1.vozy.co/api/v2"
NUM_CHANNELS = 1

class TTS(tts.TTS):
    def __init__(
        self,
        *,
        engine: str = "coqui",
        voice: str = "es-CO",
        speed: str = "100",
        audio_format: TTSEncoding = "pcm",
        sample_rate: int = 8000,
        api_key: str | None = None,
    ) -> None:
        """
        Create a new instance of WebSocket TTS.

        Args:
            engine: The TTS engine to use. defaults to "coqui"
            voice: The voice/language to use. defaults to "es-CO"
            speed: The speech speed. defaults to "100"
            audio_format: The audio format to use. defaults to "pcm"
            sample_rate: The sample rate to use. defaults to 8000
            api_key: The API key to use.
        """
        super().__init__(
            capabilities=tts.TTSCapabilities(
                streaming=False,
            ),
            sample_rate=sample_rate,
            num_channels=NUM_CHANNELS,
        )
        self._api_key = api_key or os.environ.get("VOZY_API_KEY")
        if not self._api_key:
            raise ValueError(
                "API key is required, either as argument or set VOZY_API_KEY environmental variable"
            )

        self._opts = _TTSOptions(
            engine=engine,
            voice=voice,
            speed=speed,
            sample_rate=sample_rate,
            audio_format=audio_format,
        )

    def synthesize(
        self,
        text: str,
        *,
        conn_options: APIConnectOptions = DEFAULT_API_CONNECT_OPTIONS,
        segment_id: str | None = None,
    ) -> "WebSocketStream":
        return WebSocketStream(
            tts=self,
            input_text=text,
            conn_options=conn_options,
            opts=self._opts,
            segment_id=segment_id,
            api_key=self._api_key,
        )

class WebSocketStream(tts.ChunkedStream):
    """Synthesize using WebSocket endpoint"""

    def __init__(
        self,
        tts: TTS,
        input_text: str,
        opts: _TTSOptions,
        conn_options: APIConnectOptions,
        segment_id: str | None = None,
        api_key: str | None = None,
    ) -> None:
        super().__init__(tts=tts, input_text=input_text, conn_options=conn_options)
        self._opts = opts
        self._segment_id = segment_id or utils.shortuuid()
        self._api_key = api_key

    def _build_message(self) -> str:
        config = {
            "vozy_k8s_language": self._opts.voice,
            "vozy_k8s_speed": self._opts.speed,
            "vozy_k8s_engine": self._opts.engine,
        }
        if self._opts.engine == "google":
            config["google_voice_name"] = "en-US-Wavenet-D"
        return json.dumps({"text": self._input_text, "vozy_tts_config": config})

    async def _run(self) -> None:
        stream = utils.audio.AudioByteStream(
            sample_rate=self._opts.sample_rate, num_channels=NUM_CHANNELS
        )
        request_id = utils.shortuuid()
        ws_url = f"{DEFAULT_WS_URL}?apikey={self._api_key}"

        try:
            async with websockets.connect(ws_url) as websocket:
                await websocket.send(self._build_message())

                async for message in websocket:
                    data = json.loads(message)
                    
                    if data["type_segment"] == 0:  # Audio segment
                        audio_data = base64.b64decode(data["speech_data"]["audio"])
                        for frame in stream.write(audio_data):
                            self._event_ch.send_nowait(
                                tts.SynthesizedAudio(
                                    request_id=request_id,
                                    frame=frame,
                                    segment_id=self._segment_id,
                                )
                            )
                    
                    elif data["type_segment"] == 1:  # Silence segment
                        duration_ms = data["silence_data"]["duration_miliseconds"]
                        num_samples = int(self._opts.sample_rate * (duration_ms / 1000))
                        silence_data = b"\x00\x00" * num_samples
                        for frame in stream.write(silence_data):
                            self._event_ch.send_nowait(
                                tts.SynthesizedAudio(
                                    request_id=request_id,
                                    frame=frame,
                                    segment_id=self._segment_id,
                                )
                            )

        except asyncio.TimeoutError as e:
            raise APITimeoutError() from e
        except websockets.exceptions.ConnectionClosed as e:
            raise APIStatusError(
                message=f"WebSocket connection closed: {e.code}",
                status_code=e.code,
                request_id=request_id,
                body=None,
            ) from e
        except Exception as e:
            raise APIConnectionError() from e 