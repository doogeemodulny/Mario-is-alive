from player import Player
from blocks import *
from camera import Camera
from cutscenes import FinalCutscene, StartCutscene
from Functions import *
from Levels import levels
import MUSIC

# Объявляем переменные
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 640  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#004400"
PLATFORM_WIDTH = PLATFORM_HEIGHT = 32


def camera_configure(camera, target):
    l, t, _, _ = target
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def main(level, number, screen, timer):  # передаем уровень сюда, чтобы можно было потом запускать main с разными уровнями
    number += 1

    pygame.display.set_caption("Yet another Mario")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом
    hero = Player(55, 655)  # создаем героя по (x,y) координатам
    left = right = False  # по умолчанию — стоим
    up = False
    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться

    coins = []  # монетки

    level_width = len(level[0]) * PLATFORM_WIDTH
    level_height = len(level) * PLATFORM_HEIGHT

    camera = Camera(camera_configure, level_width, level_height)

    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            elif col == "M":
                cn = Coin(x, y)
                entities.add(cn)
                coins.append(cn)
            elif col == "F":
                finish = Finish(x, y)
                finish_flag = Finish_flag(x, y)
                entities.add(finish)
                entities.add(finish_flag)
            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля



    for e in entities:  # отображение всего
        bg.blit(e.image, camera.apply(e))  # перерисовываются все блоки, создавая эффект движения камеры
    startscene = StartCutscene(screen, timer)
    nick = startscene.start(bg)  # вот здес
    bg.fill(Color(BACKGROUND_COLOR))

    while 1:  # Основной цикл программы
        timer.tick(30)

        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                terminate()
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

            if e.type == KEYDOWN and e.key == K_UP:
                mus = MUSIC.Music()
                mus.jump()
                up = True

            if e.type == KEYUP and e.key == K_UP:
                up = False

        isFinished = hero.update(left, right, up, platforms, coins, finish)  # передвижение

        if isFinished:  # когда из апдейта (строчка выше) передается, что финиш достигнут, попадаем сюда
            cutscene = FinalCutscene(screen, timer, number, nick, isFinished)
            cutscene.start()
            return

        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        entities.add(hero)
        camera.update(hero) # камера центрируется относительно главного персонажа
        for e in entities: # отображение всего
            screen.blit(e.image, camera.apply(e)) # перерисовываются все блоки, создавая эффект движения камеры

        camera.update(hero)  # камера центрируется относительно главного персонажа


        for e in entities:  # отображение всего
            screen.blit(e.image, camera.apply(e))  # перерисовываются все блоки, создавая эффект движения камеры

        pygame.display.update()  # обновление и вывод всех изменений на экран


if __name__ == "__main__":
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    timer = pygame.time.Clock()
    for level in range(len(levels)):
        main(levels[level], level, screen, timer)
    last_image(screen, timer)
