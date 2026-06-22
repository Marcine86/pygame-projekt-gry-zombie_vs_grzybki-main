import pygame

class Pocisk(pygame.sprite.Sprite):
    def __init__(self, type, pos, speed, screen_h):
        super().__init__()
        filepath = 'Grafika/' + type + '.png'
        self.image = pygame.image.load(filepath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2,self.image.get_height()*2))
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.max_y_const = screen_h

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.max_y_const + 50:
            self.kill()

    def update(self):
        self.rect.y -= self.speed
        self.destroy()

