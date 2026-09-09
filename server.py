# create audio engine and voice on startup
# serve html page
# accept ws connections
# parse json msgs

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
        msg_type = data.get("type")
        msg_value = data.get("value")

        if msg_type == "gate":
            engine.gate_on = msg_value
        elif msg_type == "freq":
            engine.voice.osc.freq = float(msg_value)
        elif msg_type == "waveform":
            # change osc but preserve curr freq & phase
            curr_freq = engine.voice.osc.freq
            curr_phase = engine.voice.osc.phase

            # wave types: sin, saw, tri, sqr
                # no noise for now
                # sqr needs load % (default to 50 for now)
            if msg_value == "sin":
                engine.voice.osc = oscillator.SineOscillator(curr_freq, engine.sample_rate)
            elif msg_value == "saw":
                engine.voice.osc = oscillator.SawOscillator(curr_freq, engine.sample_rate)
            elif msg_value == "tri":
                engine.voice.osc = oscillator.TriangleOscillator(curr_freq, engine.sample_rate)
            elif msg_value == "sqr":
                engine.voice.osc = oscillator.SquareOscillator(curr_freq, engine.sample_rate, 50)
            engine.voice.osc.phase = curr_phase
        elif msg_type == "attack":
            engine.voice.env.set_attack(float(msg_value))
        elif msg_type == "decay":
            engine.voice.env.set_decay(float(msg_value))
        elif msg_type == "sustain":
            engine.voice.env.set_sustain(float(msg_value))
        elif msg_type == "release":
            engine.voice.env.set_release(float(msg_value))

@app.on_event("shutdown")
async def shutdown_event():
    engine.stop()