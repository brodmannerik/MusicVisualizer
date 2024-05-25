import pygame
import numpy as np
import librosa
import sounddevice as sd
import math
import sys
import os

from pydub import AudioSegment


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

def update_visualization(amplitude, screen, bg_color, graph_color):
    screen.fill(bg_color)
    if amplitude == 0:
        pygame.draw.line(screen, graph_color, (0, screen.get_height() // 2), (screen.get_width(), screen.get_height() // 2), 2)
    else:
        amplitude_scaled = amplitude * (screen.get_height() // 4)
        points = [(x, screen.get_height() // 2 + int(amplitude_scaled * math.sin(x * 0.02))) for x in range(screen.get_width())]
        pygame.draw.lines(screen, graph_color, False, points, 2)
    pygame.display.flip()

def convert_mp3_to_wav(mp3_file):
    # Load MP3 file
    audio = AudioSegment.from_mp3(mp3_file)
    # Create output filename
    wav_file = mp3_file[:-4] + ".wav"
    # Export as WAV
    audio.export(wav_file, format="wav")
    return wav_file

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

song = input("\nEnter a song name + .wav or .mp3: \n")
file = os.path.join(inputdirectory, song)

if file.lower().endswith('.mp3'):
    print("Converting MP3 to WAV...")
    file = convert_mp3_to_wav(file)

bg_color_input = input("\nEnter custom background color (R,G,B) - (0-255), or skip with writing 'skip': \n")
if bg_color_input.lower() == 'skip':
    bg_color = (0, 0, 0)
else:
    try:
        bg_color = tuple(map(int, bg_color_input.split(',')))
    except ValueError:
        print("Invalid input for background color. Using default black color.")
        bg_color = (0, 0, 0)

graph_color_input = input("\nEnter custom graph color (R,G,B) - (0-255), or skip with writing 'skip': \n")
if graph_color_input.lower() == 'skip':
    graph_color = (255, 255, 255)
else:
    try:
        graph_color = tuple(map(int, graph_color_input.split(',')))
    except ValueError:
        print("Invalid input for graph color. Using default white color.")
        graph_color = (255, 255, 255)

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
    if elapsed_time >= duration * 1000:
        break

    amplitude = np.mean(audio_data[int((elapsed_time / 1000) * sample_rate):int(((elapsed_time + 1) / 1000) * sample_rate)])
    update_visualization(amplitude, screen, bg_color, graph_color)
    clock.tick(1000)

sd.wait()
pygame.quit()
sys.exit()
