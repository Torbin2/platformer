import pygame

class Block:
        def __init__(self,num ):
            self.rect = pygame.Rect((num % 12)*100, (num//12)*100, 100,100)
            self.type = 0
            self.num = num
        def update(self, screen):
            pygame.draw.rect(screen, self.colour(self.type),self.rect)
            pygame.draw.rect(screen, ("black"),self.rect,2)
        def colour(self, num):
            if num == 0:
                return ("#70a5d7")
            if num == 1:
                return ("#446482")
            if num == 2:
                return ("#bea925")
            if num in (3,4,5,6):
                return ("#824464")
            if num in (7,8):
                return ("black")
            if num == 9:
                return ('#6c25be')

class Level_editor:
    def __init__(self):
        self.screen = pygame.Surface((1200,1200))
        self.real_screen = pygame.display.set_mode((1200,600))
        pygame.display.set_caption('platformer level editor')
        self.clock = pygame.time.Clock()
        self.selected_rect = 0
        self.key_press = [False,0]
        self.offset = 0
        self.onn = True
        
        self.num_list = []
        for i in range(144):
            self.num_list.append(Block(i))

    def mous(self):
        mouse_pos = pygame.mouse.get_pos()
        self.selected_rect = mouse_pos[0]//100 + (mouse_pos[1] // 100) *12 + (self.offset //100) *12
    def update(self):
        while self.onn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.onn = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        print_list = '['
                        for i in self.num_list:
                            print_list += (str(i.type) + ", ")
                            if i.num % 12 == 11 :
                                print_list += ("8, \n")
                        print(print_list + "],")
                    elif event.key == pygame.K_l:
                        if self.offset != 600:
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
                self.num_list[self.selected_rect].type = self.key_press[1]
            for rect in self.num_list:
                rect.update(self.screen)
            
            self.real_screen.blit(self.screen, (0, 0 - self.offset))
            pygame.display.update()
            self.clock.tick(60)
