import sounddevice as sd
from voice import Voice

class AudioEngine:
    def __init__(self, vc:Voice, sample_rate, block_size):
        self.voice = vc
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.gate_on = False

        self.stream = sd.OutputStream(
            samplerate=sample_rate,
            blocksize=block_size,
            channels=1,
            dtype="float32",
            callback=self._callback,
        )

    def _callback(self, outdata, n, time_info, status):
        if status:
            print(f"Audio status: {status}")
        outdata[:, 0] = self.voice.generate(n, self.gate_on)
        # "*" for elem-wise multiplication, vs "@" or "np.dot()" for matrix op'n
        # all rows @ column 0 -> the first audio channel

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()