#!python3

import pygame
import math
import random
import xmath



UP = 1
DOWN = -1
RIGHT = 2
LEFT = -2



def darken(color_tuple, amount=25):
    r = xmath.constrain(color_tuple[0] - amount, 0, 255)
    g = xmath.constrain(color_tuple[1] - amount, 0, 255)
    b = xmath.constrain(color_tuple[2] - amount, 0, 255)
    #print(r, g, b)
    return r, g, b


class Trail(pygame.sprite.Sprite):

    def __init__(self, game, x, y, color):
        pygame.sprite.Sprite.__init__(self)

        self.game = game
        self.color = color

        self.image = pygame.Surface((self.game.tile_size, self.game.tile_size))
        
        self.rect =self.image.get_rect()
        
        self.image.fill(darken(self.color, 50))
        pygame.draw.rect(self.image, self.color, self.rect, 1)

        # set location AFTER drawing on self
        self.rect.x = x
        self.rect.y = y


    def update(self):
        pass



class Bike(pygame.sprite.Sprite):

    def __init__(self, game, name, x, y, dir_, color, key_setup):

        pygame.sprite.Sprite.__init__(self)

        # bike setup
        self.game = game
        self.name = name
        self.direction = dir_
        self.color = color
        self.key_setup = key_setup
        self.ticks = 0

        # sprite setup
        self.image = pygame.Surface((self.game.tile_size, self.game.tile_size))

        self.rect = self.image.get_rect()

        self.image.fill((0, 0, 0))
        pygame.draw.rect(self.image, self.color, self.rect, 1)

        # set location AFTER drawing, (or else drawing won't work)
        self.rect.x = x
        self.rect.y = y


    def process_inputs(self, events, keys):
        
        if keys[self.key_setup.up] and not self.direction == DOWN:
            self.direction = UP
        elif keys[self.key_setup.down] and not self.direction == UP:
            self.direction = DOWN
        elif keys[self.key_setup.left] and not self.direction == RIGHT:
            self.direction = LEFT
        elif keys[self.key_setup.right] and not self.direction == LEFT:
            self.direction = RIGHT
        elif self.key_setup.stop and keys[self.key_setup.stop]:
            self.kill()


    def move(self):
        facing = self.direction
        if facing == UP:
            self.rect.y -= self.game.tile_size
        elif facing == DOWN:
            self.rect.y += self.game.tile_size
        elif facing == RIGHT:
            self.rect.x += self.game.tile_size
        elif facing == LEFT:
            self.rect.x -= self.game.tile_size


    def make_trail(self): 
        new_trail = Trail(self.game, self.rect.x, self.rect.y, self.color)
        self.game.trails.add(new_trail)


    def update(self):

        if self.ticks % 5 == 0:
            # replace prev. location with a trail
            self.make_trail()

            # move and place self on board
            self.move()

        if not self.is_in_bounds() or self.collided():
            self.kill()

        self.ticks += 1
        
        
    def is_in_bounds(self):
        return self.game.is_in_bounds(self.rect)


    def collided(self):
        return pygame.sprite.spritecollideany(self, self.game.trails)


    def __str__(self):
        return self.name


    def __repr__(self):
        return str(self)
            
