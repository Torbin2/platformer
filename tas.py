#
# Platformer TAS Movie Format
#
# !ptm
# !gameversion [Version of the game]
# !input-start
# (here goes the inputs, e.g. "A.S..", ".DS..", ".....", "AD..T", "ADSRT")
# !input-end
import os


class TASMovie:

    def __init__(self):
        self.gameversion = 1
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
            f.write(f"{'A' if inputs[0] else '.'}"
                    f"{'D' if inputs[1] else '.'}"
                    f"{'S' if inputs[2] else '.'}"
                    f"{'R' if inputs[3] else '.'}"
                    f"{'T' if inputs[4] else '.'}\n")
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

        while len(res) < 6: # to make sure old ptm files also works
            res.append(False)

        return TASMovie.Input(res)
    class Input:

        def __init__(self, inputs: [bool, bool, bool, bool, bool]):

            print("inputs", inputs)

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
