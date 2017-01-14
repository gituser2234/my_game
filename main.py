# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 21:26:31 2017

@author: anonymous
"""

import pygame
import sys
import settings as sett
from os import path

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Set screen properties
        self.screen = pygame.display.set_mode([sett.WIDTH, sett.HEIGHT])
        pygame.display.set_caption(sett.TITLE)
        self.clock = pygame.time.Clock()
        
        self.load_data()
        
    def load_data(self):
        game_folder = path.dirname(__file__)
        
        
    def new(self):
        # Initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
    
    def run(self):
        # Game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            # Delta time
            self.dt = self.clock.tick(sett.FPS) / 1000
            self.events()
            self.update()
            self.draw()
            
    def quit(self):
        pygame.quit()
        sys.exit()
        
    def update(self):
        # Update portion of game loop
        pass
    
    def draw(self):
        self.screen.fill(sett.BGCOLOR)
        pygame.display.flip()
        
    def events(self):
        # Catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                
    def show_start_screen(self):
        pass
    
    def show_game_over_screen(self):
        pass
    
    
# Create the game object
game = Game()
game.show_start_screen()
while True:
    game.new()
    game.run()
    game.show_game_over_screen()