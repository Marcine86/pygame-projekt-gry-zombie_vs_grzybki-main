import pygame
from pocisk import Pocisk

class Gracz(pygame.sprite.Sprite):
    def __init__(self, pos, const_x, const_y,speed):
        super().__init__()
        self.image = pygame.image.load('Grafika/Grzyb_Krul.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.max_x_const = const_x
        self.max_y_const = const_y
        self.speed = speed
        self.ready = True
        self.bullet_time = 0
        self.bullet_cooldown = 600

        self.pociski = pygame.sprite.Group()
    
    def get_input(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif key[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if key[pygame.K_UP]:
            self.rect.y -= self.speed
        elif key[pygame.K_DOWN]:
            self.rect.y += self.speed
        if key[pygame.K_SPACE] and self.ready:
            self.strzelaj()
            self.ready = False
            self.bullet_time = pygame.time.get_ticks()
    
    def ladowanie(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.bullet_time >= self.bullet_cooldown:
                self.ready = True

    def strzelaj(self):
        self.pociski.add(Pocisk('Kasa',self.rect.center,5,self.rect.bottom))

    def constraint(self):

        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_const:
            self.rect.right = self.max_x_const
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.max_y_const:
            self.rect.bottom = self.max_y_const

    def update(self):
        self.constraint()
        self.get_input()
        self.ladowanie()
        self.pociski.update()