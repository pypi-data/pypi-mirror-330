import sys
print(sys.executable)

import asyncio
import websockets
import base64
import json
import wave
from typing import List, Dict, Optional
from io import BytesIO




def extract_wav_frames_from_base64(base64_wav_str):
    audio_data = base64.b64decode(base64_wav_str)
    with wave.open(BytesIO(audio_data), 'rb') as input_wav:
        frames = input_wav.readframes(input_wav.getnframes())
    return frames


class TTSClient:
    def __init__(self, text: str, voice: str, engine: str, speed: str):
        self.text = text
        self.voice = voice
        self.engine = engine
        self.speed = speed
        self.socket_url = "wss://ai-gateway-ws.prod.eksia.us-east-1.c1.vozy.co/api/v2?apikey=123456"
        self.segments: List[Dict] = []
        self.merged_audio: Optional[BytesIO] = None

    async def send_request(self):
        async with websockets.connect(self.socket_url) as websocket:
            await websocket.send(self.build_message())
            try:
                async for message in websocket:
                    await self.process_message(json.loads(message))
            except websockets.exceptions.ConnectionClosed as e:
                self.handle_close(e.code)

    def build_message(self) -> str:
        config = {
            "vozy_k8s_language": self.voice,
            "vozy_k8s_speed": self.speed,
            "vozy_k8s_engine": self.engine,
        }
        if self.engine == "google":
            config["google_voice_name"] = "en-US-Wavenet-D"
        return json.dumps({"text": self.text, "vozy_tts_config": config})

    async def process_message(self, data: Dict):
        if data["type_segment"] == 0:
            self.segments.append(self.create_audio_segment(data))
        elif data["type_segment"] == 1:
            self.segments.append(self.create_silence_segment(data))
        if len(self.segments) == data["len_seg"]:
            self.merged_audio = await self.merge_segments()
            self.save_to_wav("output.wav")

    def create_audio_segment(self, data: Dict) -> Dict:
        audio_data = extract_wav_frames_from_base64(data["speech_data"]["audio"])
        return {
            "type_segment": 0,
            "blob": BytesIO(audio_data),
            "index": data["index_seg"],
        }

    def create_silence_segment(self, data: Dict) -> Dict:
        duration_ms = data["silence_data"]["duration_miliseconds"]
        num_samples = int(8000 * (duration_ms / 1000))
        silence_data = b"\x00\x00" * num_samples
        return {
            "type_segment": 1,
            "blob": BytesIO(silence_data),
            "index": data["index_seg"],
            "silence_data": {"duration_miliseconds": duration_ms},
        }

    async def merge_segments(self) -> BytesIO:
        merged_audio = BytesIO()
        for segment in sorted(self.segments, key=lambda x: x["index"]):
            merged_audio.write(segment["blob"].read())
        merged_audio.seek(0)
        return merged_audio

    def save_to_wav(self, filename: str):
        with wave.open(filename, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(8000)
            wav_file.writeframes(self.merged_audio.read())
        print(f"Audio saved to {filename}")

    def handle_close(self, code: int):
        messages = {
            1000: ("Completed", "All segments synthesized successfully."),
            1001: ("Interrupted", "Connection closed by the client."),
            1006: ("Failed", "Connection closed abruptly."),
        }
        title, description = messages.get(code, ("Error", "Unexpected connection closure."))
        print(f"{title}: {description}")

    async def run(self):
        await self.send_request()


if __name__ == "__main__":
    # se crea una instancia de TTSclient
    client = TTSClient(
        text="Hola, ¿cómo estás? quisiera saber si es posible multiplicar los peces",
        engine="coqui",
        voice="es-CO",
        speed="100",
    )
    asyncio.run(client.run())