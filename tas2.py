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
import json
import os
import typing

MOVIE_FILE_EXTENSION = ".ptm"

MAGIC_HEADER = "!ptm"
GAME_VERSION_REF = "!gameversion"
INPUT_START = "!input-start"
SAVESTATE_DATA = "!savestate"
COMMAND_SEPERATOR = "|"
COMMENT_START = "//"

PLATFORMER_INPUT_MAPPING = {"A" : 'a',
                            "D": 'd',
                            "S": 'SPACE',
                            "R": 'r',
                            "T": 't'}

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

        self.movie_name = "a"
        self.movie_filename = self.movie_name + MOVIE_FILE_EXTENSION

        self.save_state_class = save_state_class
        self.save_states: dict[int, tuple[SaveState, int]] = {}

        self.inputs = []

        # movie mode
        try:
            with open(self.config_file, "r") as f:

                mode = f.read().strip()

                if len(mode) > 1 or not mode.isdigit() or (mode.isdigit() and int(mode) > len(MovieMode)):
                    raise ValueError(f"Unknown mode: {repr(mode)}, the value should be in {[v.value for v in MovieMode]} ({self.config_file})")
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
            extra_data = self.read_file()
            version = int(extra_data.pop(GAME_VERSION_REF[1:]))
            if version != self.GAME_VERSION:
                print('WARNING: wrong version tas')
                if version < self.GAME_VERSION:
                    print(f"    Outdated TAS version ({version}), this version is {self.GAME_VERSION}")
                elif version > self.GAME_VERSION:
                    print(f"    TAS for newer game version ({version}), this version is {self.GAME_VERSION}")
            if extra_data:
                print(f'WARNING: unused extra_data: {extra_data}')
            # raise NotImplementedError('loading frames from movie file')

    def create_savestate(self, slot: int):
        self.save_states[slot] = (self.save_state_class(), self.frame)
        print(f"saving slot {slot}")

        # /saves/
        os.makedirs(self.movie_name, exist_ok=True) # a.ptm

        # a > saves > 0.ptm, ...
        #     a.ptm
        #

        with open(os.path.join(self.movie_name, f'{slot}{MOVIE_FILE_EXTENSION}'), 'w') as f:
            self._write_header(f, extra_data={'savestate': json.dumps(self.save_states[slot][0].serialize())})

            self.write_all_inputs(f)

    def load_savestate(self, slot: int):
        if slot not in self.save_states:
            with open(os.path.join(self.movie_name, f'{slot}{MOVIE_FILE_EXTENSION}'), 'r') as f:
                extra_data = self.read_file(f)

                self.save_states[slot] = (self.save_state_class(json.loads(extra_data.pop('savestate'))), len(self.inputs))
                self.frame = len(self.inputs)
                if extra_data:
                    print(f'WARNING: unused extra_data: {extra_data}')

        self.save_states[slot][0].load()
        self.frame = self.save_states[slot][1]
        print(f"loading slot {slot}")

        if self.mode == MovieMode.WRITE:
            self.inputs = self.inputs[:self.frame]

            os.truncate(self.movie_filename, 0)
            with open(self.movie_filename, 'w') as f:
                self._write_header(f)
                self.write_all_inputs(f)

    def _write_header(self, f: typing.TextIO | None = None, extra_data: dict[str, str] | None = None) -> None: # f is file,
        # extra_data = {'savestate': '{"player_clazz": "", gravity_direction: False}'}
        def __write_header(f_):
            f_.write(MAGIC_HEADER + "\n")
            f_.write(f"{GAME_VERSION_REF} {self.GAME_VERSION}\n")
            if extra_data is not None:
                for key in extra_data:
                    f_.write('!' + key + " " + extra_data[key] + '\n')
            f_.write(INPUT_START + "\n")

        if f is None:
            with open(self.movie_filename, "w") as f:
                __write_header(f)
        else:
            __write_header(f)

    def write_input(self, _input: Input):

        self.frame += 1
        self.inputs.append(_input)

        with open(self.movie_filename, "a") as f:
            f.write(f"{_input.to_string()}\n")

    def write_all_inputs(self, f: typing.TextIO):
        for input_ in self.inputs:
            f.write(input_.to_string() + '\n')

    def get_inputs(self):
        self.frame += 1
        try:
            return self.inputs[self.frame - 1]
        except IndexError:
            return Input([False] * 5)

    def read_file(self, f: typing.TextIO | None = None) -> dict:
        def _read_file(f_) -> dict:
            extra_data: dict[str, str] = {}

            class ParseState(enum.Enum):
                BEFORE_HEADER = enum.auto()
                EXTRA_DATA = enum.auto()
                INPUTS = enum.auto()

            # TODO: parse comments and commands

            self.inputs = []

            state = ParseState.BEFORE_HEADER
            for line in f_.read().split('\n'):
                line = line.strip()
                if state == ParseState.BEFORE_HEADER:
                    if line != MAGIC_HEADER:
                        print(f'Warning: EXTRANEOUS data before ptm file {repr(line)}')
                    else:
                        state = ParseState.EXTRA_DATA
                elif state == ParseState.EXTRA_DATA:
                    if line == INPUT_START:
                        state = ParseState.INPUTS
                    else:
                        if line[0] != '!':
                            raise ValueError(f"Invalid extra data line '{repr(line)}'")
                        key, _, value = line.partition(' ')
                        extra_data[key[1:]] = value
                elif state == ParseState.INPUTS:
                    if not line:
                        pass
                    else:
                        self.inputs.append(Input([line[i] == list(PLATFORMER_INPUT_MAPPING.keys())[i] for i in range(len(PLATFORMER_INPUT_MAPPING)) if line[i] in [list(PLATFORMER_INPUT_MAPPING.keys())[i], '.']]))
                else:
                    raise NotImplementedError(state)
            return extra_data

        if f is None:
            with open(self.movie_filename, 'r') as f:
                return _read_file(f)
        else:
            return _read_file(f)


class Input:

    def __init__(self, inputs: list):
        if len(inputs) != len(PLATFORMER_INPUT_MAPPING):
            raise ValueError(repr(inputs))

        self.inputs = inputs

    def to_string(self) -> str:
        return f"{''.join([list(PLATFORMER_INPUT_MAPPING.keys())[_] if self.inputs[_] else '.' for _ in range(len(PLATFORMER_INPUT_MAPPING))])}"


class SaveState(abc.ABC):

    @abc.abstractmethod
    def __init__(self, from_dict: dict | None = None):
        pass

    @abc.abstractmethod
    def load(self):
        pass

    @abc.abstractmethod
    def serialize(self) -> dict:
        pass
