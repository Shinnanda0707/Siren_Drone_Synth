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


def get_wave(
        oscillators: list,
        freqency: list,
        master_volume: float,
        white_noise: WhiteNoiseOscillator,
        white_noise_volume: float,
        lowpass_threshold: float,
        lowpass_release: float,
        prev_wave: list,
        reverb_decay: float=0.7,
        buffer_size: int=BUFFER_SIZE
    ) -> list:
    num_tracks = len(oscillators)

    # Get values from sliders & Change oscillator settings
    for i in range(num_tracks):
        oscillators[i].freq = freqency[i]
    white_noise.vol = white_noise_volume

    # Synthesize
    wave = [
        int(((sum(
            [((next(osc) * master_volume) * lowpass_filter(osc, lowpass_threshold, lowpass_release)) for osc in oscillators]
            ) + next(white_noise)) / (num_tracks + 1) * 32767 * (1 - reverb_decay)) + prev_wave[buffer] * reverb_decay)
        for buffer in range(buffer_size)
    ]
    return wave


def run(num_oscillators: int=3, SAMPLE_RATE: int=SAMPLE_RATE, BUFFER_SIZE: int=BUFFER_SIZE, OUTPUT_CHANNELS: int=OUTPUT_CHANNELS):
    # Setup streamer
    stream = pyaudio.PyAudio().open(
        rate=SAMPLE_RATE,
        channels=OUTPUT_CHANNELS,
        format=pyaudio.paInt16,
        output=True,
        frames_per_buffer=BUFFER_SIZE,
    )

    # Setup oscillators
    oscillators = [Oscillator(0, 1) for _ in range(3)]
    sub_oscillators = [Oscillator(0, 1) for _ in range(num_oscillators * 3)]
    white_noise_oscillator = WhiteNoiseOscillator(1)
    prev_buffer_wave = [0 for _ in range(BUFFER_SIZE)]

    oscillators_freq = [0 for _ in range(3)]
    sub_oscillators_freq = [0 for _ in range(num_oscillators * 3)]

    # Pygame setup
    run = True
    win = pygame.display.set_mode((1100, 600))
    font = pygame.font.SysFont("arial", 30, True, False)
    freq = font.render("FREQ", True, (255, 255, 255))
    vol = font.render("VOL", True, (255, 255, 255))
    master = font.render("LOWPASS FILTER", True, (255, 255, 255))
    freq_slider = [
        Slider(win, 100, 100, 400, 40, min=1, max=550, step=0.01),
        Slider(win, 100, 150, 400, 40, min=1, max=550, step=0.01),
        Slider(win, 100, 200, 400, 40, min=1, max=550, step=0.01),
    ]
    vol_slider = Slider(win, 600, 100, 400, 40, min=0, max=1, step=0.0001)
    lowpass_slider = Slider(win, 100, 400, 900, 40, min=-200, max=551, step=0.01)
    wn_slider = Slider(win, 100, 450, 900, 40, min=0, max=1, step=0.0001)

    # Play sound
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        oscillators_freq = [freq_slider[i].getValue() for i in range(len(freq_slider))]
        vols = vol_slider.getValue()
        lt = lowpass_slider.getValue()
        wn = wn_slider.getValue()

        # Update sub oscillators
        for main in range(3):
            for sub in range(num_oscillators):
                sub_oscillators_freq[main * 3 + sub] = oscillators_freq[main] / (sub + 2)

        wave = get_wave(oscillators + sub_oscillators, oscillators_freq + sub_oscillators_freq, vols, white_noise_oscillator, wn, lt, 200, prev_buffer_wave)
        stream.write(numpy.int16(wave).tobytes())
        prev_buffer_wave = wave

        # Display update
        win.fill((0, 0, 0))
        pygame_widgets.update(events)
        win.blit(freq, [100, 50])
        win.blit(vol, [600, 50])
        win.blit(master, [100, 350])
        pygame.display.update()

    # Close streamer
    pygame.quit()
    stream.stop_stream()
    stream.close()


if __name__ == "__main__":
    run()
