from pygame import *
import pyganim
import MUSIC
import Functions

MOVE_SPEED = 7
WIDTH = 22
HEIGHT = 32
COLOR = "#888888"
GRAVITY = 0.6
ANIMATION_DELAY = 100


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)

        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.yvel = 0  # скорость падения. 0 - висеть
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y

        self.image = Surface((WIDTH, HEIGHT))
        self.image = image.load("data/0.png")
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект

        self.isGrounded = False
        self.onCoinTile = False

        self.anim_right = [
            ("data/r1.png", ANIMATION_DELAY),
            ("data/r2.png", ANIMATION_DELAY),
            ("data/r3.png", ANIMATION_DELAY),
            ("data/r4.png", ANIMATION_DELAY),
            ("data/r5.png", ANIMATION_DELAY)
        ]

        self.anim_left = [
            ("data/l1.png", ANIMATION_DELAY),
            ("data/l2.png", ANIMATION_DELAY),
            ("data/l3.png", ANIMATION_DELAY),
            ("data/l4.png", ANIMATION_DELAY),
            ("data/l5.png", ANIMATION_DELAY)
        ]

        self.boltAnimRight = pyganim.PygAnimation(self.anim_right)
        self.boltAnimRight.play()

        self.boltAnimLeft = pyganim.PygAnimation(self.anim_left)
        self.boltAnimLeft.play()

        self.mus = MUSIC.Music()

    def update(self, left, right, up, platforms, coins, finish):

        if self.isGrounded:
            self.image = image.load("data/0.png")

        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n
            if self.isGrounded:
                self.boltAnimLeft.blit(self.image, (0, 0))

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n
            if self.isGrounded:
                self.boltAnimRight.blit(self.image, (0, 0))

        if not (left or right or up):  # стоим, когда нет указаний идти
            self.xvel = 0
            if not self.isGrounded:
                self.image = image.load("data/d.png")

        if not self.isGrounded:  # если не на земле, увеличиваем скорость по Y на GRAVITY каждый кадр
            self.yvel += GRAVITY

        if up:
            if self.isGrounded:
                self.yvel -= MOVE_SPEED * 2
            if self.xvel < 0:
                self.image = image.load("data/jl.png")
            elif self.xvel > 0:
                self.image = image.load("data/jr.png")
            else:
                self.image = image.load("data/j.png")


        self.rect.y += self.yvel
        self.collide_motion(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide_motion(self.xvel, 0, platforms)

        self.collide_money(coins, finish)  # запускаем проверку столкновений с монетками,
        # finish передаем чтобы увеличивать счетчик

        if self.collide_finish(finish):  # запускаем проверку столкновения с финишным тайлом

            return self.collide_finish(finish)
        return False

    def collide_motion(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.isGrounded = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает
            else:
                if self.rect.bottom == p.rect.top and self.rect.left > p.rect.left - self.rect.width \
                        and self.rect.right < p.rect.right + self.rect.width:
                    self.isGrounded = True
                    break
                else:
                    self.isGrounded = False


    def collide_money(self, coins, finish):
        for c in coins:
            c.boltCoinAnim.blit(c.image, (0, 0))
            if sprite.collide_rect(self, c):  # пересечение с монеткой
                self.onCoinTile = True
                self.mus.take_a_coin()
                finish.increase_money_count()  # увеличивем счетчик монеток
                c.kill()  # убираем спрайт "c" из группы (entities), таким образом он не рисуется в следующем кадре
                coins.remove(c)  # убираем объект спрайта из списка coins, чтобы перестали срабатывать столкновения
            else:
                self.onCoinTile = False

    def collide_finish(self, finish):
        if sprite.collide_rect(self, finish):
            money = finish.get_money_count()
            self.mus.final_play()
            return money
        else:
            return False
