import pygame
import numpy as np
import librosa
import sounddevice as sd
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Visualizer")

try:
    audio_data, sample_rate = librosa.load("Toco_Meu_Rio.wav", sr=None)
    print("WAV file loaded successfully")
except Exception as e:
    print("Error loading WAV file:", e)
    sys.exit(1)

# Normalize audio data to range [0, 1]
normalized_audio = (audio_data - np.min(audio_data)) / (np.max(audio_data) - np.min(audio_data))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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
    line_height = HEIGHT - int(amplitude * HEIGHT)
    pygame.draw.line(screen, WHITE, (0, line_height), (WIDTH, line_height), 2)
    pygame.display.flip()

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
