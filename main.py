# -*- coding: utf-8 -*-
"""

"""

import pygame
import sys
import settings as sett
from sprites import Player, Wall, Mob
from tilemap import Map, Camera
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
        # Game folder path
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        
        # Load map data
        self.map_data = []
        self.map = Map(path.join(game_folder, 'map3.txt'))
        
        # Load img data
        # Scale due to huge dimensions
        self.player_img = pygame.image.load(path.join(img_folder, sett.PLAYER_IMG)).convert_alpha()
        self.player_img = pygame.transform.scale(self.player_img, (sett.TILESIZE, sett.TILESIZE))
        self.mob_img = pygame.image.load(path.join(img_folder, sett.MOB_IMG)).convert_alpha()
        self.mob_img = pygame.transform.scale(self.mob_img, (sett.TILESIZE, sett.TILESIZE))
        
    def new(self):
        # Initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
       
        # Spawning walls
        # enumerate makes row as index, example:
        # l = ['a', 'b', 'c', 'd']
        # for index, item in enumerate(l):
        #   print(index, item)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                elif tile == 'P':
                    # Spawn player
                    self.player = Player(self, col, row)
                elif tile == 'M':
                    Mob(self, col, row)
        
        self.camera = Camera(self.map.width, self.map.height)
        
    
    def run(self):
        # Game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            # Delta time
            self.dt = self.clock.tick(sett.FPS) / 1000
            self.events()
            self.update()
            self.draw()
        
    def update(self):
        # Update portion of game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        
    def draw_grid(self):
        for x in range(0, sett.WIDTH, sett.TILESIZE):
            pygame.draw.line(self.screen, sett.LIGHTGREY, (x, 0), (x, sett.HEIGHT))
        for y in range(0, sett.HEIGHT, sett.TILESIZE):
            pygame.draw.line(self.screen, sett.LIGHTGREY, (0, y), (sett.WIDTH, y))
    
    def draw(self):
        # Display FPS
        pygame.display.set_caption("{:.0f}".format(self.clock.get_fps()))
        
        # Draw things
        self.screen.fill(sett.BGCOLOR)
        #self.draw_grid()
        
        # Draw every sprite
        for sprite in self.all_sprites:
            # self.camera.apply(sprite) returns sprite rectangle shifted by 
            # camera topleft (which is shifted by player's position)
            # So the line blits sprite.image in shifted rectangle
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            
        # Finish drawing
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
    
    def quit(self):
        pygame.quit()
        sys.exit()
    
    
# Create the game object
game = Game()
game.show_start_screen()
while True:
    game.new()
    game.run()
    game.show_game_over_screen()