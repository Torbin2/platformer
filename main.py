import pygame
import tas
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1200,600))
pygame.display.set_caption("platformer")
clock = pygame.time.Clock()
font = pygame.font.SysFont('times new roman', 20)

frame = 0
frame_advance = True
frame_saves = []

movie = tas.TASMovie()  # TODO: go back in file

if movie.mode == "write":
    movie.write_header()
elif movie.mode == "read":
    frame_advance = False
    movie.read_inputs()

gravity_direction = True
num_list = []
level = 1
game_on = True

ground_rect = pygame.Rect(-100,0,100,100)
sky_rect = pygame.Rect(-100,0,100,100)
end_rect = pygame.Rect(-100,0,100,100)
lava_rect = pygame.Rect(-100,0,100,100)
lava_hitbox_rect = pygame.Rect(-100,0,75,75)


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
        global frame
        global gravity_direction
        global level
        global physics
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if physics:
            if movie.mode == "write":
                movie.write_input([keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_SPACE]])
            elif movie.mode == "read":
                print(movie.inputs[frame].l, movie.inputs[frame].r, movie.inputs[frame].s)

        if keys[pygame.K_a] or (movie.mode == "read" and movie.inputs[frame].l):
            self.x_speed -=1
        if keys[pygame.K_d] or (movie.mode == "read" and movie.inputs[frame].r):
            self.x_speed +=1
        if (keys[pygame.K_SPACE] or (movie.mode == "read" and movie.inputs[frame].s)) and current_time - self.last_press > 200 and self.grounded:
            gravity_direction = not gravity_direction
            self.last_press = current_time
            self.grounded = False
        if keys[pygame.K_t]:
            level = 999
            reset_rects()
            level_picker( )

        frame += 1
            

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
        if self.rect.bottom >= 600:
            self.rect.bottom = 600
            self.grounded = True
            self.gravity = 0
        if self.rect.top <= 0:
            self.rect.top = 0
            self.grounded = True
            self.gravity = 0

        if self.rect.right >= 1200: 
            self.rect.right = 1200
            self.x_speed = 0
        if self.rect.left <= 0: 
            self.rect.left = 0
            self.x_speed = 0
        
        
                      
    def update(self):
        self.input()
        self.movement()
        self.screen_side_check()
    def draw(self):
        pygame.draw.rect(screen, ('#18232d'), self.rect)

    def save(self) -> dict:
        return {
            'level': level,
            'x': self.rect.x,
            'y': self.rect.y,
            'xv': self.x_speed,
            'yv': self.gravity,
            'direction': gravity_direction
        }

    def load(self, raw: dict):
        global gravity_direction, level
        level = raw['level']
        level_picker()
        self.rect.x = raw['x']
        self.rect.y = raw['y']
        self.x_speed = raw['xv']
        self.gravity = raw['yv']
        gravity_direction = raw['direction']


player_class = player()

def colision_side_check(rect):
    delta_x = rect.centerx - player_class.rect.centerx
    delta_y = rect.centery - player_class.rect.centery

    abs_delta_x = abs(delta_x)
    abs_delta_y = abs(delta_y)

    if abs(abs_delta_x - abs_delta_y) < 25:
        return

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
        collision_side = colision_side_check(rect)

        if collision_side == "bottom":
            player_class.rect.bottom = rect.top
            player_class.gravity = 0
            player_class.grounded = True
        
        if collision_side == "top":
            player_class.rect.top = rect.bottom
            player_class.gravity = 0
            player_class.grounded = True
        
        if collision_side == "left":
            player_class.rect.left = rect.right
            player_class.x_speed = 0
        
        if collision_side == "right":
            player_class.rect.right = rect.left
            player_class.x_speed = 0
def converter():
    global level
    global gravity_direction
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
            if end_rect.colliderect(player_class.rect):
                level+=1
                reset_rects()
                level_picker()
        if rect == lava_rect:
            pygame.draw.rect(screen, ("#bea925"), rect)
            lava_hitbox_rect.center = rect.center
            if lava_hitbox_rect.colliderect(player_class.rect):
                player_class.rect.topleft = 0,0
                player_class.gravity = 0
                gravity_direction = False
                # level = 1
                # i = rect.x // 100 % 12 + rect.y // 100 * 12
                # reset_rects()
                # level_picker()
                # if i >= len(num_list):
                #     i = len(num_list) - 1
                # if i < 0:
                #     i = 0
                # num_list[i] = 2
def level_picker():
    global num_list
    if level == 1:
        num_list = [0,0,0,0,0,9,9,0,0,0,0,0
            ,0,0,0,0,0,0,0,0,0,0,0,0
           ,0,0,0,0,0,0,0,0,0,0,0,0               
           ,0,0,0,0,0,0,0,0,0,0,0,0
            ,0,0,0,0,0,0,0,0,0,0,0,0
           ,0,0,0,0,0,0,0,0,0,0,0,0]
    if level ==2:
        num_list = [0,1,9,2,0,0,0,0,1,1,1,0
                   ,0,1,0,2,0,0,0,1,1,2,2,0
                   ,0,1,0,2,0,0,0,1,1,1,1,0
                   ,0,1,0,2,0,0,0,1,1,1,1,0
                   ,0,0,0,0,0,0,0,0,1,0,1,0
                   ,0,0,0,0,0,0,0,0,1,0,1,0]
    if level==3:
        num_list = [0,1,0,0,0,0,1,2,2,2,0,0
                   ,0,1,0,0,0,0,1,0,0,9,0,0
                   ,0,1,0,1,1,0,1,0,0,0,0,0
                   ,0,1,0,1,0,0,2,2,2,2,1,0
                   ,0,0,0,1,0,0,2,0,0,0,0,0
                   ,0,0,0,1,0,0,0,0,0,0,0,0]
    #credits to HogoSPR on github
    if level==4:
        num_list= [0,1,1,0,0,0,0,0,0,0,0,9
                  ,0,0,1,0,0,0,0,1,1,1,1,1
                  ,0,0,1,1,1,1,0,0,0,0,0,0               
                  ,0,0,1,0,0,0,0,0,0,0,0,0
                  ,0,0,1,0,0,0,1,1,1,0,0,0
                  ,0,0,0,0,0,0,0,0,0,0,0,0]
    if level==5:
        num_list = [0,1,2,1,0,0,0,0,0,1,1,2
                   ,0,1,2,0,0,2,1,1,0,0,0,0
                   ,0,1,2,0,1,1,0,0,1,2,2,0               
                   ,0,1,2,0,0,0,0,0,2,9,2,0
                   ,0,1,1,1,1,1,1,0,2,0,2,0
                   ,0,0,0,0,0,0,0,0,2,0,0,0]
     #Tommy nikes level
    if level==6:
        num_list = [0,2,0,0,0,2,0,0,0,2,9,2
                    ,0,2,0,2,0,2,0,2,0,2,0,2
                     ,0,2,0,2,0,2,0,2,0,2,0,2
                     ,0,2,0,2,0,2,0,2,0,2,0,2
                    ,0,2,0,2,0,2,0,2,0,2,0,2
                     ,0,0,0,2,0,0,0,2,0,0,0,2]
    if level==7:
        num_list = [0,1,2,1,2,1,2,2,1,2,2,9
           ,0,1,0,0,0,1,0,0,0,0,0,0
           ,0,1,0,1,0,1,0,0,0,0,0,0               
           ,0,0,0,1,0,0,0,0,1,0,1,0
           ,0,1,0,1,0,1,0,0,1,0,0,0
           ,0,1,2,1,2,1,0,0,1,0,2,0]    
    if level == 999:
        num_list =[0,0,2,2,2,0,0,0,0,0,2,2
,0,0,0,2,2,0,1,1,2,0,2,2
,2,0,0,0,2,0,0,1,2,0,1,2
,0,2,0,0,0,2,0,0,2,0,0,0
,0,0,2,0,0,0,2,0,2,1,2,0
,0,0,0,2,0,0,0,0,2,0,2,9] 

def reset_rects():
    global ground_rect
    global sky_rect
    global end_rect
    global lava_rect
    global lava_hitbox_rect
    global player_class
    ground_rect = pygame.Rect(-100,0,100,100)
    sky_rect = pygame.Rect(-100,0,100,100)
    end_rect = pygame.Rect(-100,0,100,100)
    lava_rect = pygame.Rect(-100,0,100,100)
    lava_hitbox_rect = pygame.Rect(-100,0,75,75)
    player_class.rect.topleft = (50,0)
reset_rects()
level_picker()
events = []
physics = True
while True:
    if frame_advance:
        event = pygame.event.wait()
        while not (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                frame_advance = False
                break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player_class.load(frame_saves.pop())
                physics = False
                frame -= 1
                movie.remove_input()
                break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
                physics = False
                break
            events.append(event)
            if event.type == pygame.QUIT:
                break
    if physics:
        for event in events + pygame.event.get():
            if event.type == pygame.QUIT:
                if movie.mode == "write":
                    movie.write_end()
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                frame_advance = True
        events = []
    screen.fill(("#70a5d7"))

    # level_picker()
    if physics:
        player_class.update()
        frame_saves.append(player_class.save())
    converter()
    player_class.draw()

    screen.blit(font.render(str(frame), True, (255, 255, 255)), (0, 0))

    pygame.display.update()
    clock.tick(30)
    physics = True
    