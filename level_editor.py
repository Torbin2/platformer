import pygame
import json

class Block:
        def __init__(self,num, type ):
            self.rect = pygame.Rect((num % 13)*100, (num//13)*100, 100,100)
            self.type = type
            self.num = num
        def update(self, screen):
            pygame.draw.rect(screen, self.colour(self.type),self.rect)
            pygame.draw.rect(screen, ("black"),self.rect,2)
        def colour(self, num):
            if num == 0:
                return ("#70a5d7")
            elif num == 1:
                return ("#446482")
            elif num == 2:
                return ("#bea925")
            elif num in (3,4,5,6):
                return ("#824464")
            elif num == 8:
                return ("green")
            elif num == 9:
                return ('#6c25be')
            else:
                print("eror", num)
                return("red")
            

class Level_editor:
    def __init__(self):
        self.screen = pygame.Surface((1300,1200))
        self.real_screen = pygame.display.set_mode((1200,600))
        pygame.display.set_caption('platformer level editor')
        self.clock = pygame.time.Clock()
        self.selected_rect = 0
        self.key_press = [False,0]
        self.offset = 0
        self.button_depth = 0
        
        with open("new_levels.json", "r") as f:

            self.levels = json.load(f)
        self.num_list = self.convert(self.levels[self.button_depth])

    def convert(self, nums):
        new_list = []
        for num, type in enumerate(nums):
            new_list.append(Block(num, type))

        return new_list

        

    def mous(self):
        mouse_pos = pygame.mouse.get_pos()
        self.selected_rect = mouse_pos[0]//100 + (mouse_pos[1] // 100) *13 + (self.offset //100) *13

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
                        for num,i in enumerate(self.num_list):
                            nlist.append(int(i.type))
                            if num % 13 == 12:
                                nlist.append(8)

                        # print(nlist)
                        self.levels.append(nlist)
                        print("saved")
                    
                    elif event.key == pygame.K_s:
                        with open("new_levels.json", "w") as file:
                            json.dump(self.levels, file)

                    elif event.key == pygame.K_n: #refresh level
                        with open("new_levels.json", "w") as file:
                            x = [[]]
                            json.dump(x, file)
                            self.levels = [[]]
                            self.button_depth = 0
                            self.num_list = self.convert(self.levels[self.button_depth])


                    elif event.key == pygame.K_b:
                        if self.button_depth < self.levels.__len__() - 1:
                            self.button_depth +=1
                        else : self.button_depth = 0

                        self.num_list = self.convert(self.levels[self.button_depth])

                                            
                    elif event.key == pygame.K_l:
                        self.offset +=100
                    elif event.key == pygame.K_o:
                        if self.offset != 0:
                            self.offset -=100
                    
                    elif int(event.key) in range(48, 58):
                        self.key_press = [True,int(event.key)-48]
                    else: print("keyboard issue")
                
                if event.type == pygame.KEYUP:
                    self.key_press = [False,0]
                    
                    
            self.screen.fill("black")
            self.mous()
            if self.key_press[0]:
                if self.selected_rect < self.num_list.__len__():
                    self.num_list[self.selected_rect].type = self.key_press[1]
                else:
                    over = self.selected_rect - self.num_list.__len__() + 1
                    for i in range(over):
                        self.num_list.append(Block( self.num_list.__len__(), 0))
                                

            for rect in self.num_list:
                rect.update(self.screen)
            
            self.real_screen.blit(self.screen, (0, 0 - self.offset))
            pygame.display.update()
            self.clock.tick(60)
