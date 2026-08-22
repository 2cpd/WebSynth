import time
import oscillator
from engine import AudioEngine

SAMPLE_RATE = 44100
BLOCK_SIZE = 512

if __name__ == '__main__':
    # [test all 4 types of oscillators]
    test_oscs = [
        oscillator.SineOscillator(freq=880, sample_rate=SAMPLE_RATE),
        oscillator.SawOscillator(freq=110, sample_rate=SAMPLE_RATE),
        oscillator.TriangleOscillator(freq=440, sample_rate=SAMPLE_RATE),
        oscillator.SquareOscillator(freq=220, sample_rate=SAMPLE_RATE, duty_cycle=0.5),
    ]

    engine = AudioEngine(test_oscs[0], sample_rate=SAMPLE_RATE, block_size=BLOCK_SIZE)
    engine.start()

    for index, osc in enumerate(test_oscs):
        print(f"Playing wave #{index}, frequency = {osc.freq} Hz, using {type(osc).__name__}")
        # alternatively str(type(osc))[8:-2] instead of type(osc).__name__

        engine.osc = osc  # swap the oscillator
        time.sleep(2)

    noise_osc = oscillator.WhiteNoiseGenerator(sample_rate=SAMPLE_RATE)
    print("Playing white noise")
    engine.osc = noise_osc
    time.sleep(2)

    engine.stop()
