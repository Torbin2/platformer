import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1200,600))
pygame.display.set_caption("platformer")
clock = pygame.time.Clock()


gravity_direction = True
num_list = []
level = 1

ground_rect = pygame.Rect(0,0,200,200)
sky_rect = pygame.Rect(0,0,200,200)

class player:
    
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0,0,50,100)
        self.x_speed = 0
        self.gravity = 0
        self.last_press = 0
        self.ground_grounded = False

    def input(self):
        global gravity_direction
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        
        
        if keys[pygame.K_a]:
            self.x_speed -=1
        if keys[pygame.K_d]:
            self.x_speed +=1
        if keys[pygame.K_SPACE] and current_time - self.last_press > 200:
            gravity_direction = not gravity_direction
            self.last_press = current_time
    def movement(self):
        global gravity_direction
        #left and right
        self.rect.x += self.x_speed
        if self.x_speed >= 0:self.x_speed -=0.5
        if self.x_speed < 0:self.x_speed +=0.5  
        #gravity        
        if self.ground_grounded:
            self.gravity = 0
        else:
            if gravity_direction: self.gravity+= 1
            else: self.gravity-=1
            self.rect.y += self.gravity
        if self.rect.bottom >= 600:
            self.rect.bottom = 600
            if gravity_direction:
                self.gravity = 0
        if self.rect.top <= 0:
            self.rect.top = 0
            if gravity_direction == False:
                self.gravity = 0

    def update(self):
        self.input()
        self.movement()
        pygame.draw.rect(screen, (255,240,255), self.rect)

player_class = player()

def converter():
    rect_list = []
    for number in num_list:
        if number == 1:
            rect_list.append(ground_rect)
        if number == 0:
            rect_list.append(sky_rect)
    for pos, rect in enumerate(rect_list):
        if pos >= 0 and pos <6:
            rect.top = 0
            rect.left = pos  * 200
        elif pos >= 6 and pos < 12: 
            rect.top = 200
            rect.left = (pos - 6) * 200
        elif pos >= 12 and pos < 18: 
            rect.top = 400
            rect.left = (pos - 12) * 200
        if rect == ground_rect:
            pygame.draw.rect(screen, (0,255,0), rect)
            if player_class.rect.colliderect(rect):
                if gravity_direction:
                    player_class.rect.bottom = rect.top
                else:player_class.rect.top = rect.bottom
                player_class.ground_grounded = True
            else: player_class.ground_grounded = False
        if rect == sky_rect:
            pygame.draw.rect(screen,(0,0,255), rect)  




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill((255, 255, 255))
    if level == 1:
        num_list = [0,0,0,1,1,0 ,1,1,1,0,0,0 , 1,0,1,0,1,0]
    
    converter()
    player_class.update()
    
    pygame.display.update()
    clock.tick(60)
    