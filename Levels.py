from sys import exit
import pygame


def level_picker(level, button_clicks, new_levels):


  levels = [[[0, 0, 0, 0, 0, 9, 9, 0, 0, 0, 0, 0,8,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,8,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,8,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,8,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,8,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,8]],  # 0

            [[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 9 ,8
                  , 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1 ,8
                  , 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,8
                  , 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,8
                  , 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0,8
                  , 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,8]],  # 1

            [[0, 1, 9, 9, 0, 0, 0, 0, 0, 0, 0, 1,8,
              0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1,8,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,8,
              0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1,8,
              0, 1, 0, 0, 0, 0, 0, 9, 1, 0, 0, 1,8,
              0, 1, 9, 0, 0, 0, 0, 0, 0, 0, 0, 1,8]],  # 2

            [[0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 9,8,
              0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0,8,
              0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0,8,
              0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0,8,
              1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0,8,
              9, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0,8]],  # 3

            [[0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 9,8,
              0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0,8,
              1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0,8,
              1, 1, 2, 0, 0, 0, 1, 0, 0, 1, 1, 1,8,
              9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,8,
              1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1,8]],  # 4

            [[0, 1, 1, 2, 2, 0, 0, 0, 0, 0, 0, 9,8,
              0, 1, 1, 1, 2, 0, 0, 0, 1, 2, 1, 1,8,
              0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,8,
              0, 1, 0, 0, 1, 1, 1, 2, 0, 0, 1, 2,8,
              0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 2,8,
              0, 0, 0, 0, 0, 1, 9, 0, 0, 1, 1, 2,8]],  # 5

            [[0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 9,8,
              0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,8,
              0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0,8,
              0, 2, 0, 1, 9, 2, 2, 2, 1, 0, 2, 0,8,
              0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0,8,
              0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1,8]],  # 6

            [[0, 1, 2, 0, 0, 0, 0, 0, 1, 0, 0, 1,8,
              0, 1, 2, 0, 1, 1, 0, 0, 0, 0, 0, 1,8,
              0, 1, 1, 0, 2, 2, 1, 0, 0, 1, 0, 1,8,
              0, 0, 0, 0, 0, 2, 2, 2, 1, 9, 9, 9,8,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 9, 9,8,
              1, 1, 2, 2, 0, 0, 0, 0, 0, 0, 1, 1,8]],  # 7

            [[0, 1, 1, 1, 1, 2, 1, 2, 2, 2, 2, 2,8,
              0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 9,8,
              0, 0, 0, 1, 0, 2, 0, 1, 1, 0, 0, 9,8,
              0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 9,8,
              1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 9,8,
              1, 1, 2, 0, 0, 1, 0, 0, 2, 2, 2, 1,8, ]],  # 8

            [[0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 9,8,
              1, 1, 2, 2, 0, 0, 0, 2, 2, 2, 2, 0,8,
              0, 0, 1, 2, 0, 0, 0, 0, 2, 1, 1, 0,8,
              0, 0, 0, 0, 2, 2, 0, 0, 2, 1, 0, 0,8,
              0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,8,
              9, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1,8]],  # 9

            [[0, 0, 0, 0, 1, 9, 0, 0, 2, 1, 0, 2,8,
              1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 2,8,
              2, 9, 2, 0, 0, 0, 1, 0, 0, 0, 0, 2,8,
              2, 0, 2, 1, 0, 0, 0, 1, 1, 1, 0, 2,8,
              2, 0, 2, 2, 1, 0, 0, 0, 0, 0, 0, 2,8,
              0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 2,8]],  # 10

            [[0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 9,8,
              0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0,8,
              0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0,8,
              0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,8,
              0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,8,
              2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2,8]],  # 11

            [[0, 0, 1, 0, 0, 9, 9, 0, 0, 1, 0, 9,8,
              0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0,8,
              0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0,8,
              0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0,8,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,8,
              2, 2, 2, 1, 0, 0, 0, 0, 1, 2, 2, 2,8]],  # 12

            [[0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 9, 2,8,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 2,8,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 2,8,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 2,8,
              1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 2,8,
              2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9, 2,8]],  # 13

            [[0, 1, 2, 1, 0, 0, 0, 0, 0, 1, 1, 1,8
                  , 0, 1, 2, 0, 0, 2, 1, 1, 0, 0, 0, 0
                  , 8,0, 1, 1, 0, 1, 1, 0, 0, 1, 2, 2, 0
                  , 8,0, 2, 0, 0, 0, 0, 0, 0, 2, 9, 2, 0
                  , 8,0, 0, 1, 1, 1, 1, 1, 0, 2, 0, 2, 0
                  , 8,0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0]],  # 14

            [[0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0,8,
                0, 1, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0,8,
                  0, 2, 1, 9, 2, 1, 0, 0, 0, 0, 0, 9,8,
                    0, 2, 9, 9, 2, 0, 0, 0, 0, 2, 9, 9,8,
                      0, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 9,8,
                        0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2,8]], #15

            [[0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2,8
                  , 0, 0, 0, 2, 2, 0, 1, 1, 2, 0, 2, 2
                  ,8, 0, 0, 0, 0, 2, 0, 0, 1, 2, 0, 1, 2
                  ,8, 2, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0
                  ,8, 2, 2, 0, 0, 0, 0, 2, 0, 2, 1, 2, 0
                  ,8, 2, 2, 2, 0, 0, 0, 0, 0, 1, 2, 2, 9]],  # 16

            [[0, 1, 0, 2, 2, 0, 0, 2, 2, 2, 2, 2,8,
              0, 0, 0, 2, 2, 0, 0, 2, 2, 2, 2, 2,8,
              0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 9,8,
              0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 9,8,
              0, 2, 0, 2, 2, 0, 0, 0, 0, 0, 0, 2,8,
              0, 1, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2,8]],  # 17


            [   
                [0, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1,8,
                  0, 2, 1, 2, 1, 1, 0, 0, 0, 1, 1, 1,8,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,8,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,8,
                  1, 2, 2, 1, 1, 0, 5, 0, 0, 1, 1, 1,8,
                  1, 1, 2, 2, 2, 0, 1, 0, 0, 1, 0, 9,8, ],#18-1
                
                [0, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1,8,
                  0, 2, 1, 2, 1, 1, 0, 0, 0, 1, 1, 1,8,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,8,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,8,
                  1, 2, 2, 1, 1, 0, 0, 0, 0, 1, 1, 1,8,
                  1, 1, 2, 2, 2, 0, 1, 0, 0, 0, 0, 9, 8,]#18-2
            ],
          [# 17
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,8,
                  0, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1,8,
                  0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 9,8,
                  0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 9,8,
                  5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8,],#17-1
                
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,8,
                  0, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1,8,
                  0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 9,8,
                  0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 9,8,
                  0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8,],#17-2
              
              [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,8,
                  0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1,8,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9,8,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9,8,
                  0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,8, ]#17-3
            ],
            [ #18
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,8,
                  0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,8,
                  0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,8,
                  0, 0, 0, 5, 1, 1, 1, 1, 1, 1, 1, 1,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9,8, ],  # 18-1
                
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,8,
                  1, 1, 1, 0, 0, 4, 1, 1, 1, 1, 1, 1,8,
                  1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1,8,
                  1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 8,],  # 18-2
                
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,8,
                  1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,8,
                  1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1,8,
                  1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1,8,
                  1, 1, 1, 6, 0, 0, 1, 1, 1, 1, 1, 1,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9,8,],  # 18-3
                
                [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1,8,
                  1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1,8,
                  1, 1, 1, 1, 1, 0, 0, 2, 0, 0, 1, 1,8,
                  1, 1, 1, 1, 1, 0, 0, 2, 1, 0, 1, 1,8,
                  1, 1, 1, 0, 0, 0, 2, 2, 1, 5, 1, 1,8,
                  1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 9, 8,],  # 18-4
                
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 8,],  # 18-5
                
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 8,],  # 18-6
                
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,8,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 8,]  # 18-7
            ],
            
            [[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,8,
                0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 4, 1,8,
                  0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 1,8,
                    0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,8,
                      1, 0, 2, 2, 1, 0, 0, 0, 0, 2, 2, 1,8,
                        1, 1, 2, 9, 1, 1, 1, 1, 1, 1, 1, 1,8],
            [0, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1,8,
              0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,8,
                0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 1,8,
                  1, 0, 0, 1, 0, 0, 0, 0, 2, 2, 0, 1,8,
                    1, 1, 0, 2, 1, 0, 0, 4, 1, 2, 2, 1,8,
                      1, 1, 2, 9, 1, 1, 1, 1, 1, 1, 1, 1,8],
            [0, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1,8,
              0, 1, 0, 0, 0, 2, 0, 2, 0, 0, 0, 1,8,
                0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 1,8,
                  1, 0, 0, 2, 2, 0, 0, 0, 2, 2, 0, 1,8,
                    1, 1, 0, 2, 0, 0, 0, 0, 1, 2, 2, 2,8,
                      1, 1, 2, 9, 0, 0, 0, 1, 1, 1, 2, 2,8]],#19
            
            [[0, 1, 6, 0, 1, 1, 0, 0, 0, 0, 0, 2,8,
                0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,8,
                  0, 2, 1, 0, 0, 0, 1, 1, 1, 2, 0, 0,8,
                    0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0,8,
                      0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0,8,
                        2, 0, 0, 0, 0, 0, 0, 2, 1, 9, 9, 9,8],
              
              [ 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2,8,
                0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,8,
                0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 0, 0,8,
                0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0,8,
                0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0,8,
                1, 0, 0, 0, 0, 0, 0, 2, 1, 9, 9, 9,8]],#20
            [
                
#START BIG_LEVELS©®

[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8,
 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 8,
 0, 1, 0, 0, 0, 1, 1, 9, 9, 1, 0, 0, 8,
 0, 1, 0, 0, 0, 1, 9, 9, 9, 1, 0, 0, 8,
 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 8,
 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 8,
 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 8,
 1, 0, 1, 2, 0, 0, 0, 0, 0, 0, 1, 0, 8,
 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 1, 0, 8,
 0, 0, 0, 1, 1, 2, 2, 2, 2, 1, 0, 0, 8,
 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8,
 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, ],#23
],
#             [
# [0, 0, 0, 0, 1, 9, 0, 0, 0, 0, 1, 1, 8, 0, 0, 0, 0, 1, 2, 2, 2, 0, 0, 0, 1, 8, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 8, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 8, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 8, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 8, 2, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 8, 1, 1, 0, 0, 2, 2, 2, 2, 0, 0, 0, 1, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 8, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 8, ],#24
# ],

[
[0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 3, 8, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 1, 8, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 1, 8, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 8, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 8, 1, 1, 2, 0, 0, 2, 1, 1, 1, 1, 1, 1, 8, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 4, 1, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, ],
[0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 8, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 1, 8, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 1, 8, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 8, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 8, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 8, 1, 1, 2, 0, 0, 2, 1, 1, 1, 1, 1, 1, 8, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 4, 1, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, ],
[0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 8, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 1, 8, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 1, 8, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 8, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 8, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 8, 1, 1, 2, 0, 0, 2, 1, 1, 1, 1, 1, 1, 8, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 8, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 8, 9, 9, 9, 9, 0, 0, 9, 9, 9, 9, 9, 9, 8, 1, 1, 1, 1, 9, 9, 1, 1, 1, 1, 1, 1, 8, ],#25
],
[
    [0, 0, 0, 8,
     0, 0, 0, 8,
     1, 1, 0, 8,
     0, 1, 0, 8,
     0, 0, 0, 8, 
     0, 0, 0, 8,
     0, 0, 1, 8,
     0, 1, 1, 8,
     0, 0, 0, 8,
     0, 0, 0, 8,
     0, 0, 0, 8,
     1, 0, 0, 8,
     1, 1, 0, 8,
     1, 1, 0, 8,
     0, 1, 0, 8,
     0, 1, 0, 8,
     0, 0, 0, 8,
     0, 0, 0, 8,
     0, 0, 0, 8,
     0, 1, 0, 8,
     0, 1, 1, 8,
     0, 1, 0, 8,
     0, 1, 0, 8,
     0, 0, 0, 8,
     0, 0, 0, 8,
     1, 0, 0, 8,
     1, 1, 0, 8,
     1, 0, 0, 8,
     1, 0, 0, 8,
     1, 0, 0, 8,
     1, 0, 1, 8,
     0, 0, 1, 8,
     0, 0, 1, 8,
     0, 1, 1, 8,
     0, 1, 9, 8,
     0, 1, 0, 8,
     0, 0, 0, 8,
     0, 0, 0, 8,
     1, 0, 0, 8,
     1, 1, 1, 8,]
],#26
[
[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 1, 1, 0, 0, 0, 2, 2, 2, 8, 1, 1, 1, 0, 0, 0, 1, 1, 1, 2, 9, 2, 8, 0, 0, 0, 1, 2, 0, 0, 2, 1, 2, 0, 2, 8, 0, 0, 1, 0, 1, 2, 0, 2, 2, 2, 0, 2, 8, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8,  ],
],#27
            ]

  if level >= len(levels) and level <= 900:
      pygame.quit()
      exit()
  elif level >= 999:
      num_list = new_levels[button_clicks]
      
  else:
      num_list = levels[level][button_clicks]

  return num_list

