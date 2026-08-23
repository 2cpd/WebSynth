import sounddevice as sd

class AudioEngine:
    def __init__(self, osc, env, sample_rate, block_size):
        self.osc = osc
        self.env = env
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

    def _callback(self, outdata, frames, time_info, status):
        if status:
            print(f"Audio status: {status}")
        osc_samples = self.osc.generate(frames)
        env_samples = self.env.process(self.gate_on, frames)
        outdata[:, 0] = osc_samples * env_samples
        # "*" for elem-wise multiplication, vs "@" or "np.dot()" for matrix op'n
        # all rows @ column 0 -> the first audio channel

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()