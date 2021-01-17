import pygame
import sys, os


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


def write_string(string, y, x, screen, color='white'):
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(string, 1, pygame.Color(color))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = y
    intro_rect.x = x
    screen.blit(string_rendered, intro_rect)



def terminate():
    pygame.quit()
    sys.exit()


class FinalCutscene():
    def __init__(self, screen, clock, cn):
        self.clock = clock
        fon = pygame.transform.scale(load_image('win1.jpg'), (800, 640))
        screen.blit(fon, (0, 0))

    def start(self):  # лучше сделать тут всю логику, а в мэйне просто запустить
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            self.clock.tick(60)



class StartCutscene():
    def __init__(self, screen, clock):
        self.clock = clock
        line1 = 'Добро пожаловать!'
        line2 = 'Нажмите на любую кнопку, чтобы продолжить.'

        write_string(line1, 100, 300, screen)
        write_string(line2, 600, 200, screen, 'light blue')

    def start(self):  # тоже самое
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            self.clock.tick(60)
