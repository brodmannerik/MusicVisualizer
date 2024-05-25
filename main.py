import pygame
import numpy as np
import librosa
import sounddevice as sd
import math
import sys
import os

def startMusicPlayer(song):
    # Load audio file
    try:
        audio_data, sample_rate = librosa.load(song, sr=None)
        print("WAV file loaded successfully")
        duration = librosa.get_duration(y=audio_data, sr=sample_rate)
        return audio_data, sample_rate, duration
    except Exception as e:
        print("Error loading WAV file:", e)
        sys.exit(1)

def update_visualization(amplitude, screen):
    screen.fill((0, 0, 0))  # Clear the screen
    if amplitude == 0:
        pygame.draw.line(screen, (255, 255, 255), (0, screen.get_height() // 2), (screen.get_width(), screen.get_height() // 2), 2)
    else:
        amplitude_scaled = amplitude * (screen.get_height() // 4)  # Adjust amplitude scale
        points = [(x, screen.get_height() // 2 + int(amplitude_scaled * math.sin(x * 0.02))) for x in range(screen.get_width())]
        pygame.draw.lines(screen, (255, 255, 255), False, points, 2)
    pygame.display.flip()

pygame.init()
# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Visualizer")

inputdirectory = input("Enter an input directory: ")

list = os.listdir(inputdirectory)
print(list)

song = input("\nEnter a song name: ")
file = os.path.join(inputdirectory, song)

# Start music player
audio_data, sample_rate, duration = startMusicPlayer(file)

# Play audio
sd.play(audio_data, sample_rate)

start_time = pygame.time.get_ticks()
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time
    if elapsed_time >= duration * 1000:  # Convert duration to milliseconds
        break

    amplitude = np.mean(audio_data[int((elapsed_time / 1000) * sample_rate):int(((elapsed_time + 1) / 1000) * sample_rate)])
    update_visualization(amplitude, screen)
    clock.tick(1000)

sd.wait()
pygame.quit()
sys.exit()
