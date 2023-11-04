#
# Platformer TAS Movie Format
#
# !ptm
# !gameversion [Version of the game]
# !input-start
# (here goes the inputs, e.g. "L.S", ".RS", "...", "LR.", "LRS")
# !input-end
import os


class TASMovie:

    def __init__(self):
        self.gameversion = 0
        self.filename = "test.ptm"
        self.mode = ""

        with open("tasconfig.txt", "r") as f:
            self.mode = f.read()

        self.inputs = []

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

    def write_input(self, inputs: list[bool, bool, bool]):
        with open(self.filename, "a") as f:
            f.write(f"{'L' if inputs[0] else '.'}"
                    f"{'R' if inputs[1] else '.'}"
                    f"{'S' if inputs[2] else '.'}\n")
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




    def parse(self, line: str):

        res = []

        for c in line:

            if c == "\n":
                continue

            if c == ".":
                res.append(False)
            else:
                res.append(True)

        return TASMovie.Input(res)
    class Input:

        def __init__(self, inputs: [bool, bool, bool]):

            print("inputs", inputs)

            self.l = inputs[0]
            self.r = inputs[1]
            self.s = inputs[2]
