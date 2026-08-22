import sounddevice as sd

class AudioEngine:
    def __init__(self, osc, sample_rate, block_size):
        self.osc = osc
        self.sample_rate = sample_rate
        self.block_size = block_size

        self.stream = sd.OutputStream(
            samplerate=sample_rate,
            blocksize=block_size,
            channels=1,
            dtype="float32",
            callback=self._callback,
        )

    def _callback(self, outdata, frames, time_info, status):
        if status:
            print(f"Audio status: {status}")
        outdata[:, 0] = self.osc.generate(frames)
        # all rows @ column 0 -> the first audio channel

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()