import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1200,600))
pygame.display.set_caption("platformer")
clock = pygame.time.Clock()


gravity_direction = True
num_list = [0,0,0,0,0,0,0,0,0,0,0,0
            ,0,0,0,0,0,0,0,0,0,0,0,0
           ,0,0,0,0,0,0,0,0,0,0,0,0               
           ,0,0,0,0,0,0,0,0,0,0,0,0
            ,0,0,0,0,0,0,0,0,0,0,0,0
           ,0,0,0,0,0,0,0,0,0,0,0,0]
level = 1

ground_rect = pygame.Rect(0,0,100,100)
sky_rect = pygame.Rect(0,0,100,100)
end_rect = pygame.Rect(0,0,100,100)
lava_rect = pygame.Rect(0,0,100,100)


#colour scheme, #446482, #70a5d7, #18232d

class player:
    
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(100,100,50,100)
        self.x_speed = 0
        self.gravity = 0
        self.last_press = 0
        self.grounded = False

    def input(self):
        global gravity_direction
        global level
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
        if gravity_direction: self.gravity+= 1
        else: self.gravity-=1
        self.rect.y += self.gravity


    def screen_side_check(self):
        #side of the screen colisions
        
        self.grounded = False

        if self.rect.bottom >= 600:
            self.rect.bottom = 600
            self.grounded = True
        if self.rect.top <= 0:
            self.rect.top = 0
            self.grounded = True

        if self.rect.right >= 1200: 
            self.rect.right = 1200
            self.x_speed -= 2
        if self.rect.left <= 0: 
            self.rect.left = 0
            self.x_speed += 2
        
        if self.grounded:
            self.gravity = 0
        
                      
    def update(self):
        self.input()
        self.movement()
        self.screen_side_check()
        pygame.draw.rect(screen, ('#18232d'), self.rect)
player_class = player()

def colision_side_check(rect):
    delta_x = rect.centerx - player_class.rect.centerx
    delta_y = rect.centery - player_class.rect.centery

    abs_delta_x = abs(delta_x)
    abs_delta_y = abs(delta_y)

    if abs_delta_x > abs_delta_y:
        if delta_x > 0:
            return "right"
        else:
            return "left"
    else:
        if delta_y > 0:
            return "bottom"
        else:
            return "top"

def colisions(rect):
    if rect.colliderect(player_class.rect):
        colision_side = colision_side_check(rect)
        
        if colision_side == "bottom":
            player_class.rect.bottom = rect.top
            player_class.gravity = 0
        
        if colision_side == "top":
            player_class.rect.top = rect.bottom
            player_class.gravity = 0
        
        if colision_side == "left":
            player_class.rect.left = rect.right
            player_class.x_speed = 0
        
        if colision_side == "right":
            player_class.rect.right = rect.left
            player_class.x_speed = 0

def converter():
    player_class.ground_grounded = False
    rect_list = []
    y_pos = 1
    for number in num_list:
        if number == 1:
            rect_list.append(ground_rect)
        elif number == 0:
            rect_list.append(sky_rect)
        elif number == 2:
            rect_list.append(lava_rect)
        elif number == 9:
            rect_list.append(end_rect)

    for pos, rect in enumerate(rect_list):
        if pos == y_pos * 12:
            y_pos+=1
        pos -= (y_pos*12)-12

        rect.top = (y_pos*100) -100
        rect.left = pos  * 100
        
        if rect == ground_rect:
            pygame.draw.rect(screen, ("#446482"), rect)
            colisions(rect)
        if rect == sky_rect:
            pygame.draw.rect(screen,("#70a5d7"), rect) 
        if rect == end_rect:
            pygame.draw.rect(screen,('#6c25be'), rect)
        if rect == lava_rect:
            pygame.draw.rect(screen, ("#bea925"), rect)
        
def level_picker():
    global num_list
    level = pygame.key.get_pressed()
    if level[pygame.K_1]:
        num_list = [1,2,9,0,0,0,0,0,0,2,2,2
                   ,0,0,0,0,0,0,0,0,0,0,0,0
                   ,0,0,0,0,0,0,0,0,0,0,0,0
                   ,0,0,0,0,0,0,0,0,0,0,0,0
                   ,0,0,0,0,0,0,0,0,0,0,0,0
                   ,0,0,0,0,0,0,0,0,0,0,0,0]
    if level[pygame.K_2]:
        num_list = [0,1,0,0,0,0,1,0,0,0,0,0
                   ,0,1,0,0,0,0,1,0,0,1,0,0
                   ,0,1,0,1,0,0,1,0,0,0,0,0
                   ,0,1,0,1,0,0,1,0,1,1,1,0
                   ,0,0,0,1,0,0,1,0,0,0,0,0
                   ,0,0,0,1,0,0,0,0,0,0,0,0]
    if level[pygame.K_3]:
        num_list= [1,1,1,0,0,0,0,0,0,0,0,9
                  ,0,0,1,0,0,0,0,1,1,1,1,1
                  ,0,0,1,1,1,1,0,0,0,0,0,0               
                  ,0,0,1,0,0,0,0,0,0,0,0,0
                  ,0,0,1,0,0,0,1,1,1,0,0,0
                  ,0,0,0,0,0,0,0,0,0,0,0,0]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill((255, 255, 255))

    level_picker()
    converter()
    player_class.update()
    
    pygame.display.update()
    clock.tick(60)
    