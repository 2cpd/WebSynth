# create audio engine and voice on startup
# serve html page
# accept ws connections
# parse json msgs
import fastapi

from envelope import Envelope
import oscillator
from voice import Voice
from engine import AudioEngine

from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse

SAMPLE_RATE = 44100
BLOCK_SIZE = 512

app = FastAPI()

# pre html setup
test_env = Envelope(attack_ms=100, decay_ms=100, sustain_level=0.5, release_ms=1000, sample_rate=SAMPLE_RATE)
test_osc = oscillator.TriangleOscillator(freq=440.0, sample_rate=SAMPLE_RATE)
test_voice = Voice(test_osc, test_env)
engine = AudioEngine(test_voice, sample_rate=SAMPLE_RATE, block_size=BLOCK_SIZE)
engine.start()

@app.get("/")
async def get():
    return FileResponse("index.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        if data.get("type") == "gate":
            engine.gate_on = data.get("value", False)

@app.on_event("shutdown")
async def shutdown_event():
    engine.stop()


