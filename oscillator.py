import numpy as np
from abc import ABC, abstractmethod

class Oscillator(ABC):
    def __init__(self, freq, sample_rate):
        self.freq = freq
        self.sample_rate = sample_rate
        self.phase = 0 # phase starts at 0 @ init

    def generate(self, n):
    # generates sin wave w/ designated params for n samples
    # uses np vectors instead of loops for efficiency
        step_count = self.freq / self.sample_rate
        phases = self.phase + np.arange(n) * step_count
        # array containing phase value of each step

        samples = self._waveform(phases)
        # _waveform() to be defined in subclasses for diff waves

        self.phase = (self.phase + n * step_count) % 1.0
        # advances phases by current block length (ie sample count)

        return samples

    @abstractmethod # decorator, enforces abstractmethod to prevent typerror from creating a subclass without "generate()"
    def _waveform(self, phases):
        pass # in python, empty method cannot be left blank (syntax error o/w)

class SineOscillator(Oscillator): # extends oscillator
    def _waveform(self, phases):
        return np.sin(2.0 * np.pi * phases)

class SawOscillator(Oscillator): # extends oscillator
    def _waveform(self, phases):
        return 2.0 * (phases % 1.0) - 1.0
        # "phases % 1.0" folds values into [0,1)
        # times two minus one maps to [-1, 1)

class TriangleOscillator(Oscillator): # extends oscillator
    def _waveform(self, phases):
        return 1.0 - 4.0 * np.abs(phases % 1.0 - 0.5)
        # "phases % 1.0 - 0.5" folds values into [-.5, .5)
        # abs for desired triangle shape, range now [0, .5)
        # times 4 for range [0, 2)
        # subtract from 1 to invert and start from minval; range [-1, 1)

class SquareOscillator(Oscillator): # extends oscillator
    # @Override needed here if in java
    def __init__(self, freq, sample_rate, duty_cycle=0.5):
        super().__init__(freq=freq, sample_rate=sample_rate)
        self.duty_cycle = duty_cycle

    def _waveform(self, phases):
        return np.where(phases % 1.0 < self.duty_cycle, 1.0, -1.0)
        # pcwise fn for sq wav generation

class WhiteNoiseGenerator(Oscillator):
# TODO: if needed, refactor noise gen to diff class
# for now, noise generator goes under oscillator
    # @Override
    def __init__(self, sample_rate, freq=0):
        super().__init__(freq=freq, sample_rate=sample_rate)
    """
    In definitions: defaults go last
    def __init__(self, sample_rate, freq=0):  # OK
    
    In calls: use keyword args for clarity
    super().__init__(freq=0, sample_rate=sample_rate)
    (instead of "super().__init__(freq, sample_rate)")
    """

    def _waveform(self, phases):
        return np.random.uniform(-1, 1, size=len(phases))