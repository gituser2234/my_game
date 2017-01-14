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
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        
        # Vectors
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * sett.TILESIZE
        
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
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        # self.hit_rect = MOB_HIT_RECT.copy() IN ORIGINAL
        self.pos = vec(x, y) * sett.TILESIZE
        self.vel = vec(0, 0)
        self.rect.center = self.pos
        
    #def update(self)

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        # Member of all sprites and walls groups
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface([sett.TILESIZE, sett.TILESIZE])
        self.image.fill(sett.GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * sett.TILESIZE
        self.rect.y = y * sett.TILESIZE