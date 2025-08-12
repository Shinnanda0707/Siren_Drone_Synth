import math
import random


def _step_function(x: float) -> int:
    if x % 2 < 0.5:
        return 1
    return -1


def _triangle_function(x: float) -> float:
    if x % 2 < 1:
        return x % 2
    return 1 - (x - 1) % 2


# White noise oscillator
class WhiteNoiseOscillator:
    def __init__(self, volume: float):
        self.vol = volume
    
    def __iter__(self):
        return self
    
    def __next__(self):
        return random.uniform(0, 1) * self.vol


class Oscillator:
    def __init__(
            self,
            frequency: float,
            volume: float,
            oscillator_type: dict={
                "sine": True,
                "sawtooth": True,
                "sqare": True,
                "triangle": True
            },
            sample_rate: int=44100
            ):
        self.freq = frequency
        self.vol = volume
        self.sample_rate = sample_rate
        self.current = 0
        self.oscillator_type = oscillator_type
    
    def __iter__(self):
        return self
    
    def __next__(self):
        wave = 0
        self.current += (2 * self.freq) / self.sample_rate

        if self.oscillator_type["sine"]:
            wave += math.sin(self.current * math.pi)
        
        if self.oscillator_type["sawtooth"]:
            wave += (self.current % 2) / 2
        
        if self.oscillator_type["sqare"]:
            wave += _step_function(self.current)
        
        if self.oscillator_type["triangle"]:
            wave += _triangle_function(self.current)
        
        return wave / sum(self.oscillator_type.values()) * self.vol


# Sine oscillator iterator
class SineOscillator:
    def __init__(self, frequency: float, volume: float, sample_rate: int=44100):
        self.freq = frequency
        self.vol = volume
        self.sample_rate = sample_rate
        self.current = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        self.current += (math.pi * 2 * self.freq) / self.sample_rate
        return math.sin(self.current) * self.vol


# Sqare oscillator iterator
class SqareOscillator:
    def __init__(self, frequency: float, volume: float, sample_rate: int=44100):
        self.freq = frequency
        self.vol = volume
        self.sample_rate = sample_rate
        self.current = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        self.current += (2 * self.freq) / self.sample_rate
        return _step_function(self.current) * self.vol


# Sawtooth oscillator iterator
class SawtoothOscillator:
    def __init__(self, frequency: float, volume: float, sample_rate: int=44100):
        self.freq = frequency
        self.vol = volume
        self.sample_rate = sample_rate
        self.current = 0
    
    def __iter__(self):
        return self

    def __next__(self):
        self.current += (2 * self.freq) / self.sample_rate
        return (self.current % 2) / 2 * self.vol


# Triangle oscillator iterator
class TriangleOscillator:
    def __init__(self, frequency: float, volume: float, sample_rate: int=44100):
        self.freq = frequency
        self.vol = volume
        self.sample_rate = sample_rate
        self.current = 0
    
    def __iter__(self):
        return self

    def __next__(self):
        self.current += (2 * self.freq) / self.sample_rate
        return _triangle_function(self.current) * self.vol


def lowpass_filter(oscillator, threshold: float, release: float):
    if oscillator.freq < threshold:
        return oscillator.vol
    if oscillator.freq > threshold + release:
        return 0
    return (-1 / release * (oscillator.freq - threshold) + 1) * oscillator.vol
