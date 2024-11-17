# V1.9.1
# 2 Player mode
import os
import random
import time
import typing
import threading

start = time.time()

SHOW_HITBOXES = False
SFX = False
ROCK_SFX = False
MUSIC = True
MAX_SPEED = True
FRAMES_TIMER = True
TEST_STUFF = False
FULLSCREEN = False  # slow start up

import pygame
from Levels import level_picker
from level_editor import Level_editor

pygame.init()
pygame.mixer.init()

big_display = pygame.Surface((2400, 1200))

if FULLSCREEN:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((1200, 600))

pygame.display.set_caption("platformer")
clock = pygame.time.Clock()
current_time = pygame.time.get_ticks()
scroll = [0, 0]
rect_list = []

num_list = []
level = 18
game_on = True

TEST_LEVEL = 30

players = 2
player_classes = []
players_color_schemes = ['#47602d', '#cb3333']
players_input_mapping = {0: [pygame.K_a, pygame.K_d, pygame.K_SPACE],
                         1: [pygame.K_b, pygame.K_m, pygame.K_n],}

gravity_directions = []

for _ in range(players):
    gravity_directions.append(True)

stone_slide: typing.Union[None, pygame.mixer.Sound] = None

if ROCK_SFX and not SFX:
    raise ValueError('rock_sound_effects can only be enabled with the other sound effects (sound_effects)')

if SFX:
    sounds = {}
    for sound in os.listdir("assets/sounds"):
        if sound == 'stone_slide.wav':
            continue

        sounds[sound.split('.')[0]] = pygame.mixer.Sound(f"assets/sounds/{sound}")
    if ROCK_SFX:
        def load_stone_slide():
            global stone_slide
            stone_slide = pygame.mixer.Sound("assets/sounds/stone_slide.wav")


        load_stone_slide_thread = threading.Thread(name='load_stone_slide_thread', target=load_stone_slide)
        load_stone_slide_thread.start()

if MUSIC:
    musics = []
    for music in os.listdir('assets/music'):
        musics.append(f'assets/music/{music}')
    random.shuffle(musics)

    pygame.mixer.music.load(musics[0])
    for music in musics[1:]:
        pygame.mixer.music.queue(music)
    pygame.mixer.music.play(loops=-1)

font = pygame.font.Font(("assets/Pixeltype.ttf"), 50)
big_font = pygame.font.Font(("assets/Pixeltype.ttf"), 100)
bigger_font = pygame.font.Font(("assets/Pixeltype.ttf"), 300)

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

total_frames = 0
death_counter = 0


# colour scheme, #446482, #70a5d7, #18232d

class player:

    def __init__(self, player_index: int):
        super().__init__()

        self.player_index = player_index

        self.speed_mult = 1.0

        self.rect = pygame.Rect(100, 100, 50, 100)
        self.x_speed = 0
        self.gravity = 0

        self.last_press = 0
        self.last_KeyB = 0

        self.grounded = False
        self.colour = players_color_schemes[self.player_index]
        # rock
        self.rock_rect = pygame.Rect(0, 0, 50, 35)
        self.rock_grav = 0

        self.walk_delay = 0
        self.slide_state = False

    def input(self):
        global gravity_directions
        global level

        global button_clicks
        global total_frames
        keys = pygame.key.get_pressed()
        # current_time = pygame.time.get_ticks()
        if keys[players_input_mapping[self.player_index][0]]:
            if MAX_SPEED:
                self.x_speed = max(-30 * self.speed_mult, self.x_speed - 1 * self.speed_mult)
            else:
                self.x_speed = self.x_speed - 1 * self.speed_mult
        if keys[players_input_mapping[self.player_index][1]]:
            if MAX_SPEED:
                self.x_speed = min(30 * self.speed_mult, self.x_speed + 1 * self.speed_mult)
            else:
                self.x_speed = self.x_speed + 1 * self.speed_mult
            # print(self.x_speed)
        if keys[players_input_mapping[self.player_index][2]] and total_frames - self.last_press > 9:
            gravity_directions[self.player_index] = not gravity_directions[self.player_index]
            self.last_press = total_frames
            self.grounded = False
            # play_sound("switch_gravity")
        if TEST_STUFF:
            if keys[pygame.K_t]:
                level = TEST_LEVEL
                reset_rects()
                timer(True)
            if keys[pygame.K_b] and total_frames > self.last_KeyB + 10:
                self.last_KeyB = total_frames
                button_clicks += 1
                reset_rects(True)
                print(button_clicks)
            if keys[pygame.K_z]:
                self.rect.y = -700
        if keys[pygame.K_r]:
            level = 0
            reset_rects()
            timer(True)
        if keys[pygame.K_l]:
            last_KeyB = Level_editor()
            last_KeyB.update()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()

    def movement(self):
        global gravity_directions
        # left and right
        self.rect.x += round(self.x_speed)
        if self.x_speed >= 0: self.x_speed -= 0.5 * self.speed_mult
        if self.x_speed < 0: self.x_speed += 0.5 * self.speed_mult
        colisions(self, rect_list, False)

        # gravity
        if gravity_directions[self.player_index]:
            self.gravity += 1
        else:
            self.gravity -= 1
        self.rect.y += self.gravity
        colisions(self, rect_list, True)

    def rock(self):
        self.rock_rect.y += self.rock_grav
        self.rock_rect.x += self.x_speed

        if abs(self.rock_grav) > 2:
            if ROCK_SFX and not self.slide_state and stone_slide is not None:
                stone_slide.play()
                self.slide_state = True
        else:
            if ROCK_SFX and self.slide_state and stone_slide is not None:
                stone_slide.stop()
                self.slide_state = False

        if gravity_directions[self.player_index]:
            self.rock_grav += 0.5
        else:
            self.rock_grav -= 0.5

        if self.rock_rect.top <= self.rect.top - 10:
            self.rock_rect.top = self.rect.top - 8
            if abs(self.rock_grav) > 2 and ROCK_SFX:
                play_sound('rock')
            self.rock_grav = 0
        elif self.rock_rect.bottom >= self.rect.bottom + 10:
            self.rock_rect.bottom = self.rect.bottom + 8
            if abs(self.rock_grav) > 2 and ROCK_SFX:
                play_sound('rock')
            self.rock_grav = 0
        if self.rock_rect.left < self.rect.left - 10:
            self.rock_rect.left = self.rect.left - 10
        if self.rock_rect.right > self.rect.right + 10:
            self.rock_rect.right = self.rect.right + 10

    def screen_side_check(self):
        # side of the screen colisions
        if level != 30:
            if self.rect.top <= 0:
                self.rect.top = 0
                self.gravity = 0

        if self.rect.left <= 0:
            self.rect.left = 0
            self.x_speed = 0

        if level <= 22:
            if self.rect.right >= 1200:
                self.rect.right = 1200
                self.x_speed = 0

            if self.rect.bottom >= 600:
                self.rect.bottom = 600
                self.gravity = 0

    def update(self):
        self.input()
        self.movement()
        self.screen_side_check()
        self.rock()

    def draw(self, scroll):
        drawing_rect = pygame.Rect(self.rect.left - scroll[0], self.rect.top - scroll[1], self.rect.width,
                                   self.rect.height)
        drawing_rock_rect = pygame.Rect(self.rock_rect.left - scroll[0], self.rock_rect.top - scroll[1],
                                        self.rock_rect.width, self.rock_rect.height)

        pygame.draw.rect(big_display, self.colour, drawing_rect)
        pygame.draw.line(big_display, self.colour, drawing_rect.midright, drawing_rock_rect.midright, 10)
        pygame.draw.line(big_display, self.colour, drawing_rect.midleft, drawing_rock_rect.midleft, 10)
        pygame.draw.rect(big_display, ('#747b81'), drawing_rock_rect)


for n in range(players):
    player_classes.append(player(n))


def colision_side_check(player_class, rect):
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


def colisions(player_class, rect_list, allow_vertical):
    for rect in rect_list:
        if rect.colliderect(player_class.rect):
            collision_side = colision_side_check(_, rect)
            # if collision_side is not None:
            #     print(collision_side)

            if allow_vertical:
                if collision_side == "bottom":
                    player_class.rect.bottom = rect.top
                    player_class.gravity = 0
                    player_class.grounded = True

                if collision_side == "top":
                    player_class.rect.top = rect.bottom
                    player_class.gravity = 0
                    player_class.grounded = True

            if not allow_vertical:
                if collision_side == "left":
                    player_class.rect.left = rect.right
                    player_class.x_speed = 0

                if collision_side == "right":
                    player_class.rect.right = rect.left
                    player_class.x_speed = 0


def game_funciton(scroll):
    global level
    global num_list
    global button_clicks
    global rect_list
    global death_counter
    rect_list = []
    x = 0
    y = 0
    for num in num_list:
        rect = pygame.Rect(0, 0, 100, 100)

        rect.topleft = (x, y)
        x += 100
        # if  100 < rect.centerx - scroll[0] < 2500 and 100 < rect.centery - scroll[1] < 1100:
        if -50 < rect.centerx - scroll[0] < 2650 and -50 < rect.centery - scroll[1] < 1250:  # optimization?
            if num == 0:
                pygame.draw.rect(big_display, ("#70a5d7"),
                                 pygame.Rect(rect.left - scroll[0], rect.top - scroll[1], rect.width, rect.height))

            elif num == 1:
                pygame.draw.rect(big_display, ("#446482"),
                                 pygame.Rect(rect.left - scroll[0], rect.top - scroll[1], rect.width, rect.height))
                rect_list.append(rect)

            elif num == 2:
                pygame.draw.rect(big_display, ("#bea925"),
                                 pygame.Rect(rect.left - scroll[0], rect.top - scroll[1], rect.width, rect.height))
                lava_hitbox_rect.center = rect.center
                if SHOW_HITBOXES:
                    pygame.draw.rect(big_display, ("#000000"),
                                     pygame.Rect(lava_hitbox_rect.left - scroll[0], lava_hitbox_rect.top - scroll[1],
                                                 lava_hitbox_rect.width, lava_hitbox_rect.height))  # fix

                for _ in player_classes:
                    if lava_hitbox_rect.colliderect(_.rect):
                        _.rect.topleft = 0, 0
                        _.gravity = 0
                        reset_rects()
                        print(f"death at {timer(False)}")
                        death_counter += 1
                        if SFX:
                            play_sound("death")

                        break
            elif num in (3, 4, 5, 6):
                pygame.draw.rect(big_display, ("#70a5d7"),
                                 pygame.Rect(rect.left - scroll[0], rect.top - scroll[1], rect.width, rect.height))
                rect = create_button(num, rect)
                pygame.draw.rect(big_display, ("#824464"),
                                 pygame.Rect(rect.left - scroll[0], rect.top - scroll[1], rect.width, rect.height))
                for _ in player_classes:
                    if rect.colliderect(_.rect):
                        button_clicks += 1
                        reset_rects(True)
                        print(f"button {button_clicks} hit at {timer(False)} in level {level}")
                        if SFX:
                            play_sound("button_hit")
        if num == 8:
            for _ in player_classes:
                if _.rect.colliderect(rect):
                    _.rect.right = rect.left
            y += 100
            x = 0
        elif num == 9:
            pygame.draw.rect(big_display, ('#6c25be'),
                             pygame.Rect(rect.left - scroll[0], rect.top - scroll[1], rect.width, rect.height))
            for _ in player_classes:
                if rect.colliderect(_.rect):
                    print(f"level: {level} time: {timer(False)}")
                    level += 1
                    button_clicks = 0
                    reset_rects()
                    if SFX:
                        play_sound("finish_level")
                    # break
        if num not in (0, 1, 2, 3, 4, 5, 6, 8, 9):
            print("something wrong")
            print(num, scroll, rect.center)

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
    global player_classes
    global button_rect
    global gravity_directions
    global num_list
    global button_clicks
    global scroll
    ground_rect = pygame.Rect(-100, 0, 100, 100)
    sky_rect = pygame.Rect(-100, 0, 100, 100)
    end_rect = pygame.Rect(-100, 0, 100, 100)
    lava_rect = pygame.Rect(-100, 0, 100, 100)
    lava_hitbox_rect.center = (-100, 0)
    button_rect.center = (-100, -100)
    button_rect = pygame.Rect(-100, 0, 100, 100)
    if button == False:
        for _ in player_classes:
            gravity_directions[_.player_index] = False
        if level == 30:
            for _ in player_classes:
                _.rect.topleft = (0, 3100)
        else:
            for _ in player_classes:
                _.rect.topleft = (50, 0)
        for _ in player_classes:
            _.gravity = 0
            _.rock_rect.midtop = _.rect.midtop
        button_clicks = 0
        scroll = [0, 0]

    num_list = level_picker(level, button_clicks)


last_run_time = 0
frames_timer = 0


def timer(reset):
    global last_run_time
    global frames_timer

    if FRAMES_TIMER:
        frames_timer += 1
        run_time = frames_timer
        if reset:
            frames_timer = 0
    else:
        current_time = pygame.time.get_ticks()
        if reset:
            last_run_time = current_time
        run_time = float((current_time - last_run_time) / 1000)

    if level > 22:
        score_display = big_font.render(f"{run_time}", False, ("#8f5a28"))
        score_rect = score_display.get_rect(midtop=big_display.get_rect().midtop)
    else:
        score_display = font.render(f"{run_time}", False, ("#8f5a28"))
        score_rect = score_display.get_rect(midtop=(600, 0))

    # screen.blit(font.render(str(clock.get_fps()), False, (255, 255, 255)), (0, 0))

    big_display.blit(score_display, score_rect)
    return run_time


def play_sound(name):
    # pygame.mixer.music.stop()
    pygame.mixer.Sound.play(sounds[name])
    # pygame.mixer.Sound.play(pygame.mixer.Sound(f"sounds/{name}.wav"))


def camera(scroll):
    scroll[0] += (player_classes[0].rect.centerx - big_display.get_width() / 2 - scroll[0]) / 2
    scroll[1] += (player_classes[0].rect.centery - big_display.get_height() / 2 - scroll[1]) / 2
    return [int(scroll[0]), int(scroll[1])]


first = True


def ending(scroll):
    global first
    global clouds
    global end_timer
    global expl_size
    global rock_pos_y
    global multp
    global resize
    global game_time
    global death_counter

    pygame.draw.rect(big_display, ("#70a5d7"), pygame.Rect(0 - scroll[0], -1300 - scroll[1], 3000, 1400))

    if player_classes[0].rect.centery < -600 and first:
        end_timer = 0
        rock_pos_y = 1300
        game_time = timer(False)
        expl_size = 0
        multp = 1

        clouds = []
        for i in range(25):
            x = random.randint(0, 2400)
            y = random.randint(-1450, 50)
            clouds.append([x, y, random.randint(1, 5)])

        first = False

        def resize(rect, expl_size):
            rect.size = [expl_size, expl_size]
            rect.center = pygame.Rect(1425, rock_pos_y, 50 * multp, 35 * multp).center
            return rect
    elif first == False:
        big_display.fill("#70a5d7")
        end_timer += 1
        for i in clouds:
            pygame.draw.rect(big_display, ("white"), pygame.Rect(i[0], i[1], 300, 150))
            i[1] += 20 / i[2]
            if i[1] > 2600:
                i[1] = -150
                i[0] = random.randint(0, 2400)

        pygame.draw.rect(big_display, ('#47602d'), pygame.Rect(800 - 25 * multp, 450, 50 * multp, 100 * multp))
        if end_timer < 80:
            multp = end_timer / 40 + 1

        # rock_stuf
        if end_timer < 450:
            pygame.draw.rect(big_display, ('#747b81'), pygame.Rect(1425, rock_pos_y, 50 * multp, 35 * multp))

        # if 400 < end_timer and  end_timer < 406:
        #     if SFX or MUSIC:
        #         play_sound("death")
        if end_timer > 80 and end_timer < 450:
            rock_pos_y += (200 - rock_pos_y) / 120
            print((900 - rock_pos_y) / 60)
        elif 400 < end_timer and end_timer < 600:
            rect = pygame.Rect(0, 0, expl_size, expl_size)

            expl_size = (end_timer - 400) * 5
            rect = resize(rect, expl_size)
            pygame.draw.rect(big_display, ('#e20404'), rect)

            expl_size = (end_timer - 420) * 5
            rect = resize(rect, expl_size)
            pygame.draw.rect(big_display, ('#fb9304'), rect)

            expl_size = (end_timer - 450) * 5
            rect = resize(rect, expl_size)
            pygame.draw.rect(big_display, ('#fbea04'), rect)
        if end_timer > 500:
            score_display = bigger_font.render(f"PLATFORMER", False, ("#fba904"))
            score_rect = score_display.get_rect(midtop=(600, 0))
            big_display.blit(score_display, score_rect)
            if FRAMES_TIMER:
                score_display = bigger_font.render(f"Frames : {game_time}", False, ("#fba904"))
                score_rect = score_display.get_rect(midtop=(600, 400))
                big_display.blit(score_display, score_rect)

                score_display = bigger_font.render(f"Seconds : {game_time // 60}", False, ("#fba904"))
                score_rect = score_display.get_rect(midtop=(600, 700))
                big_display.blit(score_display, score_rect)
            else:
                score_display = bigger_font.render(f"Seconds : {game_time}", False, ("#fba904"))
                score_rect = score_display.get_rect(midtop=(600, 400))
                big_display.blit(score_display, score_rect)

            score_display = bigger_font.render(f"deaths : {death_counter}", False, ("#fba904"))
            score_rect = score_display.get_rect(midtop=(600, 1000))
            big_display.blit(score_display, score_rect)


print(f'loading took: {time.time() - start}')

reset_rects()
while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if level > 22 and FULLSCREEN:
        if screen.get_width() < 2400 or screen.get_height() < 1200:
            if big_display.get_size() != (2400, 1200):
                big_display = pygame.Surface((2400, 1200))
        else:
            if big_display.get_size() != screen.get_size():
                big_display = pygame.Surface(screen.get_size())
                # print(f'[DEBUG] resized big_display to {big_display.get_size()}')

    screen.fill(("#446482"))
    big_display.fill(("#446482"))

    if level > 22:
        scroll = camera(scroll)

    for _ in player_classes:
        _.update()

    game_funciton(scroll)

    for _ in player_classes:
        _.draw(scroll)

    timer(False)

    if level == 30:
        ending(scroll)

    if level > 22:
        if FULLSCREEN and screen.get_width() > big_display.get_width() and screen.get_height() > big_display.get_height():
            scaled = big_display
        else:
            # 1200 / 600 = 2
            height = min(screen.get_height(), screen.get_width() // 2)
            width = height * 2

            scaled = pygame.transform.scale(big_display, (width, height))

        dest = tuple(map(lambda a, b: a - b, screen.get_rect().center, scaled.get_rect().center))
        screen.blit(scaled, dest)
    else:
        dest = tuple(map(lambda a, b: a - b, screen.get_rect().center, (1200 // 2, 600 // 2)))
        screen.blit(big_display, dest)

    pygame.display.update()
    clock.tick(60)

    if MUSIC:
        if frames_timer == 3600 * 10:  # 36000
            pygame.mixer.music.load('assets/🤡.mp3')
            pygame.mixer.music.play(-1)

    total_frames += 1