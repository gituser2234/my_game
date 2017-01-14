# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 21:33:56 2017

@author: anonymous
"""

import pygame
import settings as sett
vec = pygame.math.Vector2


def collide_with_walls(sprite, group, direction):
    if direction == 'x':
        hits = pygame.sprite.spritecollide(sprite, group, False)
        if hits:
            if sprite.vel.x > 0:
                # sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2 IN ORIGINAL
                sprite.pos.x = hits[0].rect.left - sprite.rect.width
            elif sprite.vel.x < 0:
                # sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2 IN ORIGINAL
                sprite.pos.x = hits[0].rect.right
                
            # if we hit, then we stop
            sprite.vel.x = 0
            sprite.rect.x = sprite.pos.x
            
    if direction == 'y':
        hits = pygame.sprite.spritecollide(sprite, group, False)
        if hits:
            if sprite.vel.y > 0:
                # sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2 IN ORIGINAL
                sprite.pos.y = hits[0].rect.top - sprite.rect.height
            elif sprite.vel.y < 0:
                # sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2 IN ORIGINAL
                sprite.pos.y = hits[0].rect.bottom
                
            # if we hit, then we stop
            sprite.vel.y = 0
            sprite.rect.y = sprite.pos.y
            

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = sett.PLAYER_LAYER
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Vectors
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        
    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vel.x = -sett.PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.vel.x = sett.PLAYER_SPEED
        if keys[pygame.K_UP]:
            self.vel.y = -sett.PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.vel.y = sett.PLAYER_SPEED
            
        # if running diagonal to avoid speed-up
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
        
    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.rect.y = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        
        
class Mob(pygame.sprite.Sprite):
    # MOB NEEDS TO BE CAREFULLY COMPLETED FROM SCRATCH
    def __init__(self, game, x, y):
        # Member of all sprites and mob groups
        self._layer = sett.MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # self.hit_rect = MOB_HIT_RECT.copy() IN ORIGINAL
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.rect.center = self.pos
    #def update(self)

    
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        # Member of all sprites groups and walls groups (???)
        self.groups = game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
        
class Item(pygame.sprite.Sprite):
    def __init__(self, game, pos, item_type):
        self._layer = sett.ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[item_type]
        self.rect = self.image.get_rect()
        self.item_type = item_type
        self.rect.center = pos