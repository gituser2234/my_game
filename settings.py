# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 21:21:55 2017

@author: anonymous
"""

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# GAME SETTINGS
WIDTH = 800
HEIGHT = 640
FPS = 60
TITLE = "TAKA GIERKA"
BGCOLOR = DARKGREY
BG_IMAGE = 'background.jpg'

TILESIZE = 32
GRIDWIDTH = WIDTH // TILESIZE
GRIDHEIGHT = HEIGHT // TILESIZE

# PLAYER SETTINGS
PLAYER_SPEED = 300
PLAYER_ACC = 0.7
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.76
PLAYER_IMG = 'player.png' 

# MOB SETTINGS
MOB_IMG = 'zoimbie1_hold.png'
MOB_SPEED = 150

# LAYERS
WALL_LAYER = 1
PLAYER_LAYER = 2
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# ITEMS
ITEM_IMAGES = {'health': 'health_pack.png',
               'coin_gold': 'coinGold.png'}
BOB_RANGE = 15
BOB_SPEED = 0.38