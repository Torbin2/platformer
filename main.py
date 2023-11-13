import pygame
from sys import exit
import tas

pygame.init()
screen = pygame.display.set_mode((1400, 600))
pygame.display.set_caption("platformer")
clock = pygame.time.Clock()

frame = 0
frame_advance = True
frame_saves = []

loading_savestate = "false"

clock_speed = 60

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
last_run_time = 0

font = pygame.font.Font(("font/Pixeltype.ttf"), 50)
times_new_roman = pygame.font.SysFont('times new roman', 20)

ground_rect = pygame.Rect(-100, 0, 100, 100)
sky_rect = pygame.Rect(-100, 0, 100, 100)
end_rect = pygame.Rect(-100, 0, 100, 100)
lava_rect = pygame.Rect(-100, 0, 100, 100)
lava_hitbox_rect = pygame.Rect(-100, 0, 75, 75)


# colour scheme, #446482, #70a5d7, #18232d

def reinitialize():

    global clock, frame, gravity_direction, num_list, level, game_on, last_run_time, player_class, events, physics

    clock = pygame.time.Clock()

    frame = 0

    gravity_direction = True
    num_list = []
    level = 1
    game_on = True
    last_run_time = 0
    player_class = player()

    reset_rects()
    level_picker()
    events = []
    physics = True


class player:

    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(100, 100, 50, 100)
        self.x_speed = 0
        self.gravity = 0
        self.last_press = 0
        self.grounded = False

    def input(self):
        global gravity_direction
        global level
        global frame
        global physics
        global loading_savestate
        global frame_advance
        global clock_speed
        global keys
        # current_time = pygame.time.get_ticks()

        print("upo", frame)

        if (movie.mode != "read" and loading_savestate != "true" and keys[pygame.K_a]) or (movie.mode == "read" and movie.inputs[frame].a) or (movie.mode == "write" and loading_savestate == "true" and movie.inputs[frame].a):
            self.x_speed -= 1
        if (movie.mode != "read" and loading_savestate != "true" and keys[pygame.K_d]) or (movie.mode == "read" and movie.inputs[frame].d) or (movie.mode == "write" and loading_savestate == "true" and movie.inputs[frame].d):
            self.x_speed += 1
        if ((movie.mode != "read" and loading_savestate != "true" and keys[pygame.K_SPACE]) or (movie.mode == "read" and movie.inputs[frame].s) or (movie.mode == "write" and loading_savestate == "true" and movie.inputs[frame].s)) and frame - self.last_press > 12 and self.grounded:
            gravity_direction = not gravity_direction
            self.last_press = frame
            self.grounded = False
        # if keys[pygame.K_SPACE] and current_time - self.last_press > 200:
        #     gravity_direction = not gravity_direction
        #     self.last_press = current_time
        #     self.grounded = False
        if (movie.mode != "read" and loading_savestate != "true" and keys[pygame.K_t]) or (movie.mode == "read" and movie.inputs[frame].t) or (movie.mode == "write" and loading_savestate == "true" and movie.inputs[frame].t):
            level = 999
            reset_rects()
            level_picker()
        if (movie.mode != "read" and loading_savestate != "true" and keys[pygame.K_r]) or (movie.mode == "read" and movie.inputs[frame].r) or (movie.mode == "write" and loading_savestate == "true" and movie.inputs[frame].r):
            level = 1
            reset_rects()
            level_picker()
            timer(True)

        if physics:

            if movie.mode == "write":

                if loading_savestate == "true":

                    frame_advance = False

                    if frame >= movie.inputs.__len__() - 1:
                        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")

                        clock_speed = 60
                        # player_class.draw()
                        # pygame.display.update()
                        frame_advance = True
                        loading_savestate = "false"

                        frame += 1
                        return
                    else:

                        print("crashed?", frame, "leng", len(movie.inputs))

                        print("reading: ",
                              movie.inputs[frame].a,
                              movie.inputs[frame].d,
                              movie.inputs[frame].s,
                              movie.inputs[frame].r,
                              movie.inputs[frame].t, "at frame", frame)

                else:
                    movie.write_input([keys[pygame.K_a],
                                       keys[pygame.K_d],
                                       keys[pygame.K_SPACE],
                                       keys[pygame.K_r],
                                       keys[pygame.K_t]])
            elif movie.mode == "read":
                print(movie.inputs[frame].a,
                      movie.inputs[frame].d,
                      movie.inputs[frame].s,
                      movie.inputs[frame].r,
                      movie.inputs[frame].t)

        frame += 1

    def movement(self):
        global gravity_direction
        # left and right
        self.rect.x += self.x_speed
        if self.x_speed >= 0: self.x_speed -= 0.5
        if self.x_speed < 0: self.x_speed += 0.5
        # gravity
        if gravity_direction:
            self.gravity += 1
        else:
            self.gravity -= 1
        self.rect.y += self.gravity

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

    def draw(self):
        pygame.draw.rect(screen, ('#18232d'), self.rect)

        if not gravity_direction:
            pygame.draw.rect(screen, (255, 255, 255), self.rect.topleft + (self.rect.width, self.rect.height // 4))
        else:
            pygame.draw.rect(screen, (255, 255, 255),
                             (self.rect.bottomleft[0], self.rect.bottomleft[1] - self.rect.height // 4, self.rect.width, self.rect.height // 4))

    def save(self) -> dict:
        return {
            'level': level,
            'x': self.rect.x,
            'y': self.rect.y,
            'xv': self.x_speed,
            'yv': self.gravity,
            'direction': gravity_direction,
            'ground': self.grounded,
            'last_press': self.last_press,
            'frame': frame
        }

    def load(self, raw: dict):
        global gravity_direction, level, frame
        level = raw['level']
        level_picker()
        self.rect.x = raw['x']
        self.rect.y = raw['y']
        self.x_speed = raw['xv']
        self.gravity = raw['yv']
        gravity_direction = raw['direction']
        self.grounded = raw['ground']
        self.last_press = raw['last_press']
        frame = raw['frame']


player_class = player()


def colision_side_check(rect):
    delta_x = rect.centerx - player_class.rect.centerx
    delta_y = rect.centery - player_class.rect.centery

    abs_delta_x = abs(delta_x)
    abs_delta_y = abs(delta_y)

    pygame.draw.line(screen, (255, 0, 0), rect.bottomleft, rect.topright, 25 // 2)

    if abs(abs_delta_x - abs_delta_y) < 25:
        return

    pygame.draw.rect(screen, (255, 0, 0), rect, 1)

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
            y_pos += 1
        pos -= (y_pos * 12) - 12

        rect.top = (y_pos * 100) - 100
        rect.left = pos * 100

        if rect == ground_rect:
            pygame.draw.rect(screen, ("#446482"), rect)
            colisions(rect)
        if rect == sky_rect:
            pygame.draw.rect(screen, ("#70a5d7"), rect)
        if rect == end_rect:
            pygame.draw.rect(screen, ('#6c25be'), rect)
            if end_rect.colliderect(player_class.rect):
                print(f"level: {level} time: {timer(False)}")
                level += 1
                reset_rects()
                level_picker()
        if rect == lava_rect:
            pygame.draw.rect(screen, ("#bea925"), rect)
            lava_hitbox_rect.center = rect.center
            if lava_hitbox_rect.colliderect(player_class.rect):
                player_class.rect.topleft = 0, 0
                player_class.gravity = 0
                gravity_direction = False
                # level = 1
                # i = rect.x // 100 % 12 + rect.y // 100 * 12
                # reset_rects()
                # level_picker()
                # timer(True)
                # print("death")
                # if i >= len(num_list):
                #     i = len(num_list) - 1
                # if i < 0:
                #     i = 0
                # num_list[i] = 2


def level_picker():
    global num_list
    if level == 1:
        num_list = [0, 0, 0, 0, 0, 9, 9, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if level == 2:
        num_list = [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 9
            , 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1
            , 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0
            , 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0
            , 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0
            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if level == 3:
        num_list = [0, 1, 9, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                    0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
                    0, 1, 0, 0, 0, 0, 0, 9, 1, 0, 0, 1,
                    0, 1, 9, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    if level == 4:
        num_list = [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 9,
                    0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0,
                    1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0,
                    1, 1, 2, 0, 0, 0, 1, 0, 0, 1, 1, 1,
                    9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
                    1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]
    if level == 5:
        num_list = [0, 1, 1, 2, 2, 0, 0, 0, 0, 0, 0, 9,
                    0, 1, 1, 1, 2, 0, 0, 0, 1, 2, 1, 1,
                    0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
                    0, 1, 0, 0, 1, 1, 1, 2, 0, 0, 1, 2,
                    0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 2,
                    0, 0, 0, 0, 0, 1, 9, 0, 0, 1, 1, 2]
    if level == 6:
        num_list = [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 9,
                    0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
                    0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0,
                    0, 2, 0, 1, 9, 2, 2, 2, 1, 0, 2, 0,
                    0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
    if level == 7:
        num_list = [0, 1, 2, 1, 0, 0, 0, 0, 0, 1, 1, 1
            , 0, 1, 2, 0, 0, 2, 1, 1, 0, 0, 0, 0
            , 0, 1, 2, 0, 1, 1, 0, 0, 1, 2, 2, 0
            , 0, 1, 2, 0, 0, 0, 0, 0, 2, 9, 2, 0
            , 0, 0, 1, 1, 1, 1, 1, 0, 2, 0, 2, 0
            , 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0]
    if level == 8:
        num_list = [0, 1, 1, 1, 1, 2, 1, 2, 2, 2, 2, 2,
                    0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 9,
                    0, 0, 0, 1, 0, 2, 0, 1, 1, 0, 0, 9,
                    0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 9,
                    1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 9,
                    1, 1, 2, 0, 0, 1, 0, 0, 2, 2, 2, 1, ]
    if level == 9:
        num_list = [0, 1, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1
            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            , 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 0
            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0
            , 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0]
    if level == 10:
        num_list = [0, 0, 0, 0, 1, 9, 0, 0, 2, 1, 0, 2,
                    1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 2,
                    2, 9, 2, 0, 0, 0, 1, 0, 0, 0, 0, 2,
                    2, 0, 2, 1, 0, 0, 0, 1, 1, 1, 0, 2,
                    2, 0, 2, 2, 1, 0, 0, 0, 0, 0, 0, 2,
                    0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 2]
    if level == 11:
        num_list = [0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2
            , 0, 0, 0, 2, 2, 0, 1, 1, 2, 0, 2, 2
            , 2, 0, 0, 0, 2, 0, 0, 1, 2, 0, 1, 2
            , 2, 2, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0
            , 2, 2, 2, 0, 0, 0, 2, 0, 2, 1, 2, 0
            , 2, 2, 2, 2, 0, 0, 0, 0, 2, 0, 2, 9]
    if level == 12:
        pygame.quit()
        exit()
    if level == 999:
        num_list = [0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0
            , 0, 0, 0, 2, 1, 2, 1, 2, 0, 2, 1, 0
            , 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0
            , 9, 1, 2, 1, 2, 1, 2, 1, 2, 0, 0, 0
            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            , 1, 0, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2]


def reset_rects():
    global ground_rect
    global sky_rect
    global end_rect
    global lava_rect
    global lava_hitbox_rect
    global player_class
    global gravity_direction
    ground_rect = pygame.Rect(-100, 0, 100, 100)
    sky_rect = pygame.Rect(-100, 0, 100, 100)
    end_rect = pygame.Rect(-100, 0, 100, 100)
    lava_rect = pygame.Rect(-100, 0, 100, 100)
    lava_hitbox_rect = pygame.Rect(-100, 0, 75, 75)
    player_class.rect.topleft = (50, 0)
    gravity_direction = False


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


reset_rects()
level_picker()
events = []
physics = True

def create_savestate(slot):
    movie.write_savestate(slot)
    print(f"Created savestate at slot {slot}")

def load_savestate(slot): # TODO: fix rendering and allowing saving and loading from non-frame advance state

    if slot is not None:
        res = movie.parse_lines_of_savestate(slot)

        if res is None:
            print("Empty savestate recieved.")
            return

    global loading_savestate, clock_speed, frame_advance

    clock_speed = 0
    reinitialize()
    # frame_advance = True

    loading_savestate = "true"


while True:

    if frame_advance:
        event = pygame.event.wait()
        while not (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                frame_advance = False
                break

            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                create_savestate(0)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                load_savestate(0)
                break

            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                load_savestate(None)
                break

            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                create_savestate(1)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                load_savestate(1)
                break

            if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                create_savestate(2)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_6:
                load_savestate(2)
                break

            if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                create_savestate(3)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_7:
                load_savestate(3)
                break

            # elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            #     player_class.load(frame_saves.pop())
            #     physics = False
            #     frame -= 1
            #     if movie.mode != 'read':
            #         movie.remove_input()
            #     break
            # if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
            #     converter()
            #     player_class.draw()
            #     pygame.display.update()
            events.append(event)
            if event.type == pygame.QUIT:
                break

            event = pygame.event.wait()

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
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed(3)

    screen.fill("#70a5d7")

    # level_picker()
    player_class.update()
    converter()
    player_class.draw()

    screen.blit(times_new_roman.render(
        str(frame) + ' ' + str(frame - player_class.last_press) + ' ' + str(player_class.grounded), True,
        (255, 255, 255)), (0, 0))
    # if movie.mode == 'read':
    try:
        screen.blit(times_new_roman.render(str(movie.inputs[frame].to_string()), True, (255, 255, 255)), (0, 20))
    except:
        pass
    # elif movie.mode == 'write':
        # screen.blit(times_new_roman.render())

    timer(False)

    if loading_savestate == 'false':
        pygame.draw.rect(screen, (0, 0, 0), (1200, 0, 200, 600))

        mi = int((mouse_pos[1] / 600) * 600 // times_new_roman.get_height())
        for y in range(600 // times_new_roman.get_height()):
            i = y + frame - 300 // times_new_roman.get_height()
            y = y * times_new_roman.get_height()
            try:
                if i < 0:
                    raise IndexError

                if mouse_press[0]:
                    print(mi)
                    movie.studio[mi].a = keys[pygame.K_a]
                    movie.studio[mi].d = keys[pygame.K_d]
                    movie.studio[mi].s = keys[pygame.K_s]
                    movie.studio[mi].r = keys[pygame.K_r]
                    movie.studio[mi].t = keys[pygame.K_t]

                s = movie.studio[i].to_string()
            except IndexError:
                s = '-'
            # s += ' ' + str(i)
            if i == 300 // times_new_roman.get_height():
                b = (100, 100, 100)
            else:
                b = None
            screen.blit(times_new_roman.render(s, True, (255, 255, 255), b), (1200, y))

    if loading_savestate == 'false':
        pygame.display.update()

    clock.tick(clock_speed)
    physics = True
    print(frame_advance)
