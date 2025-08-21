import math
import random

import numpy
import pyaudio

import pygame
import pygame_widgets
from pygame_widgets.slider import Slider

from oscillators import Oscillator, WhiteNoiseOscillator, lowpass_filter
pygame.init()

# Static variables
SAMPLE_RATE = 44100
BUFFER_SIZE = 2048
OUTPUT_CHANNELS = 1


# White noise oscillator
class WhiteNoiseOscillator:
    def __init__(self, volume: float):
        self.vol = volume

    def __iter__(self):
        return self

    def __next__(self):
        return random.uniform(0, 1) * self.vol / 2


class Oscillator:
    def __init__(self, frequency: float, sample_rate: int=SAMPLE_RATE):
        self.freq = frequency
        self.sample_rate = sample_rate
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.current += (2 * self.freq) / self.sample_rate
        return (math.sin(self.current * math.pi) + (self.current % 2) / 2) / 12


def lowpass_filter(val: float, lowpass_threshold: float, lowpass_release: float) -> float:
    return min(max((lowpass_threshold - val) / lowpass_release / 2 + 1 / 2, 0), 1 / 2)


def get_wave(
        oscillators: list,
        master_volume: float,
        white_noise: WhiteNoiseOscillator,
        lowpass_threshold: float,
        lowpass_release: float,
        buffer_size: int=BUFFER_SIZE
    ) -> list:
    # Synthesize
    return [
        int(((lowpass_filter(sum([next(osc) for osc in oscillators]), lowpass_threshold, lowpass_release)
        + next(white_noise)) * 32767)
        for _ in range(buffer_size)
    ]


def run(num_oscillators: int=3, SAMPLE_RATE: int=SAMPLE_RATE, BUFFER_SIZE: int=BUFFER_SIZE, OUTPUT_CHANNELS: int=OUTPUT_CHANNELS):
    pass


if __name__ == "__main__":
    run()
