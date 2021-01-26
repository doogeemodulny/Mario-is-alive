import pygame
import random

class Music():
    def __init__(self):
        pass

    def start_play(self):
        pygame.mixer.music.load(r"data\start_music.mp3")
        pygame.mixer.music.play()

    def final_play(self):
        pygame.mixer.music.load(r"data\final_music.mp3")
        pygame.mixer.music.play()

    def jump(self):
        pygame.mixer.music.load(r"data\jump_music.mp3")
        pygame.mixer.music.play()

    def take_a_coin(self):
        pygame.mixer.music.load(r"data\coin_music.mp3")
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def end(self):
        i = random.randint(1, 4)
        pygame.mixer.music.load(r"data\end_" + str(i) + ".mp3")
        pygame.mixer.music.play()
