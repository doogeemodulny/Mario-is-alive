from Functions import *
from pygame_textinput import TextInput
from DataBase import *
import MUSIC

textinput = TextInput()


class FinalCutscene():  # всё, что происходит после окончания уровня
    def __init__(self, screen, clock, level, nick, coins):
        self.background = screen
        self.screen = screen
        self.coins = coins
        self.nick = nick
        self.clock = clock
        self.level = level

        add(self.nick, self.level, self.coins)  # добавление данных в базу данных

    def start(self):  # вывод результатов
        res = conclusion(self.nick, self.level)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN):
                    self.results()
                    return  # начинаем игру
            self.screen.blit(self.background, (0, 0))  # фон - игровой уровень
            write_string('Имя персонажа:  ' + self.nick, 300, 300, self.screen, 30, 'light blue')
            write_string('Собрано монет:  ' + str(self.coins), 300, 350, self.screen, 30, 'light blue')
            write_string('Лучший результат:  ' + str(res[1]), 300, 400, self.screen, 30, 'light blue')
            pygame.display.flip()
            self.clock.tick(60)

    def results(self):  # Вывод таблицы лидеров
        a = top5(self.level)  # связь с бд для получения топ 5 игроков
        if len(a) > 5:
            a = a[:5]
            print(a)
        if len(a) < 5:
            while len(a) != 5:
                a.append((' ', ' '))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN):
                    return  # начинаем игру
            self.screen.fill("#004400")
            write_string('Таблица лидеров', 40, 20, self.screen, 100)
            x, y = 200, 150
            x1 = 410
            for i in range(5):  # Отрисовка
                pygame.draw.rect(self.screen, pygame.Color('white'), (x, y, 200, 40))
                write_string(str(a[i][0]), x, y, self.screen, 50, 'black')
                pygame.draw.rect(self.screen, pygame.Color('white'), (x1, y, 100, 40))
                write_string(str(a[i][1]), x1, y, self.screen, 50, 'black')
                y += 50
            pygame.display.flip()
            self.clock.tick(60)


class StartCutscene():
    def __init__(self, screen, clock):
        self.clock = clock
        self.screen = screen

        self.st = MUSIC.Music()  # Стартовая музыка
        self.st.start_play()

    def start(self, star_screen):  # стартовый экран
        while True:
            self.screen.fill((0, 0, 0))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.st.stop()
                    terminate()
                elif event.type == pygame.KEYDOWN and (
                        event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN):
                    self.screen.fill((0, 0, 0))
                    nick = textinput.get_text()
                    self.st.stop()
                    return nick  # начинаем игру

            line1 = 'Добро пожаловать!'
            line2 = 'Нажмите ENTER, чтобы продолжить.'
            line3 = 'Введите имя:'

            self.screen.blit(star_screen, (0, 0))

            write_string(line1, 280, 100, self.screen, 30, 'light blue')  # Вывод надписей для игрока
            write_string(line2, 200, 600, self.screen, 30, 'light blue')
            write_string(line3, 280, 300, self.screen, 30)

            pygame.draw.rect(self.screen, pygame.Color('white'), (280, 350, 250, 40))  # Прямоугольник для ввода
            textinput.update(events)
            self.screen.blit(textinput.get_surface(), (280, 355))  # Ввод текста
            pygame.display.flip()
            self.clock.tick(60)
