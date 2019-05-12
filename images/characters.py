player_1 = ['images/pack/Characters/Player/player_tilesheet.png',
          [(0,111, 80,110),
           (0,0, 80,110),  # move
           (81,111, 80,110),
           (0,0, 80,110)],
          (0,0, 80,110),  # stay
          (81,0, 80,110),  # jump
          (161,111, 80,110),  # fire
          (0, 0),  # scale image(size)
          (-30, -30)  # shift image
          ]

player_mario_classic = ['images/pack/Characters/Player/Super_Mario.png',
          [(80+17*1,1, 16,32),
           (80+17*2,1, 16,32),  # move
           (80+17*3,1, 16,32)],
          (80,1, 16,32),  # stay
          (80+17*5,1, 16,32),  # jump
          (80+17*8,1, 16,32),  # fire
          (50,80),  # scale image(size)
          (0, 0)  # shift image
          ]

player_mario_classic_small = ['images/pack/Characters/Player/Super_Mario.png',
          [(80+17*1,34, 16,16),
           (80+17*2,34, 16,16),  # move
           (80+17*3,34, 16,16)],
          (80,34, 16,16),  # stay
          (80+17*5,34, 16,16),  # jump
          (80+17*8,34, 16,16),  # fire
          (50,50),  # scale image(size)
          (-16, 0)  # shift image
          ]

player_mario_fire = ['images/pack/Characters/Player/Super_Mario.png',
          [(80+17*1,129, 16,32),
           (80+17*2,129, 16,32),  # move
           (80+17*3,129, 16,32)],
          (80,129, 16,32),  # stay
          (80+17*5,129, 16,32),  # jump
          (80+17*8,129, 16,32),  # fire
          (50,80),  # scale image(size)
          (0, 0)  # shift image
          ]

player_mario_fire_small = ['images/pack/Characters/Player/Super_Mario.png',
          [(80+17*1,162, 16,16),
           (80+17*2,162, 16,16),  # move
           (80+17*3,162, 16,16)],
          (80,162, 16,16),  # stay
          (80+17*5,162, 16,16),  # jump
          (80+17*8,162, 16,16),  # fire
          (50,50),  # scale image(size)
          (-16, 0)  # shift image
          ]


player_list = [player_1,
               player_mario_classic,
               player_mario_classic_small,
               player_mario_fire,
               player_mario_fire_small]
