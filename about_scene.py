#!/usr/bin/env python3

import pygame
from base_scene import BaseScene


class AboutScene(SceneBase):

    def __init__(self):
        super().__init__()

        pygame.font.init()

        self.font = pygame.font.SysFont("Courier New", 20)
        self.label = self.font.render("Hi", 1, (0, 255, 0))


    def display(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.label, (20, 20))


    def update(self):
        pass
		