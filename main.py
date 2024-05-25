import pygame
import math
import pyaudio

#pygame init
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Audio Visualizer')

#pyaudio init
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

def get_microphone_input_level():
    try:
        data = stream.read(CHUNK, exception_on_overflow=False)
    except IOError as e:
        print(f"Error reading stream: {e}")
        return 0
    rms = 0
    for i in range(0, len(data), 2):
        sample = int.from_bytes(data[i:i + 2], byteorder='little', signed=True)
        rms += sample * sample
    rms = math.sqrt(rms / (CHUNK / 2))
    return rms

def draw_sine_wave(amplitude):
    screen.fill((0, 0, 0))
    points = []
    if amplitude > 10:
        for x in range(SCREEN_WIDTH):
            y = SCREEN_HEIGHT / 2 + int(amplitude * math.sin(x * 0.02))
            points.append((x, y))
    else:
        points.append((0, SCREEN_HEIGHT / 2))
        points.append((SCREEN_WIDTH, SCREEN_HEIGHT / 2))

    pygame.draw.lines(screen, (255, 255, 255), False, points, 2)

running = True
amplitude = 100

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        amplitude_adjust = get_microphone_input_level() / 50
        amplitude = max(10, amplitude_adjust)

        input_level = get_microphone_input_level()
        print(input_level)

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
stream.stop_stream()
stream.close()
p.terminate()