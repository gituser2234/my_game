# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 21:33:56 2017

@author: anonymous
"""

import pygame
import settings as sett

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface([sett.TILESIZE, sett.TILESIZE])
        self.image.fill(sett.YELLOW)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * sett.TILESIZE
        self.y = y * sett.TILESIZE
        
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vx = -sett.PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.vx = sett.PLAYER_SPEED
        if keys[pygame.K_UP]:
            self.vy = -sett.PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.vy = sett.PLAYER_SPEED
            
        # if running diagonal to avoid speed-up
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
            
    def collide_with_walls(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                elif self.vx < 0:
                    self.x = hits[0].rect.right
                    
                # if we hit, then we stop
                self.vx = 0
                self.rect.x = self.x
                
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                elif self.vy < 0:
                    self.y = hits[0].rect.bottom
                    
                # if we hit, then we stop
                self.vy = 0
                self.rect.y = self.y
                
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        
        
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