# -*- coding: utf-8 -*-

import pygame
import sys
import settings as sett
from sprites import Player, Obstacle, Mob, Item, Finish, Lava, FallingItem
from tilemap import Camera, TiledMap
from os import path
vec = pygame.math.Vector2

# TODO:
# MERGE LAVAS AND FALLING ITEMS INTO ONE GAME OVER GROUP

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
        # Folders' paths
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'img')
        self.map_folder = path.join(self.game_folder, 'maps')
        self.music_folder = path.join(self.game_folder, 'music')
        self.sound_folder = path.join(self.game_folder, 'sound')
        
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
            
        # Load HUD
        self.hud_x = pygame.image.load(path.join(self.img_folder, sett.HUD_X)).convert_alpha()
        
        self.hud_digits = []
        for digit in sett.HUD_DIGITS:
            self.hud_digits.append(pygame.image.load(path.join(self.img_folder, digit)).convert_alpha())
            
        self.hud_images = {}
        for image in sett.HUD_IMAGES:
            self.hud_images[image] = pygame.image.load(path.join(self.img_folder, sett.HUD_IMAGES[image])).convert_alpha()
        
        # Prepare map data
        self.map_data = []
        self.map_nr = 0
        self.chosen_map = sett.MAP_LIST[self.map_nr]
        
        # Load music
        pygame.mixer.music.load(path.join(self.music_folder, sett.BG_MUSIC))
        pygame.mixer.music.play(loops=-1)
        
        # Load sounds
        self.sound_effects = {}
        for sound_type in sett.SOUND_EFFECTS:
            self.sound_effects[sound_type] = pygame.mixer.Sound(path.join(self.sound_folder, sett.SOUND_EFFECTS[sound_type]))
        
        # Load chosen map
        self.load_map(self.chosen_map)
            
    def load_map(self, chosen_map):
        self.map = TiledMap(path.join(self.map_folder, chosen_map))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        # Initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.lavas = pygame.sprite.Group()
        self.fallings = pygame.sprite.Group()
        self.fallings_list = []
        self.points = 0
       
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
            elif tile_object.name == 'lava':
                Lava(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            elif tile_object.name == 'weight':
                falling = FallingItem(self, obj_center.x, obj_center.y, tile_object.name)
                self.fallings_list.append(falling)
        
        self.camera = Camera(self.map.width, self.map.height)
        
    def new(self):
        # Debug mode
        self.draw_debug = False
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
        
        # Player activates weight
        for falling_item in self.fallings_list:
            if self.player.rect.top > falling_item.rect.bottom:
                if self.player.rect.right >= falling_item.rect.left and\
                   self.player.rect.right <= falling_item.rect.right or\
                   self.player.rect.left >= falling_item.rect.left and\
                   self.player.rect.left <= falling_item.rect.right:
                    falling_item.fall = True
        
        # Player hits items
        hits = pygame.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.item_type == 'coin_gold':
                self.sound_effects['coin_gathered'].play()
                self.points += 1
                hit.kill()
                
        # Player hits lava
        hits = pygame.sprite.spritecollide(self.player, self.lavas, False)
        if hits:
            self.load_map(self.chosen_map)
                
        # Player hits finish
        hits = pygame.sprite.collide_rect(self.player, self.finish)
        if hits:
            self.sound_effects['lvl_complete'].play()
            self.map_nr += 1
            
            if self.map_nr >= len(sett.MAP_LIST):
                self.show_game_over_screen()
            else:
                chosen_map = sett.MAP_LIST[self.map_nr]
                self.load_map(chosen_map)
                        
    
    def draw_hud(self):
        # DRAMATIC CODE, NEEDS TO BE IMPROVED
        image_rect = self.hud_digits[self.points].get_rect()
        image_rect.centery = 25
        self.screen.blit(self.hud_digits[self.points], [10, image_rect.y])
        image_rect = self.hud_x.get_rect()
        image_rect.centery = 25
        self.screen.blit(self.hud_x, [40, image_rect.y])
        #image_rect = self.hud_images['hud_coin_gold'].get_rect()
        #y_offset = image_rect.height
        self.screen.blit(self.hud_images['hud_coin_gold'], [70, 10])
    
    def draw(self):
        # Display FPS
        pygame.display.set_caption("{:.0f}".format(self.clock.get_fps()))
        
        # Draw things
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
    
        # Draw every sprite
        for sprite in self.all_sprites:
            # self.camera.apply(sprite) returns sprite rectangle shifted by 
            # camera topleft (which is shifted by player's position)
            # So the line blits sprite.image in shifted rectangle
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        
        self.draw_hud()
            
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