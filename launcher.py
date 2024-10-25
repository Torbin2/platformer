from __future__ import annotations

import sys
import pygame

import tas
# from main import big_display

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

print(f'Parsed game version: {gameversion}')
tas_handler = tas.TASHandler(gameversion)
tas_handler.init_movie()
our_clock = pygame.time.Clock()


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
        'quit': lambda *args, **kwargs: tas_handler.finish_movie(),
        'event.get': event_get
    }


def get_pressed(*args, **kwargs):
    global keys
    keys = pygame.key.get_pressed()
    # TODO: overwrites
    return keys


def update(*args, **kwargs):
    tas_handler.handle_input(keys)
    run = True
    while not tas_handler.frame_advance and run:
        our_clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Exiting from launcher.py')
                pygame.quit()
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    tas_handler.frame_advance = True
                elif event.key == pygame.K_RIGHT:
                    # Return from this function but return because tas_handler.frame_advance is still False
                    run = False

        rect = platformer.player_class.rect

        drawing_rect = pygame.Rect(rect.left - platformer.scroll[0], rect.top - platformer.scroll[1], rect.width, rect.height)
        pygame.draw.rect(platformer.big_display,  (255, 0, 0), drawing_rect)

        height = rect.height // 3
        t = (rect.bottomleft[0] - platformer.scroll[0], rect.bottomleft[1] - height - platformer.scroll[1]) if platformer.gravity_direction else (rect.topleft[0] - platformer.scroll[0], rect.topleft[1] - platformer.scroll[1])
        pygame.draw.rect(platformer.big_display, (255, 255, 255), (t[0], t[1], rect.width, height))

        print("direction", platformer.gravity_direction)

        if platformer.level > 22:
            platformer.screen.blit(pygame.transform.scale(platformer.big_display, (1200, 600)), (0, 0))
        else:
            platformer.screen.blit(platformer.big_display, (0, 0))

        pygame.display.update()


def event_get(*args, **kwargs):
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                tas_handler.frame_advance = False

    return events


class Clock:
    def __init__(self, *args, **kwargs):
        self._clock = pygame.time.Clock(*args, **kwargs)
        self._fps = 60

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
    'time.Clock': Clock,
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
