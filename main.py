# V1.9.1c4

SHOW_HITBOXES = False
MAX_SPEED = True
FRAMES_TIMER = True

import pygame
from Levels import level_picker

pygame.init()
pygame.mixer.init()

big_display = pygame.Surface((2400, 1200))
screen = pygame.display.set_mode((1200, 600))

pygame.display.set_caption("platformer")
clock = pygame.time.Clock()
current_time = pygame.time.get_ticks()
scroll = [0, 0]
rect_list = []

gravity_direction = True
num_list = []
level = 29

ground_rect = pygame.Rect(-100, 0, 100, 100)
sky_rect = pygame.Rect(-100, 0, 100, 100)
end_rect = pygame.Rect(-100, 0, 100, 100)
lava_rect = pygame.Rect(-100, 0, 100, 100)
lava_hitbox_rect = pygame.Rect(-100, 0, 50, 50)
# button
button_rect = pygame.Rect(0, 0, 0, 0)
b_long = 80
b_short = 35
button_clicks = 0

total_frames = 0


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

    def input(self):
        global gravity_direction
        global level

        global button_clicks
        global total_frames
        keys = pygame.key.get_pressed()
        # current_time = pygame.time.get_ticks()
        if keys[pygame.K_a]:
            self.x_speed = max(-30 * self.speed_mult, self.x_speed - 1 * self.speed_mult)
        if keys[pygame.K_d]:
            self.x_speed = min(30 * self.speed_mult, self.x_speed + 1 * self.speed_mult)
        if keys[pygame.K_SPACE] and total_frames - self.last_press > 9:
            gravity_direction = not gravity_direction
            self.last_press = total_frames
            self.grounded = False
            # play_sound("switch_gravity")
        if keys[pygame.K_r]:
            level = 0
            reset_rects()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()

    def movement(self):
        global gravity_direction
        # left and right
        self.rect.x += round(self.x_speed)
        if self.x_speed >= 0: self.x_speed -= 0.5 * self.speed_mult
        if self.x_speed < 0: self.x_speed += 0.5 * self.speed_mult
        colisions(rect_list, False)

        # gravity
        if gravity_direction:
            self.gravity += 1
        else:
            self.gravity -= 1
        self.rect.y += self.gravity
        colisions(rect_list, True)

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

    def draw(self, scroll):
        drawing_rect = pygame.Rect(self.rect.left - scroll[0], self.rect.top - scroll[1], self.rect.width,
                                   self.rect.height)

        pygame.draw.rect(big_display, self.colour, drawing_rect)


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


def colisions(rect_list, allow_vertical):
    for rect in rect_list:
        if rect.colliderect(player_class.rect):
            collision_side = colision_side_check(rect)
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
    global gravity_direction
    global num_list
    global button_clicks
    global rect_list

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
                if lava_hitbox_rect.colliderect(player_class.rect):
                    player_class.rect.topleft = 0, 0
                    player_class.gravity = 0
                    reset_rects()

                    break
            elif num in (3, 4, 5, 6):
                pygame.draw.rect(big_display, ("#70a5d7"),
                                 pygame.Rect(rect.left - scroll[0], rect.top - scroll[1], rect.width, rect.height))
                rect = create_button(num, rect)
                pygame.draw.rect(big_display, ("#824464"),
                                 pygame.Rect(rect.left - scroll[0], rect.top - scroll[1], rect.width, rect.height))
                if rect.colliderect(player_class.rect):
                    button_clicks += 1
                    reset_rects(True)
        if num == 8:
            if player_class.rect.colliderect(rect):
                player_class.rect.right = rect.left
            y += 100
            x = 0
        elif num == 9:
            pygame.draw.rect(big_display, ('#6c25be'),
                             pygame.Rect(rect.left - scroll[0], rect.top - scroll[1], rect.width, rect.height))
            if rect.colliderect(player_class.rect):
                level += 1
                button_clicks = 0
                reset_rects()
                break
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
    global player_class
    global button_rect
    global gravity_direction
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
        gravity_direction = False
        if level == 30:
            player_class.rect.topleft = (0, 3100)
        else:
            player_class.rect.topleft = (50, 0)
        player_class.gravity = 0
        button_clicks = 0
        scroll = [0, 0]

    num_list = level_picker(level, button_clicks)

def camera(scroll):
    scroll[0] += (player_class.rect.centerx - big_display.get_width() / 2 - scroll[0]) / 2
    scroll[1] += (player_class.rect.centery - big_display.get_height() / 2 - scroll[1]) / 2
    return [int(scroll[0]), int(scroll[1])]

reset_rects()
while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill(("#446482"))
    big_display.fill(("#446482"))

    if level > 22:
        scroll = camera(scroll)
    player_class.update()
    game_funciton(scroll)
    player_class.draw(scroll)

    if level > 22:

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

    total_frames += 1