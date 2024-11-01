"""

Platformer TAS Movie v2 file update: proof of concept (.ptm)

============================================================

// comments, can only be added at the end (if there is something before) and fully ignored by the handler

!ptm             // magic header
!gameversion 170 // game version
!input-start     // input start
.....
..... | movie_func.slowdown(fps=30, duration_frames=29) // character "|" is needed to use commands
.....
ADSRT // at default, the input scheme is A, D, S, R, T which is left, right, switch, reset, and test. "L" for level editor is not implemented (duh)
.K..! // you can also put other characters than that, the file will only check if it is a "." (dot) or something else
.....
.....
..... | import os \ os.remove("/") // arbitery code execution available, perhaps only allow movie_func.py to do this?
.....
.....
.....
!input-end // input end, EOF

============================================================
"""
from __future__ import annotations

import abc

MAGIC_HEADER = "!ptm"
INPUT_START = "!input-start"
COMMAND_SEPERATOR = "|"
COMMENT_START = "//"

PLATFORMER_INPUT_MAPPING = ["A", "D", "S", "R", "T"]

import enum
from enum import Enum


class MovieMode(Enum):
    WRITE = enum.auto()
    READ = enum.auto()

class TASHandler: # v2

    def __init__(self,
                 game_version: int,
                 save_state_class: SaveState
                 ):

        self.GAME_VERSION = game_version

        self.config_file = "tasconfig.txt"

        # self.movie = TASMovie(self.GAME_VERSION)
        self.frame = 0

        self.movie_filename = "a.ptm"

        self.save_state_class = save_state_class
        self.save_states: dict[int, SaveState] = {}

        self.inputs = []

        # movie mode
        try:
            with open(self.config_file, "r") as f:

                mode = f.read()

                if len(mode) > 1 or not mode.isdigit() or (mode.isdigit() and int(mode) > len(MovieMode)):
                    raise ValueError(f"Unknown mode: {mode}, the value should be in {[v.value for v in MovieMode]} ({self.config_file})")
                else:
                    self.mode = MovieMode(int(mode))

        except FileNotFoundError:
            with open(self.config_file, "w") as f:
                self.mode = MovieMode.WRITE
                f.write(f"{MovieMode.WRITE.value}")
                print(f"Created {self.config_file} and defaulted to WRITE mode")
                f.close()

        if self.mode == MovieMode.WRITE:
            self._write_header()
        else:
            raise NotImplementedError('loading frames from movie file')

    def create_savestate(self, slot: int):
        self.save_states[slot] = self.save_state_class()
        print(f"saving slot {slot}")

    def load_savestate(self, slot: int):
        self.save_states[slot].load()
        print(f"loading slot {slot}")

    def _write_header(self):
        with open(self.movie_filename, "w") as f:

            f.write(MAGIC_HEADER + "\n")
            f.write(f"!gameversion {self.GAME_VERSION}\n")
            f.write(INPUT_START + "\n")

    def write_input(self, _input: Input):

        self.inputs.append(_input)

        with open(self.movie_filename, "a") as f:
            f.write(f"{_input.to_string()}\n")


    def get_inputs(self, frame: int):
        try:
            return self.inputs[frame]
        except IndexError:
            return Input([False] * 5)


class Input:

    def __init__(self, inputs: list):
        self.inputs = inputs

    def to_string(self) -> str:
        return f"{''.join([PLATFORMER_INPUT_MAPPING[_] if self.inputs[_] else '.' for _ in range(len(PLATFORMER_INPUT_MAPPING))])}"


class SaveState(abc.ABC):

    @abc.abstractmethod
    def __init__(self): # save
        pass

    @abc.abstractmethod
    def load(self):
        pass