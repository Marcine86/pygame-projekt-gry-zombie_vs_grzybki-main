import pygame

class Muchomor(pygame.sprite.Sprite):
    def __init__(self,x,y,speed):
        super().__init__()
        self.image = pygame.image.load('Grafika/Muchomor.png')
        self.rect = self.image.get_rect(topleft = (x,y))
        self.speed = speed
    
    def update(self,gracz):
        pozycja_gracza = gracz
        if self.rect.x >= pozycja_gracza.rect.x:
            self.rect.x -= self.speed
        if self.rect.x < pozycja_gracza.rect.x:
            self.rect.x += self.speed
        if self.rect.y >= pozycja_gracza.rect.y:
            self.rect.y -= self.speed
        if self.rect.y < pozycja_gracza.rect.y:
            self.rect.y += self.speed

            

class Ognisty(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load('Grafika/MuchomorOgnisty.png')
        self.rect = self.image.get_rect(topleft = (x,y))
        self.speed = 1

    def update(self,grupa):
        self.rect.x += self.speed
        for ognisty in grupa.sprites():
            if ognisty.rect.right >= 600:
                self.speed = -1
            elif ognisty.rect.left <= 0:
                self.speed = 1