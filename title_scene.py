#!/usr/bin/env python3

import pygame
from base_scene import BaseScene
from game_scene import GameScene


class TitleScene(BaseScene):

	def __init__(self):
		super().__init__()
		
		pygame.font.init()
		my_font = pygame.font.SysFont("Courier Bold", 50)
		
		self.buttons = pygame.sprite.Group()
		self.background = pygame.sprite.Group()
		
		play_button = pygame.sprite.Sprite(self.buttons)
		play_button.rect = pygame.Rect(180, 150, 150, 55)
		play_button.image = pygame.Surface(play_button.rect.size)
		play_button.image.fill(pygame.color.THECOLORS['orange'])
		play_button.image.fill(pygame.color.THECOLORS['blue'], play_button.rect.inflate(-5, -5))
		play_button.image.blit(my_font.render("Play", 1, pygame.color.THECOLORS['orange']), (30, 15))		

	def process_inputs(self, events, keys):
		pass

	def update(self):
		pass

	def display(self, screen):
		self.background.draw(screen)
		self.buttons.draw(screen)