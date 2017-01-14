# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 21:58:44 2017

@author: anonymous
"""

import pygame
import settings as sett

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                # strip() deletes newline characters
                self.data.append(line.strip())
                
        # How many tiles wide/high is map
        self.titlewidth = len(self.data[0])
        self.titleheight = len(self.data)
        self.width = self.titlewidth * sett.TILESIZE
        self.height = self.titleheight * sett.TILESIZE
    
class Camera:
    def __init__(self, width, height):
        # As we can see camera is just a Rectangle
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        
    def apply(self, entity):
        # move() gives new rectangle shifted by amount of an argument
        return entity.rect.move(self.camera.topleft)
        
    def update(self, target):
        # We wanted centered on the screen
        x = -target.rect.x + (sett.WIDTH // 2)
        y = -target.rect.y + (sett.HEIGHT // 2)
        
        # Limit scrolling to map size
        x = min(0, x) # left
        y = min(0, y) # top
        x = max(-(self.width - sett.WIDTH), x) # right
        y = max(-(self.height - sett.HEIGHT), y) # bottom
        self.camera = pygame.Rect(x, y, self.width, self.height)