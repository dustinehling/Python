import pygame
import sys
import time
import math
import random
from os import path

#initialize directory where files are found
img_dir = path.join(path.dirname(__file__), 'EKKO')

#window settings
WINDOWHEIGHT = 600
WINDOWWIDTH = 900
FPS = 30

#colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

#initilize and create window
pygame.init()
pygame.mixer.init()
SIZE = (WINDOWWIDTH,WINDOWHEIGHT)
WINDOW = pygame.display.set_mode(SIZE)
pygame.display.set_caption('OPERATION EKKO')
FPSCLOCK = pygame.time.Clock()

#classes
class Battleship(pygame.sprite.Sprite):
    def __init__(self, battleship_img, all_active_sprites):
        super().__init__()

        #scale player image
        self.image = pygame.transform.scale(battleship_img, (60, 60))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        #set spawn location for ships
        self.rect.x = random.randrange(100, WINDOWWIDTH - 100)
        self.rect.y = random.randrange(100, WINDOWHEIGHT - 100)

        #set speed for x and y values
        self.speed_x = random.choice([-1,1])
        self.speed_y = random.choice([-1,1])

    def update(self):
        ''' update Battleship class '''
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        #simulate zigzag movement
        if(self.rect.x == 100) or (self.rect.x == 300) or (self.rect.x == 500):
            self.speed_y *= random.choice([-1,1])
        if(self.rect.y == 50) or (self.rect.y == 150) or (self.rect.y == 250):
            self.speed_x *= random.choice([-1,1])

        #set window boundries as limits and make ship bounce back in
        if(self.rect.x < 0) or (self.rect.x > 900 - 16):
            self.speed_x *= -1
        if(self.rect.y < 0) or (self.rect.y > 600 - 16 ):
            self.speed_y *= -1

        #self.rect.x = self.rect.x + self.speed_x
        #self.rect.y = self.rect.y + self.speed_y

        #calculate coordinates
        global Bx
        Bx = self.rect.x
        global By
        By = self.rect.y
        distanceBP = math.sqrt((Bx - Px)**2 + (By - Py)**2)
        print("Distance_P2B:",distanceBP)

class Carrier(pygame.sprite.Sprite):
    def __init__(self, carrier_img, all_active_sprites):
        super().__init__()

        #scale player image
        self.image = pygame.transform.scale(carrier_img,(60,60))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        #set spawn location for ships
        self.rect.x = random.randrange(100, WINDOWWIDTH - 100)
        self.rect.y = random.randrange(100, WINDOWHEIGHT - 100)

        #set speed for x and y valuesmarcus aurelius
        self.speed_x = random.choice([-1,1])
        self.speed_y = random.choice([-1,1])

    def update(self):
        ''' update Carrier class '''
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        #set window boundries as limits and make ship bounce back in
        if(self.rect.x < 0) or (self.rect.x > 900 - 16):
            self.speed_x *= -1
        if(self.rect.y < 0) or (self.rect.y > 600 - 16):
            self.speed_y *= -1

        self.rect.x = self.rect.x + self.speed_x
        self.rect.y = self.rect.y + self.speed_y

        #calculate coordinates
        global Cx
        Cx = self.rect.x
        global Cy
        Cy = self.rect.y
        distanceCP = math.sqrt((Cx - Px)**2 + (Cy - Py)**2)
        print("Distance_P2C:",distanceCP)

class Destroyer(pygame.sprite.Sprite):
    def __init__(self, destroyer_img, all_active_sprites):
        super().__init__()

        #scale player image
        self.image = pygame.transform.scale(destroyer_img,(50,50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        #set spawn location for ships
        self.rect.x = random.randrange(100, WINDOWWIDTH - 100)
        self.rect.y = random.randrange(100, WINDOWHEIGHT - 100)

        #player starting angle
        self.angle = random.random()*2*math.pi

        #radius for orbit size
        self.radius = random.randrange(2, 5)

        #set speed for x and y values
        self.speed_x = random.choice([-1,1])
        self.speed_y = random.choice([-1,1])

        #how fast will orbit be
        self.speed = 0.01

    def update(self):
        ''' update Destroyer class '''
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        #set window boundries as limits and make ship bounce back in
        if(self.rect.x < 0) or (self.rect.x > 900 - 16):
            self.speed_x *= -1
        if(self.rect.y < 0) or (self.rect.y > 600 - 16):
            self.speed_y *= -1

        #calculate coordinates
        global Dx
        Dx = self.rect.x
        global Dy
        Dy = self.rect.y
        distanceDP = math.sqrt((Dx - Px)**2 + (Dy - Py)**2)
        print("Distance_P2D:",distanceDP)

class Fishing(pygame.sprite.Sprite):
    def __init__(self, fishing_img, all_active_sprites):
        super().__init__()
        #scale player image
        self.image = pygame.transform.scale(fishing_img, (30, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        #player starting angle
        self.angle = random.random()*2*math.pi

        #radius for orbit size
        self.radius = random.randrange(2, 5)

        #player starting location
        self.center_x = random.randrange(100,800)
        self.center_y = random.randrange(200,400)

        #how fast will orbit be
        self.speed = random.choice([-0.03,0.03])

    def update(self):
        ''' update the Fishing class '''
        #increase the angle such that the spiral isn't too fast
        self.angle += self.speed
        if(self.radius < 50):
            self.radius += .05
        else:
            self.radius = 50
            self.speed = 0.005

        #simulate spiral movement
        self.rect.x = self.radius * math.sin(self.angle) + self.center_x
        self.rect.y = self.radius * math.cos(self.angle) + self.center_y

        #calculate coordinates
        global Fx
        Fx = self.rect.x
        global Fy
        Fy = self.rect.y
        distanceFP = math.sqrt((Fx - Px)**2 + (Fy - Py)**2)
        print("Distance_P2F:",distanceFP)

class Sub(pygame.sprite.Sprite):
    def __init__(self, sub_img, all_active_sprites):
        super().__init__()

        #scale player image
        self.image = pygame.transform.scale(sub_img, (40,40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        #set spawn location for ships
        self.rect.x = random.randrange(100, WINDOWWIDTH - 100)
        self.rect.y = random.randrange(100, WINDOWHEIGHT - 100)

        #player starting angle
        self.angle = random.random()*2*math.pi

        #radius for orbit size
        self.radius = random.randrange(10, 200)

        #set speed for x and y values
        self.speed_x = random.choice([-1,1])
        self.speed_y = random.choice([-1,1])

    def update(self):
        ''' update Sub class '''
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        #set window boundries as limits and make ship bounce back in
        if(self.rect.x < 0) or (self.rect.x > 900 - 16):
            self.speed_x *= -1
        if(self.rect.y < 0) or (self.rect.y > 600 - 16):
            self.speed_y *= -1

        self.rect.x = self.rect.x + self.speed_x
        self.rect.y = self.rect.y + self.speed_y

        #calculate coordinates
        global Sx
        Sx = self.rect.x
        global Sy 
        Sy = self.rect.y
        #coordinates_sub = (Sx,Sy)
        distanceSP = math.sqrt((Sx - Px)**2 + (Sy - Py)**2)
        print("Distance_P2S:",distanceSP)

class Player(pygame.sprite.Sprite):
    def __init__(self,player_img,all_active_sprites):
        super().__init__()
        #scale player image
        self.image = pygame.transform.scale(player_img, (20, 20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        #player starting location
        self.rect.x = WINDOWWIDTH / 2
        self.rect.y = WINDOWHEIGHT/ 2

        #player speed
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        '''update the Player class'''
        #then check if there is event handling for arrow keys
        #change values to control speeds and constrain
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x -= 0.1
        if keys[pygame.K_RIGHT]:
            self.speed_x += 0.1
        if keys[pygame.K_UP]:
            self.speed_y -= 0.1
        if keys[pygame.K_DOWN]:
            self.speed_y += 0.1

        #update movement, stop at boundaries, and contrain speed
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if(self.speed_x > 2):
            self.speed_x = 2
        if(self.speed_y > 2):
            self.speed_y = 2
        if(self.speed_x < -2):
            self.speed_x = -2
        if(self.speed_y < -2):
            self.speed_y = -2
        if(self.rect.x < 0) or (self.rect.x > 900 - 16):
            self.speed_x *= -1
        if(self.rect.y < 0) or (self.rect.y > 600 - 16):
            self.speed_y *= -1

        #calculate coordinates
        global Px
        Px = self.rect.x
        global Py 
        Py = self.rect.y
        #print("Player Position:",Px,Py)

#main program loop
def main():
    
    #load all images
    background = pygame.image.load('/home/knightowl/EKKO/ocean.jpg').convert_alpha()
    background_rect = background.get_rect()
    player_img = pygame.image.load('/home/knightowl/EKKO/player.png').convert_alpha()
    player_img.set_colorkey(BLACK)
    player_rect = player_img.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT / 2))
    battleship_img = pygame.image.load('/home/knightowl/EKKO/battleship.png').convert_alpha()
    carrier_img = pygame.image.load('/home/knightowl/EKKO/carrier.png').convert_alpha()
    destroyer_img = pygame.image.load('/home/knightowl/EKKO/destroyer.png').convert_alpha()
    sub_img = pygame.image.load('/home/knightowl/EKKO/sub.png').convert_alpha()
    fishing_img = pygame.image.load('/home/knightowl/EKKO/fishing.png').convert_alpha()

    #create a list of all sprites
    all_active_sprites = pygame.sprite.Group()
    #create list for ships
    ship_sprites = pygame.sprite.Group()
    #add sprite for Player class
    player = Player(player_img, all_active_sprites)
    all_active_sprites.add(player)

    #create a list of instances to call the class
    battleship1 = Battleship(battleship_img, all_active_sprites)
    battleship2 = Battleship(battleship_img, all_active_sprites)
    battleship3 = Battleship(battleship_img, all_active_sprites)
    carrier1 = Carrier(carrier_img, all_active_sprites)
    carrier2 = Carrier(carrier_img, all_active_sprites)
    carrier3 = Carrier(carrier_img, all_active_sprites)                 #Reduce this and make more efficient
    destroyer1 = Destroyer(destroyer_img, all_active_sprites)
    destroyer2 = Destroyer(destroyer_img, all_active_sprites)
    destroyer3 = Destroyer(destroyer_img, all_active_sprites)
    sub1 = Sub(sub_img, all_active_sprites)
    sub2 = Sub(sub_img, all_active_sprites)
    sub3 = Sub(sub_img, all_active_sprites)
    ships = [battleship1, carrier1, destroyer1, sub1,
            battleship2, carrier2, destroyer2, sub2,
            battleship3, carrier3, destroyer3, sub3]

    #randomly spawn ships
    for i in range(2):
        new_other = Fishing(fishing_img, all_active_sprites)
        all_active_sprites.add(new_other)
        all_active_sprites.add(new_other)

    for i in range(3):
        new_ship = random.sample(ships,1)
        all_active_sprites.add(new_ship)
        print(new_ship)

    #process input/output events
    while True: # main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #update all sprites
        all_active_sprites.update()
        #draw/render
        WINDOW.fill(BLACK)
        #draw background image to game
        WINDOW.blit(background, background_rect)
        all_active_sprites.draw(WINDOW)
        #draw crosshairs 
        pygame.draw.circle(WINDOW,RED,(Px+12,Py+12),150,2)
        pygame.draw.circle(WINDOW,RED,(Px+12,Py+12),100,2)
        pygame.draw.circle(WINDOW,RED,(Px+12,Py+12),50,2)
        #done after drawing everything to the screen
        pygame.display.flip()
        #limit to 30 FPS
        FPSCLOCK.tick(FPS)
        ticks = pygame.time.get_ticks()

if __name__ == "__main__":
    main()
