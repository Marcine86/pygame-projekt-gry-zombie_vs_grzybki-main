import pygame , sys
from gracz import Gracz
from Przeciwnicy import Muchomor, Ognisty
from random import randint, choice
from pocisk import Pocisk
from button import Button

waluta = 0

class Game:
    def __init__(self):
        
        # Gracz
        self.gracz_sprite = Gracz((screen_w / 2, screen_h),screen_w,screen_h,5)
        self.gracz = pygame.sprite.GroupSingle(self.gracz_sprite)

        # Punkty i Życia
        self.serca = 3
        self.serce_sprite = pygame.image.load('Grafika/Punkt_Zdrowia.png').convert_alpha()
        self.serce_sprite = pygame.transform.scale(self.serce_sprite, (50,50))
        self.serce_x_start = screen_w - (self.serce_sprite.get_size()[0] * 2 + 20)
        self.punkty = 0
        self.czcionka = pygame.font.SysFont('Comic Sans',30)
        # Rundy
        self.runda = 0
        self.ilosc_much = 0
        self.ilosc_much_max = 15

        # Muchomory
        self.muchomory = pygame.sprite.Group()
        # Ognisty 
        self.ognisty = pygame.sprite.Group()
        self.ognisty_czas = randint(400,800)
        self.ognisty_pociski = pygame.sprite.Group()

        # Muzyka / Audio
        self.Muzyka_Gry = pygame.mixer.Sound('Muzyka/Grzybv3.mp3')
        self.Muzyka_Gry.set_volume(0.6)
        self.Muzyka_Gry.play(loops=-1)
    
    def Muchomor_spawner(self,rows,cols):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                ran = randint(0,550)
                x = row_index + ran
                y = col_index
        self.muchomor_sprite = Muchomor(x,y,1)
        self.muchomory.add(self.muchomor_sprite)

    def Ognisty_spawner(self,rows,cols,x_distance,y_distance,x_offset):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance
                self.ognisty_sprite = Ognisty(x,y)
                self.ognisty.add(self.ognisty_sprite)

    def Ognisty_timer(self):
        self.ognisty_czas -= 1
        if self.ognisty_czas <= 0:
            self.Ognisty_spawner(1,3,150,48,80)
            self.ognisty_czas = randint(400,800)

    def Ognisty_Strzelaj(self):
        if self.ognisty.sprites():
            random = choice(self.ognisty.sprites())
            pocisk = Pocisk('Kula_ognia',(random.rect.x,random.rect.y),-3,screen_h)
            self.ognisty_pociski.add(pocisk)
    
    def Muchomor_Deploy(self):
        if self.muchomory.sprites():
            deploy = Pocisk('Kula_ognia',(self.muchomor_sprite.rect.x,self.muchomor_sprite.rect.y),5,self.muchomor_sprite.rect.top)
            self.ognisty_pociski.add(deploy)

    def Pokaz_Punkty(self):
        wynik_sprite = self.czcionka.render(f'Wynik: {self.punkty}',False,'white')
        wynik_rect = wynik_sprite.get_rect(topleft = (10,10))
        runda_sprite = self.czcionka.render(f'RUNDA {self.runda}',False,'white')
        runda_rect = runda_sprite.get_rect(topright = (590,10))
        ilosc_sprite = self.czcionka.render(f'{self.ilosc_much}/{self.ilosc_much_max}',False,'white')
        ilosc_rect = ilosc_sprite.get_rect(topright = (590,30))
        screen.blit(wynik_sprite,wynik_rect)
        screen.blit(ilosc_sprite,ilosc_rect)
        screen.blit(runda_sprite,runda_rect)

    def Pokaz_Zycia(self):
        for serce in range(self.serca - 1):
            y = self.serce_x_start + (serce * self.serce_sprite.get_size()[0] + 10)
            screen.blit(self.serce_sprite,(5,y))

    def Pokaz_Runde(self):
        czcionka = pygame.font.SysFont('Comic Sans',90,False,False)
        self.runda += 1
        self.ilosc_much = 0
        self.ilosc_much_max += 5
        round_sprite = czcionka.render(f'RUNDA {self.runda}',True,'white')
        round_rect = round_sprite.get_rect(center = (screen_w/2,screen_h/2-50))
        screen.blit(round_sprite,round_rect)
        pygame.display.flip()
        clock.tick(1)
        round_sprite = czcionka.render('GO!',True,'white')
        round_rect = round_sprite.get_rect(center = (screen_w/2,screen_h/2+30))
        screen.blit(round_sprite,round_rect)
        pygame.display.flip()
        clock.tick(1)
            
    def check_collisions(self):
        # Sprawdza, czy istnieją pociski gracz
        global waluta
        if self.gracz.sprite.pociski:
            for pocisk in self.gracz.sprite.pociski:
                if pygame.sprite.spritecollide(pocisk, self.muchomory, True): 
                    # Sprawdza czy pocisk i muchomor dotknęli siebie, oraz sprawdza, czy zabijać Muchomora.
                    pocisk.kill()
                    self.punkty += 5
                    self.ilosc_much += 1
                
                if pygame.sprite.spritecollide(pocisk, self.ognisty, True):
                    pocisk.kill()
                    self.punkty += 10
                    self.ilosc_much += 1
        
        if self.muchomory.sprites():
            for enemy in self.muchomory:
                if pygame.sprite.spritecollide(enemy,self.gracz, False):
                    enemy.kill()
                    self.serca -= 1
                    if self.serca <= 0:
                        waluta += self.punkty
                        self.Muzyka_Gry.stop()
                        Scena_Menu()

        if self.ognisty.sprites():
            for enemy in self.ognisty:
                if pygame.sprite.spritecollide(enemy,self.gracz, False):
                    enemy.kill()
                    self.serca -= 1
                    if self.serca <= 0:
                        waluta += self.punkty
                        self.Muzyka_Gry.stop()
                        Scena_Menu()

        if self.ognisty_pociski.sprites():
            for enemy in self.ognisty_pociski:
                if pygame.sprite.spritecollide(enemy,self.gracz, False):
                    enemy.kill()
                    self.serca -= 1
                    if self.serca <= 0:
                        waluta += self.punkty
                        self.Muzyka_Gry.stop()
                        Scena_Menu()

    def run(self):
        self.gracz_sprite.pociski.draw(screen)
        self.gracz.update()
        self.gracz.draw(screen)

        if self.ilosc_much_max == self.ilosc_much:
            self.Pokaz_Runde()
            self.muchomory.empty()
            self.ognisty.empty()
            self.ognisty_pociski.empty()
        else:
            self.muchomory.draw(screen)
            self.muchomory.update(self.gracz_sprite)
            self.Muchomor_Deploy() # ============== OPCJONALNE ==============

            self.Ognisty_timer()
            self.ognisty.update(self.ognisty)
            self.ognisty.draw(screen)
            self.ognisty_pociski.update()
            self.ognisty_pociski.draw(screen)

        self.Pokaz_Zycia()
        self.Pokaz_Punkty()
        self.check_collisions()
# POZA KLASE GAME
def Scena_Gra():
    game = Game()

    ENEMYSPAWN = pygame.USEREVENT + 1
    pygame.time.set_timer(ENEMYSPAWN,1275)
    OGNISTYPOCISK = pygame.USEREVENT + 1
    pygame.time.set_timer(OGNISTYPOCISK,900)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ENEMYSPAWN:
                game.Muchomor_spawner(6,8)
            if event.type == OGNISTYPOCISK:
                game.Ognisty_Strzelaj()
    
        screen.fill((0,175,0))
        pygame.draw.circle(screen,(150,75,0),(screen_w/2,(screen_h/2)-400),400)
        game.run()

        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)

def Scena_Menu():
    pygame.init()
    global waluta

    play_button = Button((0, 255, 0), 50, 250, 150, 50, 'Graj')
    quit_button = Button((255, 0, 0), 400, 250, 150, 50, 'Wyjdź')

    Muzyka_Gry = pygame.mixer.Sound('Muzyka/grzybv2.mp3')
    Muzyka_Gry.set_volume(0.6)
    Muzyka_Gry.play(loops=-1)

    font = pygame.font.SysFont('Comic Sans',30,False)
    title_sprite = font.render('Borowiki vs Muchomory',True,'black')
    title_rect = title_sprite.get_rect(topleft = (screen_w/4,screen_h/6))
    moneta_s = pygame.image.load('Grafika/Kasa.png').convert_alpha()
    moneta_s = pygame.transform.scale(moneta_s,(moneta_s.get_width()*2,moneta_s.get_height()*2))
    moneta_r = moneta_s.get_rect(topleft = (10,20))
    waluta_sprite = font.render(f'{waluta}',False,'black')
    waluta_rect = waluta_sprite.get_rect(topleft = (75,10))

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_over(pygame.mouse.get_pos()):
                    print("GRAJ")
                    Muzyka_Gry.stop()
                    Scena_Gra()
                if quit_button.is_over(pygame.mouse.get_pos()):
                    print("WYJDŹ")
                    pygame.quit()
                    sys.exit()

        screen.fill((255,155,0))
        play_button.draw(screen)
        quit_button.draw(screen)
        screen.blit(title_sprite,title_rect)
        screen.blit(waluta_sprite,waluta_rect)
        screen.blit(moneta_s,moneta_r)

        pygame.display.update()
        pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    screen_w = 600
    screen_h = 600
    screen = pygame.display.set_mode((screen_w,screen_h))
    pygame.display.set_caption("Grzybki vs Muchomory")
    clock = pygame.time.Clock()
    Scena_Menu()