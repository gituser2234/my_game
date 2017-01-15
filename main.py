# -*- coding: utf-8 -*-
"""

"""

import pygame
import sys
import settings as sett
from sprites import Player, Obstacle, Mob, Item, Finish
from tilemap import Camera, TiledMap
from os import path
vec = pygame.math.Vector2

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
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'img')
        self.map_folder = path.join(self.game_folder, 'maps')
        
        # Load img data
        # Scale due to huge dimensions
        self.player_img = pygame.image.load(path.join(self.img_folder, sett.PLAYER_IMG)).convert_alpha()
        self.player_img = pygame.transform.scale(self.player_img, (sett.TILESIZE, sett.TILESIZE))
        
        self.background_img = pygame.image.load(path.join(self.img_folder, sett.BG_IMAGE)).convert()
        self.background_rect = self.background_img.get_rect()
        
        # Load items
        self.item_images = {}
        for item in sett.ITEM_IMAGES:
            self.item_images[item] = pygame.image.load(path.join(self.img_folder, sett.ITEM_IMAGES[item])).convert_alpha()
            self.item_images[item] = pygame.transform.scale(self.item_images[item], (sett.TILESIZE * 3 // 4, sett.TILESIZE * 3 // 4))
        
        # Prepare map data
        self.map_data = []
        chosen_map = 'map1.tmx'
        
        # Load chosen map
        self.load_map(chosen_map)
            
            
    def load_map(self, chosen_map):
        self.map = TiledMap(path.join(self.map_folder, chosen_map))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        
        # Initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
       
        # Placing objects from map
        for tile_object in self.map.tmxdata.objects:
            # To spawn our object in the center of the object in map, not in left upper corner
            obj_center = vec(tile_object.x + tile_object.width // 2, tile_object.y + tile_object.height // 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            elif tile_object.name == 'zombie':
                Mob(self, obj_center.x, obj_center.y)
            elif tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            elif tile_object.name in ['coin_gold']:
                Item(self, obj_center, tile_object.name)
            elif tile_object.name == 'finish':
                self.finish = Finish(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)  
        
        self.camera = Camera(self.map.width, self.map.height)
        
        
    def new(self):
        # Debug mode
        self.draw_debug = True
        if self.draw_debug:
            self.font = pygame.font.SysFont('Calibri', 35, True, False)
        
    
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
        
        # Player hits items
        hits = pygame.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.item_type == 'coin_gold':
                hit.kill()
                
        # Player hits finish
        hits = pygame.sprite.collide_rect(self.player, self.finish)
        if hits:
            chosen_map = 'map2.tmx'
            self.load_map(chosen_map)
            
        
    def draw_grid(self):
        for x in range(0, sett.WIDTH, sett.TILESIZE):
            pygame.draw.line(self.screen, sett.LIGHTGREY, (x, 0), (x, sett.HEIGHT))
        for y in range(0, sett.HEIGHT, sett.TILESIZE):
            pygame.draw.line(self.screen, sett.LIGHTGREY, (0, y), (sett.WIDTH, y))
    
    def draw(self):
        # Display FPS
        pygame.display.set_caption("{:.0f}".format(self.clock.get_fps()))
        
        # Draw things
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        
        #self.screen.fill(sett.BGCOLOR)
        #self.draw_grid()
        
        # Draw every sprite
        for sprite in self.all_sprites:
            # self.camera.apply(sprite) returns sprite rectangle shifted by 
            # camera topleft (which is shifted by player's position)
            # So the line blits sprite.image in shifted rectangle
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            
        if self.draw_debug:
            text = self.font.render("vel="+str(self.player.vel), True, sett.BLACK)
            self.screen.blit(text, [20, 20])
            
        # Finish drawing
        pygame.display.flip()
        
    def events(self):
        # Catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                
    def next_level(self):
        pass            
                
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