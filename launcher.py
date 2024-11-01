from __future__ import annotations

import sys
import typing
import copy

import pygame

import tas2 as tas

TO_RUN_MODULE = 'main'
to_run_module_file_name = TO_RUN_MODULE + '.py'
THIS_NAME = 'launcher'

if THIS_NAME not in sys.modules:
    __import__(THIS_NAME)

    # https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
    this_module = sys.modules[THIS_NAME]
    sys.modules['pygame'] = this_module

    print(f'injected, running {TO_RUN_MODULE}')
    __import__(TO_RUN_MODULE)


keys = None
platformer = None

with open(to_run_module_file_name, 'r') as file:
    version = file.readline()[:-1]
    if version[:3] != '# V':
        raise ValueError("No valid version found with regex # Vn.n.n")
    version = version[3:]

    split = version.split('.')
    out = ''
    for s in split:
        if len(s) > 1:
            raise ValueError(repr(s))
        out += s
    gameversion = int(out)


class SaveState(tas.SaveState):

    NEEDED_VAR_NAMES = {
        'player_class',
        'level',
        'timer',
        'gravity_direction',
        'rect_list',
        'num_list',
        'button_clicks',
        'frames_timer',
        'total_frames'
    }

    def __init__(self):
        print('creating savestate')

        global platformer
        assert platformer is not None

        self._values: dict[str, typing.Any] = {}
        for name in self.NEEDED_VAR_NAMES:
            self._values[name] = copy.deepcopy(getattr(platformer, name))

    def load(self):
        global platformer
        assert platformer is not None

        for name in self.NEEDED_VAR_NAMES:
            setattr(platformer, name, copy.deepcopy(self._values[name]))

        pygame.display.update()


print(f'Parsed game version: {gameversion}')
tas_handler = tas.TASHandler(gameversion, SaveState)
our_clock = pygame.time.Clock()

frame_advance = False

DEFAULT_CLOCK_SPEED = 60


def get_pressed_init(*args, **kwargs):
    get_pressed(*args, **kwargs)

    global platformer
    platformer = sys.modules[TO_RUN_MODULE]

    if platformer is None:
        raise ModuleNotFoundError("No platformer instance!")

    global WRAP_FUNC
    WRAP_FUNC |= {
        'key.get_pressed': get_pressed,
        'display.update': update,
        # 'quit': lambda *args, **kwargs: print("hello, seamen!"),
        'event.get': event_get
    }


def get_pressed(*args, **kwargs):
    global keys
    keys = pygame.key.get_pressed()
    # TODO: overwrites
    return keys


def update(*args, **kwargs):

    global frame_advance

    if tas_handler.mode == tas.MovieMode.WRITE:
        tas_handler.write_input(tas.Input([
            keys[getattr(pygame, 'K_' + k.lower())] for k in tas.PLATFORMER_INPUT_MAPPING
        ]))
    else:
        raise NotImplementedError("can't play movie files")

    run = True
    while not frame_advance and run:
        our_clock.tick(DEFAULT_CLOCK_SPEED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                print('Exiting from launcher.py')
                pygame.quit()
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    frame_advance = True
                elif event.key == pygame.K_RIGHT:
                    # Return from this function but return because frame_advance is still False
                    run = False
                elif event.key == pygame.K_w:
                    tas_handler.create_savestate(0)
                elif event.key == pygame.K_2:
                    tas_handler.load_savestate(0)


        # debug player gravity thingy

        rect = platformer.player_class.rect

        drawing_rect = pygame.Rect(rect.left - platformer.scroll[0], rect.top - platformer.scroll[1], rect.width, rect.height)
        pygame.draw.rect(platformer.big_display,  (255, 117, 0), drawing_rect)

        height = rect.height // 3
        t = (rect.bottomleft[0] - platformer.scroll[0], rect.bottomleft[1] - height - platformer.scroll[1]) if platformer.gravity_direction else (rect.topleft[0] - platformer.scroll[0], rect.topleft[1] - platformer.scroll[1])
        pygame.draw.rect(platformer.big_display, (64, 64, 64), (t[0], t[1], rect.width, height))

        # print("direction", platformer.gravity_direction)

        if platformer.level > 22:
            platformer.screen.blit(pygame.transform.scale(platformer.big_display, (1200, 600)), (0, 0))
        else:
            platformer.screen.blit(platformer.big_display, (0, 0))

        pygame.display.update()


def event_get(*args, **kwargs):
    global frame_advance
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                frame_advance = False

    return events


class Clock:
    def __init__(self, *args, **kwargs):
        self._clock = pygame.time.Clock(*args, **kwargs)
        self._fps = DEFAULT_CLOCK_SPEED

    def __getattr__(self, item):
        if item == 'tick':
            return self._tick
        else:
            return getattr(self._clock, item)

    def _tick(self, fps: int):
        self._clock.tick(self._fps)


WRAP_FUNC = {
    'display.update': lambda *args: print('pygame.display.update', *args),
    'key.get_pressed': get_pressed_init,
    'time.Clock': Clock
}


def _getattr(module, item, name=''):
    item = name + '.' + item if name else item
    # print(f"get: '{item}'")
    if type(module) is int:
        return module
    return Module(module, item)


class Module:
    def __init__(self, module: Module, name: str):
        self.module = module
        self.name = name

    def __call__(self, *args, **kwargs):
        if self.name in WRAP_FUNC:
            r = WRAP_FUNC[self.name](*args, **kwargs)
            if r is not None:
                return r
        return self.module(*args, **kwargs)

    def __getattr__(self, item):
        r = getattr(self.module, item)
        return _getattr(r, item, self.name)


def __getattr__(name):
    return _getattr(getattr(pygame, name), name)

