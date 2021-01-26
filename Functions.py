import pygame
import sys
import os
import MUSIC

WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 640
NICKNAME = ''
COINS = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not fullname:
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def write_string(string, x, y, screen, size, color='white'):
    font = pygame.font.Font(pygame.font.match_font('calibri'), size)
    string_rendered = font.render(string, 1, pygame.Color(color))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = y
    intro_rect.x = x
    screen.blit(string_rendered, intro_rect)


def quick_sort(arr):
    if len(arr) < 2:
        return arr
    else:
        pivot = arr[0]
        less = [i for i in arr[1:] if i[-1] >= pivot[-1]]

        greater = [i for i in arr[1:] if i[-1] < pivot[-1]]

        return quick_sort(less) + [pivot] + quick_sort(greater)


def last_image(screen, clock):
    fon = pygame.transform.scale(load_image('end1.jpg'), (800, 640))
    mus = MUSIC.Music()
    mus.end()
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN):
                return
        screen.blit(fon, (0, 0))
        write_string('Спасибо за прохождение!', 220, 20, screen, 35)
        write_string('Ждите новых уровней', 240, 600, screen, 35)
        pygame.display.flip()
        clock.tick(60)


def terminate():
    pygame.quit()
    sys.exit()
