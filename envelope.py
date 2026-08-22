class Envelope:
    def __init__(self, attack_ms, decay_ms, sustain_level, release_ms, sample_rate):
        self.attack = attack_ms
        self.decay = decay_ms
        self.sustain = sustain_level
        self.release = release_ms
        self.sample_rate = sample_rate