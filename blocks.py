from pygame import *
import pyganim

PLATFORM_COLOR = "#A05550"
COIN_COLOR = "#FFD700"
FINISH_COLOR = "#FAF999"
PLATFORM_WIDTH = PLATFORM_HEIGHT = 32
COIN_ANIMATION_DELAY = 180

class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = image.load("data/platform.png")
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Coin(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(COIN_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.coinanim = [
            ("data/coin1.png", COIN_ANIMATION_DELAY),
            #("data/coin2.png", COIN_ANIMATION_DELAY),
            ("data/coin3.png", COIN_ANIMATION_DELAY),
            #("data/coin4.png", COIN_ANIMATION_DELAY),
            ("data/coin5.png", COIN_ANIMATION_DELAY),
            #("data/coin6.png", COIN_ANIMATION_DELAY),
            ("data/coin7.png", COIN_ANIMATION_DELAY),
            #("data/coin8.png", COIN_ANIMATION_DELAY),
            ("data/coin9.png", COIN_ANIMATION_DELAY),
            ("data/coin10.png", COIN_ANIMATION_DELAY)
        ]
        self.boltCoinAnim = pyganim.PygAnimation(self.coinanim)
        self.boltCoinAnim.play()

class Finish(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT * 1.5))
        self.image.fill(Color(FINISH_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.money_count = 0

    def get_money_count(self):
        return self.money_count

    def increase_money_count(self):
        self.money_count += 1