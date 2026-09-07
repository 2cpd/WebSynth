from enum import Enum
import numpy as np

class State(Enum):
    IDLE = 1
    ATTACK = 2
    DECAY = 3
    SUSTAIN = 4
    RELEASE = 5
    # alternatively, from enum import auto, then can do "IDLE = auto()" etc
    # java equiv: enum State { IDLE, ATTACK... }

class Envelope:
    def __init__(self, attack_ms, decay_ms, sustain_level, release_ms, sample_rate):
        self.sustain_level = sustain_level
        self.sample_rate = sample_rate

        self.attack_rate = 1.0 / (attack_ms / 1000.0 * sample_rate)
        self.decay_rate = (1.0 - sustain_level) / (decay_ms / 1000.0 * sample_rate)
        # rate = amount of change in env lvl to next state / #samples to reach that lvl

        self.release_ms = release_ms
        """
        self.release_rate = sustain_level / (release_ms / 1000.0 * sample_rate)
        """
        # fixed rls rate causes bug for sustain level = 0, calculate rate on the fly in process()

        self.state = State.IDLE # env always starts at IDLE
        self.current_level = 0.0

    def process(self, n, gate_on):
    # with type hints: def process(self, gate_on:bool, n:int): -> np.ndarray:
        # generate n samples, check state for each sample

        # new empty array[n] for output
        output = np.zeros(n)

        for i in range(n):
            if self.state == State.IDLE:
                if gate_on:
                    self.state = State.ATTACK

            elif self.state == State.ATTACK:
                if not gate_on: # edge case if key released
                    self.state = State.RELEASE
                else:
                    self.current_level += self.attack_rate
                    if self.current_level >= 1.0:
                        self.current_level = 1.0
                        self.state = State.DECAY

            elif self.state == State.DECAY:
                if not gate_on: # edge case if key released
                    self.state = State.RELEASE
                else:
                    self.current_level -= self.decay_rate
                    if self.current_level <= self.sustain_level:
                        self.current_level = self.sustain_level
                        self.state = State.SUSTAIN

            elif self.state == State.SUSTAIN:
                if not gate_on:
                    self.state = State.RELEASE
                self.current_level = self.sustain_level

            elif self.state == State.RELEASE:
                if gate_on:
                    self.state = State.ATTACK
                else:
                    release_rate = self.current_level / (self.release_ms / 1000.0 * self.sample_rate)
                    self.current_level -= release_rate
                    if self.current_level <= 0.0:
                        self.current_level = 0.0
                        self.state = State.IDLE

            output[i] = self.current_level

        return output