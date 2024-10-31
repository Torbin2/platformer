import pygame
import json

LENGHT = [5]  # in blocks


# change self.screen size to change y length

class Block:
    def __init__(self, num, type):
        self.rect = pygame.Rect((num % (LENGHT[0] + 1)) * 100, (num // (LENGHT[0] + 1)) * 100, 100, 100)
        if type in (3, 4, 5, 6):
            self.rect = self.create_button(type, self.rect)
        self.type = type
        self.num = num

    def update(self, screen):
        pygame.draw.rect(screen, self.colour(self.type), self.rect)
        pygame.draw.rect(screen, ("black"), self.rect, 2)

    def colour(self, num):
        if num == 0:
            return ("#70a5d7")
        elif num == 1:
            return ("#446482")
        elif num == 2:
            return ("#bea925")
        elif num in (3, 4, 5, 6):
            return ("#824464")
        elif num == 8:
            return ("#a3ef90")
        elif num == 9:
            return ('#6c25be')
        else:
            print("eror", num)
            return ("red")

    def create_button(self, b_type, rect):
        # button(b_type) directions:
        #  3
        # 6   4
        #  5
        if b_type == 3 or b_type == 5:
            rect.size = (80, 35)
            if b_type == 5:
                rect.top += 100 - 35
            rect.left += (100 - 80) / 2
        else:
            rect.size = (35, 80)
            if b_type == 4:
                rect.left += 100 - 35
            rect.top += (100 - 80) / 2

        return rect


class Level_editor:
    def __init__(self):
        self.screen = pygame.Surface((LENGHT[0] * 100, 4800))  # rendering breaks after y-value, so ignore that :)
        self.real_screen = pygame.display.set_mode((LENGHT[0] * 100, 2400))
        pygame.display.set_caption('platformer level editor')
        self.clock = pygame.time.Clock()
        self.selected_rect = 0
        self.key_press = [False, 0]
        self.offset = 0
        self.button_depth = 0

        with open("new_levels.json", "r") as f:
            self.levels = json.load(f)
        self.num_list = self.convert(self.levels[self.button_depth])

    def convert(self, nums):
        new_list = []
        x = 0
        for num, type in enumerate(nums):
            if type != 8:
                new_list.append(Block(num - x, type))
            else:
                x += 1  # removes 8

        return new_list

    def mous(self):
        mouse_pos = pygame.mouse.get_pos()
        self.selected_rect = mouse_pos[0] // 100 + (mouse_pos[1] // 100) * (LENGHT[0] + 1) + (self.offset // 100) * (
                    LENGHT[0] + 1)

    def update(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    #     if event.key == pygame.K_p:
                    #         print("[")
                    #         for i in self.levels:
                    #             print_list = '['
                    #             for x in i:
                    #                 print_list += (str(x) + ", ")
                    #             print(print_list + "],")
                    #         print("]")

                    if event.key == pygame.K_a:
                        nlist = []
                        for num, i in enumerate(self.num_list):
                            nlist.append(int(i.type))
                            if num % (LENGHT[0] + 1) == (LENGHT[0]):
                                nlist.append(8)
                        nlist.append(8)

                        # print(nlist)
                        self.levels.append(nlist)
                        print("saved")

                    elif event.key == pygame.K_s:
                        with open("new_levels.json", "w") as file:
                            json.dump(self.levels, file)

                    elif event.key == pygame.K_c:
                        with open("new_levels.json", "w") as file:
                            x = [[]]
                            json.dump(x, file)


                    elif event.key == pygame.K_n:  # refresh levels
                        with open("new_levels.json", "w") as file:
                            x = [[]]
                            json.dump(x, file)
                            self.levels = [[]]
                            self.button_depth = 0
                            self.num_list = self.convert(self.levels[self.button_depth])

                    elif event.key == pygame.K_r:  # refresh numlist
                        self.num_list = []


                    elif event.key == pygame.K_b:
                        if self.button_depth < self.levels.__len__() - 1:
                            self.button_depth += 1
                        else:
                            self.button_depth = 0

                        self.num_list = self.convert(self.levels[self.button_depth])


                    elif event.key == pygame.K_l:
                        self.offset += 300
                    elif event.key == pygame.K_o:
                        if self.offset != 0:
                            self.offset -= 300

                    elif int(event.key) in range(48, 58):
                        self.key_press = [True, int(event.key) - 48]
                    else:
                        print("keyboard issue")

                if event.type == pygame.KEYUP:
                    self.key_press = [False, 0]

            self.screen.fill("#296d18")
            self.mous()
            if self.key_press[0]:
                if self.selected_rect < self.num_list.__len__():
                    self.num_list[self.selected_rect] = Block(self.selected_rect, self.key_press[1])


                else:
                    over = self.selected_rect - self.num_list.__len__() + 1
                    for i in range(over):
                        self.num_list.append(Block(self.num_list.__len__(), 0))

            for rect in self.num_list:
                rect.update(self.screen)

            self.real_screen.blit(self.screen, (0, 0 - self.offset))
            pygame.display.update()
            self.clock.tick(60)