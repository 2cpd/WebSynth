import oscillator
import envelope

class Voice:
    def __init__(self, osc, env):
        self.osc = osc
        self.env = env

    def generate(self, n, gate_on):
        osc_samples = self.osc.generate(n)
        env_samples = self.env.process(n, gate_on)
        return osc_samples * env_samples