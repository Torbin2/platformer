"""

Platformer TAS Movie v2 file update: proof of concept (.ptm)

============================================================

// comments, can only be added at the end (if there is something before) and fully ignored by the handler

!ptm             // magic header
!gameversion 170 // game version
!input-start     // start header
.....
..... | [movie_func.slowdown(fps=30, duration_frames=29)] // commands in between [], character "|" is needed to use
.....
ADSRT // at default, the input scheme is A, D, S, R, T which is left, right, switch, reset, and test. "L" for level editor is not implemented (duh)
.K..! // you can also put other characters than that, the file will only check if it is a "." (dot) or something else
.....
.....
..... | [import os] [os.remove("/")] // arbitery code execution available, perhaps only allow movie_func.py to do this?
.....
.....
.....
!input-end // EOF

============================================================
"""
import enum
from enum import Enum


class MovieMode(Enum):
    WRITE = enum.auto()
    READ = enum.auto()

class TASHandler: # v2

    def __init__(self,
                 game_version: int,
                 default_clock_speed: int
                 ):

        self.GAME_VERSION = game_version
        self.DEFAULT_CLOCK_SPEED = default_clock_speed

        self.config_file = "tasconfig.txt"
        self.mode = None

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



a = TASHandler(171, 60)