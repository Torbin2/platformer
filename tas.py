#
# Platformer TAS Movie Format
#
# !ptm
# !gameversion [Version of the game]
# !input-start
# (here goes the inputs, e.g. "A.S..", ".DS..", ".....", "AD..T", "ADSRT")
# !input-end

import pygame
import os
from enum import Enum, auto

class MovieMode(Enum):
    WRITE = auto()
    READ = auto()

class TASHandler:

    def __init__(self):

        self.movie = TASMovie()
        self.mode = "write"
        self.frame = 0
        self.frame_advance = False
        self.loading_savestate = False
        self.default_clock_speed = 60
        self.clock_speed = self.default_clock_speed
        self.physics = True

        with open("tasconfig.txt", "r") as f:
            self.mode = f.read()

    def init_movie(self):
        if self.mode == "write":
            self.movie.write_header()
        elif self.mode == "read":
            self.frame_advance = False
            self.movie.read_inputs()

    def finish_movie(self):
        if self.mode == "write":
            self.movie.write_end()

    def pressed(self, normal_pressed: bool, key: str):
        # print(f'key: {key}, normal_pressed: {normal_pressed}, p: {(self.mode != "read" and not self.loading_savestate and normal_pressed) or (self.mode == "read" and eval(f"self.movie.get_inputs(self.frame).{key}")) or (self.mode == "write" and self.loading_savestate and eval(f"self.movie.get_inputs(self.frame).{key}"))}')
        return (self.mode != "read" and not self.loading_savestate and normal_pressed) or (self.mode == "read" and eval(f"self.movie.get_inputs(self.frame).{key}")) or (self.mode == "write" and self.loading_savestate and eval(f"self.movie.get_inputs(self.frame).{key}"))




    def handle_input(self, keys):

        if self.physics:

            if self.mode == "write":

                if self.loading_savestate:

                    self.frame_advance = False

                    if self.frame >= self.movie.inputs.__len__() - 1:
                        self.clock_speed = self.default_clock_speed
                        self.frame_advance = True
                        self.loading_savestate = False
                        self.frame += 1
                        return

                else:
                    self.movie.write_input([keys[pygame.K_a],
                                       keys[pygame.K_d],
                                       keys[pygame.K_SPACE],
                                       keys[pygame.K_r],
                                       keys[pygame.K_t]])

            elif self.mode == "read":
                pass

        self.frame += 1

    def create_savestate(self, slot: int):
        self.movie.write_savestate(slot)
        print(f"Created savestate at slot {slot}")

    def load_savestate(self, slot: int, reinit_func):

        if slot is not None:
            res = self.movie.parse_lines_of_savestate(slot)

            if res is None:
                print("Empty savestate received, ignoring...")
                return

        self.clock_speed = 0
        reinit_func()

        self.loading_savestate = True


class TASMovie:

    def __init__(self):
        self.gameversion = 102
        self.filename = "test.ptm"
        # self.studio = []

        self.inputs = []

    def get_inputs(self, frame: int):

        try:
            return self.inputs[frame]
        except:
            return TASMovie.Input([False, False, False, False, False])


    def write_header(self):

        if self.filename in os.listdir("."):
            os.remove(self.filename)

        with open(self.filename, "a") as f:

            f.write("!ptm\n")
            f.write(f"!gameversion {self.gameversion}\n")
            f.write("!input-start\n")
            f.close()

    def write_end(self):
        with open(self.filename, "a") as f:
            f.write("!input-end")
            f.close()

    def write_input(self, inputs: list[bool, bool, bool, bool, bool]):

        self.inputs.append(TASMovie.Input(inputs))

        with open(self.filename, "a") as f:
            f.write(f"{'A' if inputs[0] else '.'}"
                    f"{'D' if inputs[1] else '.'}"
                    f"{'S' if inputs[2] else '.'}"
                    f"{'R' if inputs[3] else '.'}"
                    f"{'T' if inputs[4] else '.'}\n")
            f.close()

    def set_inputs(self, inputs):

        with open(self.filename, 'w+') as f:

            f.seek(0)
            f.truncate()
            f.write("!ptm\n")
            f.write("!gameversion 1\n")
            f.write("!input-start\n")

            for i in range(len(inputs)):

                input: TASMovie.Input = inputs[i]

                f.write(f"{input.to_string()}\n")

            # f.write("!input-end")
            f.close()



    def remove_input(self, frame):
        with open(self.filename, 'r+') as f:

            lines = f.readlines()

            res = []

            for i in range(len(lines)):
                if i <= frame - 1 + 3: # here you have to remove 3 because of the headers
                    res.append(lines[i])

            f.seek(0)
            f.truncate()
            f.writelines(res)
            f.close()

    def read_inputs(self):

        with open(self.filename, "r+") as f:

            contents = f.readlines()

            print(contents)

            started = False
            finished = False

            for i in range(len(contents)):

                line = contents[i]

                if i == 0:
                    if line.startswith("!ptm"):
                        continue
                    else:
                        raise KeyError("Platformer TAS Movie should always start with !ptm")

                if i == 1:
                    if contents[1].startswith("!gameversion"):
                        try:
                            self.gameversion = contents[1].split(" ")[1]
                            continue
                        except:
                            raise ValueError("Malformed Platformer TAS Movie file found! check !gameversion line 1")
                    else:
                        raise KeyError("Platformer TAS Movie should include gameversion attribute")


                if line.startswith("!input-start"):
                    print("Start of the inputs")
                    started = True
                    continue

                if line.startswith("!input-end"):
                    finished = True
                    print("End of the inputs")
                    continue
                else:
                    if started and not finished:
                        self.inputs.append(self.parse(line))


    def write_savestate(self, slot: int):

        if not os.path.isdir("saves"):
            os.mkdir("saves")

        filename = f"{slot}.psv"

        with open("saves/" + filename, "w") as f:
            f.write("!psv\n")
            # json.dump(save, f)
            f.write("!input-start\n")

            for input in self.inputs:
                f.write(f"{input.to_string()}\n")

            f.write("!input-end")
            f.close()

    def parse_lines_of_savestate(self, slot: int):

        filename = f"{slot}.psv"

        if filename not in os.listdir("./saves"):
            return None

        with open("saves/" + filename, "r+") as f:

            lines = f.readlines()

            # print(lines)

            inputs = []
            started = False

            for i in range(len(lines)):

                line = lines[i]

                if i == 0:
                    if line.startswith("!psv"):
                        continue
                    else:
                        raise KeyError(f"Platformer savestate file should always start with !psv, instead got {line}")

                if line.startswith("!input-start"):
                    started = True
                    print("starting line")
                    continue

                if line.startswith("!input-end"):

                    print("end line")

                    if self.inputs is None:
                        print("none??")
                        assert False, ""

                    self.inputs = inputs
                    self.set_inputs(self.inputs)

                    # if slot == 0:
                    #     self.studio = self.inputs

                    return inputs
                else:

                    if started:
                        print(f"parse {line}")
                        inputs.append(self.parse(line))



    def parse(self, line: str):

        res = []

        for c in line:

            if c == "\n":
                continue

            if c == ".":
                res.append(False)
            else:
                res.append(True)

        while len(res) < 6: # to make sure old ptm files also works
            res.append(False)

        return TASMovie.Input(res)

    class Input:

        def __init__(self, inputs: [bool, bool, bool, bool, bool]):

            self.a = inputs[0]
            self.d = inputs[1]
            self.s = inputs[2]
            self.r = inputs[3]
            self.t = inputs[4]

        def to_string(self) -> str:
            return (f"{'A' if self.a else '.'}"
                    f"{'D' if self.d else '.'}"
                    f"{'S' if self.s else '.'}"
                    f"{'R' if self.r else '.'}"
                    f"{'T' if self.t else '.'}")
