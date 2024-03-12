# V1.5.0
import os
import random

show_hitboxes = False

import pygame
from Levels import level_picker

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("platformer")
clock = pygame.time.Clock()
current_time = pygame.time.get_ticks()
scroll = [0,0]

gravity_direction = True
num_list = []
level = 0
game_on = True
last_run_time = 0

test_level = 17

sounds = {}
for sound in os.listdir("assets/sounds"):
    sounds[sound.split('.')[0]] = pygame.mixer.Sound(f"assets/sounds/{sound}")

musics = []
for music in os.listdir('assets/music'):
    musics.append(f'assets/music/{music}')
random.shuffle(musics)

pygame.mixer.music.load(musics[0])
for music in musics[1:]:
    pygame.mixer.music.queue(music)
pygame.mixer.music.play(loops = -1)


font = pygame.font.Font(("assets/Pixeltype.ttf"), 50)

ground_rect = pygame.Rect(-100, 0, 100, 100)
sky_rect = pygame.Rect(-100, 0, 100, 100)
end_rect = pygame.Rect(-100, 0, 100, 100)
lava_rect = pygame.Rect(-100, 0, 100, 100)
level_building_rects = [sky_rect, ground_rect, lava_rect, end_rect]
lava_hitbox_rect = pygame.Rect(-100, 0, 50, 50)
# button
button_rect = pygame.Rect(0, 0, 0, 0)
b_long = 80
b_short = 35
button_clicks = 0
death_sound_factor = 1.0

# colour scheme, #446482, #70a5d7, #18232d

class player:

    def __init__(self):
        super().__init__()
        self.speed_mult = 1.0

        self.rect = pygame.Rect(100, 100, 50, 100)
        self.x_speed = 0
        self.gravity = 0
        self.last_press = 0
        self.grounded = False
        self.colour = ('#47602d')
        # rock
        self.rock_rect = pygame.Rect(0, 0, 50, 35)
        self.rock_grav = 0

    def input(self):
        global gravity_direction
        global level
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_a]:
            self.x_speed = max(-30 * self.speed_mult, self.x_speed - 1 * self.speed_mult)
        if keys[pygame.K_d]:
            self.x_speed = min(30 * self.speed_mult, self.x_speed + 1 * self.speed_mult)
        # if keys[pygame.K_SPACE] and current_time - self.last_press > 200 and self.grounded:
        #    gravity_direction = not gravity_direction
        #    self.last_press = current_time
        #    self.grounded = False
        if keys[pygame.K_SPACE] and current_time - self.last_press > 150:
            gravity_direction = not gravity_direction
            self.last_press = current_time
            self.grounded = False
            # play_sound("switch_gravity")
        if keys[pygame.K_t]:
            level = test_level
            reset_rects()
            timer(True)
        if keys[pygame.K_r]:
            level = 0
            reset_rects()
            timer(True)
        if keys[pygame.K_p]:
            print(self.x_speed)

    def movement(self):
        global gravity_direction
        # left and right
        self.rect.x += self.x_speed
        if self.x_speed >= 0: self.x_speed -= 0.5 * self.speed_mult
        if self.x_speed < 0: self.x_speed += 0.5 * self.speed_mult
        # gravity
        if gravity_direction:
            self.gravity += 1
        else:
            self.gravity -= 1
        self.rect.y += self.gravity

    def rock(self):
        self.rock_rect.y += self.rock_grav
        self.rock_rect.x += self.x_speed

        if gravity_direction:
            self.rock_grav += 0.5
        else:
            self.rock_grav -= 0.5

        if self.rock_rect.top <= self.rect.top - 10:
            self.rock_rect.top = self.rect.top - 8
            self.rock_grav = 0
        elif self.rock_rect.bottom >= self.rect.bottom + 10:
            self.rock_rect.bottom = self.rect.bottom + 8
            self.rock_grav = 0
        if self.rock_rect.left < self.rect.left - 10:
            self.rock_rect.left = self.rect.left - 10
        if self.rock_rect.right > self.rect.right + 10:
            self.rock_rect.right = self.rect.right + 10

    def screen_side_check(self):
        # side of the screen colisions
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
        self.rock()

    def draw(self, scroll):
        drawing_rect = pygame.Rect(self.rect.left - scroll[0], self.rect.top - scroll[1],self.rect.width,self.rect.height)
        drawing_rock_rect = pygame.Rect(self.rock_rect.left - scroll[0], self.rock_rect.top - scroll[1],self.rock_rect.width,self.rock_rect.height)
        
        pygame.draw.rect(screen, self.colour, drawing_rect)
        pygame.draw.line(screen, self.colour, drawing_rect.midright,  drawing_rock_rect.midright , 10)
        pygame.draw.line(screen, self.colour, drawing_rect.midleft,  drawing_rock_rect.midleft, 10)
        pygame.draw.rect(screen, ('#747b81'), drawing_rock_rect )


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


def game_funciton(scroll):
    global level
    global gravity_direction
    global num_list
    global button_clicks
    for pos, num in enumerate(num_list):
        rect = pygame.Rect(0, 0, 100, 100)
        
        rect.top = 100*(pos // 12)
        rect.left = 100*(pos % 12)
        
        if num == 0:
            pygame.draw.rect(screen, ("#70a5d7"), pygame.Rect(rect.left - scroll[0], rect.top - scroll[1],rect.width,rect.height))

        elif num == 1:
            pygame.draw.rect(screen, ("#446482"), pygame.Rect(rect.left - scroll[0], rect.top - scroll[1],rect.width,rect.height))
            colisions(rect)

        elif num == 2:
            pygame.draw.rect(screen, ("#bea925"), pygame.Rect(rect.left - scroll[0], rect.top - scroll[1],rect.width,rect.height))
            lava_hitbox_rect.center = rect.center
            if show_hitboxes:
                pygame.draw.rect(screen, ("#000000"), lava_hitbox_rect)#fix
            if lava_hitbox_rect.colliderect(player_class.rect):
                player_class.rect.topleft = 0, 0
                player_class.gravity = 0
                reset_rects()
                print(f"death at {timer(False)}")
                play_sound("death")
                break
        elif num in (3, 4, 5, 6):
            pygame.draw.rect(screen, ("#70a5d7"), pygame.Rect(rect.left - scroll[0], rect.top - scroll[1],rect.width,rect.height))
            rect = create_button(num, rect)
            pygame.draw.rect(screen, ("#824464"), pygame.Rect(rect.left - scroll[0], rect.top - scroll[1],rect.width,rect.height))
            if rect.colliderect(player_class.rect):
                button_clicks += 1
                reset_rects(True)
                print(f"button {button_clicks} hit at {timer(False)} in level {level}")
                play_sound("button_hit")
        elif num == 9:
            pygame.draw.rect(screen, ('#6c25be'), pygame.Rect(rect.left - scroll[0], rect.top - scroll[1],rect.width,rect.height))
            if rect.colliderect(player_class.rect):
                print(f"level: {level} time: {timer(False)}")
                level += 1
                button_clicks = 0
                reset_rects()
                play_sound("finish_level")
                break
        else:
            print("something wrong")

        # button


def create_button(b_type, rect):
    # button(b_type) directions:
    #  3
    # 6   4
    #  5
    if b_type == 3 or b_type == 5:
        rect.size = (b_long, b_short)
        if b_type == 5:
            rect.top += 100 - b_short
        rect.left += (100 - b_long) / 2
    else:
        rect.size = (b_short, b_long)
        if b_type == 4:
            rect.left += 100 - b_short
        rect.top += (100 - b_long) / 2
    return rect


def reset_rects(button=False):
    global ground_rect
    global sky_rect
    global end_rect
    global lava_rect
    global lava_hitbox_rect
    global player_class
    global button_rect
    global gravity_direction
    global num_list
    global button_clicks
    ground_rect = pygame.Rect(-100, 0, 100, 100)
    sky_rect = pygame.Rect(-100, 0, 100, 100)
    end_rect = pygame.Rect(-100, 0, 100, 100)
    lava_rect = pygame.Rect(-100, 0, 100, 100)
    lava_hitbox_rect.center = (-100, 0)
    button_rect.center = (-100, -100)
    button_rect = pygame.Rect(-100, 0, 100, 100)
    if button == False:
        gravity_direction = False
        player_class.rect.topleft = (50, 0)
        player_class.gravity = 0
        player_class.rock_rect.midtop = player_class.rect.midtop
        button_clicks = 0

    num_list = level_picker(level, button_clicks)


def timer(reset):
    global last_run_time
    current_time = pygame.time.get_ticks()
    if reset:
        last_run_time = current_time
    run_time = float((current_time - last_run_time) / 1000)
    score_display = font.render(f"{run_time}", False, ("#8f5a28"))
    score_rect = score_display.get_rect(midtop=(600, 0))
    screen.blit(score_display, score_rect)
    return run_time

def play_sound(name):
    # pygame.mixer.music.stop()
    pygame.mixer.Sound.play(sounds[name])
    # pygame.mixer.Sound.play(pygame.mixer.Sound(f"sounds/{name}.wav"))

def camera(scroll):
    scroll[0] += (player_class.rect.centerx- screen.get_width() / 2- scroll[0]) /2
    scroll[1] += (player_class.rect.centery- screen.get_height() / 2- scroll[1]) /2
    return [int(scroll[0]), int(scroll[1])]


reset_rects()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill(("#446482"))
    if level >= 18:
        scroll = camera(scroll)
    player_class.update()
    game_funciton(scroll)
    player_class.draw(scroll)
    timer(False)

    pygame.display.update()
    clock.tick(60)
