import pygame
import math
import pyaudio
from pydub import AudioSegment

#pygame init
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Audio Visualizer')

p = pyaudio.PyAudio()

mp3_file = "Toco_Meu_Rio.mp3"
audio = AudioSegment.from_mp3(mp3_file)

# Convert to PCM audio data
pcm_data = audio.raw_data
format = p.get_format_from_width(audio.sample_width)
channels = audio.channels
rate = audio.frame_rate

def play_audio():
    # Open PyAudio stream
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    output=True)
    # Play audio
    stream.write(pcm_data)

    # Close PyAudio stream
    stream.stop_stream()
    stream.close()
    p.terminate()

def draw_sine_wave(amplitude):
     screen.fill((0, 0, 0))
     points = []
     for x in range(SCREEN_WIDTH):
         y = SCREEN_HEIGHT / 2 + int(amplitude * math.sin(x * 0.02))
         points.append((x, y))
     pygame.draw.lines(screen, (255, 255, 255), False, points, 2)
     pygame.display.flip()

running = True
# amplitude = 100

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # amplitude_adjust = get_microphone_input_level() / 50
        # amplitude = max(10, amplitude_adjust)
        #
        # input_level = get_microphone_input_level()
        # print(input_level)

        play_audio()

        # draw_sine_wave(amplitude)
        # pygame.display.flip()
        clock.tick(60)

pygame.quit()
# stream.stop_stream()
# stream.close()
# p.terminate()