import pygame
import numpy as np
import librosa
import sounddevice as sd
import math
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Visualizer")

# Load audio file
try:
    audio_data, sample_rate = librosa.load("Toco_Meu_Rio.wav", sr=None)
    print("WAV file loaded successfully")
except Exception as e:
    print("Error loading WAV file:", e)
    sys.exit(1)

# Normalize audio data to range [0, 1]
normalized_audio = (audio_data - np.min(audio_data)) / (np.max(audio_data) - np.min(audio_data))

def get_amplitude_data():
    num_samples_per_ms = sample_rate // 1000  # Samples per millisecond
    for millisecond in range(len(normalized_audio) // num_samples_per_ms):
        start = millisecond * num_samples_per_ms
        end = start + num_samples_per_ms
        amplitude = np.mean(normalized_audio[start:end])
        yield amplitude

amplitude_generator = get_amplitude_data()

def update_visualization(amplitude):
    screen.fill(BLACK)
    points = []
    if amplitude == 0:
        # Draw a flat line when amplitude is 0
        points = [(x, HEIGHT // 2) for x in range(WIDTH)]
    else:
        # Scale amplitude to screen height and draw sine wave
        amplitude_scaled = amplitude * (HEIGHT // 2)
        for x in range(WIDTH):
            y = HEIGHT / 2 + amplitude_scaled * math.sin(x * 0.02)
            points.append((x, int(y)))
    pygame.draw.lines(screen, WHITE, False, points, 2)
    pygame.display.flip()

# Play audio
sd.play(normalized_audio, sample_rate)

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    try:
        amplitude = next(amplitude_generator)
        print(amplitude)
    except StopIteration:
        break

    update_visualization(amplitude)
    clock.tick(1000)

sd.wait()
pygame.quit()
sys.exit()
