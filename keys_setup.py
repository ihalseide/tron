#!/usr/bin/env python3

import pygame


class KeysSetup:

    def __init__(self, up, right, down, left, stop=None):
        self.up = up
        self.right = right
        self.down = down
        self.left = left
        self.stop = stop

        self.all = [self.up, self.right, self.down, self.left, self.stop]


# default key usages
KeysSetup.arrows = KeysSetup(pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN,
                       pygame.K_LEFT)
KeysSetup.wasd = KeysSetup(pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a)
KeysSetup.tfgh = KeysSetup(pygame.K_t, pygame.K_h, pygame.K_g, pygame.K_f)
KeysSetup.pl = KeysSetup(pygame.K_p, pygame.K_QUOTE, pygame.K_SEMICOLON,
                   pygame.K_l)
KeysSetup.ijkl = KeysSetup(pygame.K_i, pygame.K_l, pygame.K_k, pygame.K_j)
