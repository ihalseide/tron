#!/usr/bin/env python3

import pygame
import math
import random

from constants import *
from keys_setup import KeysSetup
from base_scene import BaseScene


class Trail(pygame.sprite.Sprite):

	def __init__(self, game, x, y, color):
		pygame.sprite.Sprite.__init__(self)

		self.game = game
		self.color = color

		self.image = pygame.Surface((self.game.tile_size, self.game.tile_size))

		self.rect =self.image.get_rect()

		self.image.fill(self.color)
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
		
		
class GameScene(BaseScene):

	@staticmethod
	def fill_board(dimensions, value=None):
		# create a row variable so that one is created every time a row 
		# is needed
		a_row = list([value for x in range(dimensions[0])])
		return list([a_row for x in range(dimensions[1])])


	def __init__(self, players=2):
		super().__init__()

		# check args
		if players > 4 or players < 2:
			raise ValueError("num. of players must be: 2 <= n <= 4")

		
		# specific to each game
		self.num_of_players = players
		self.board_size = (50, 50)
		self.tile_size = 10

		# graphics
		self.line_color = (0, 255, 0)
		pygame.font.init()
		self.the_font = pygame.font.SysFont("Courier New", 80)
		self.game_over_text = self.the_font.render("GAME OVER", 1,
												   (255, 255, 255))
		self.the_font = pygame.font.SysFont("Courier New", 50)

		self.win_text = None

		# physics
		self.bikes = pygame.sprite.Group()
		self.trails = pygame.sprite.Group()

		# spawn the players
		spawns = []
		if self.num_of_players >= 1:
			b = Bike(self, "P1",
						   self.board_size[0] // 4 * self.tile_size,
						   self.board_size[1] // 2 * self.tile_size,
						   RIGHT, (255, 0, 0), KeysSetup.wasd)
			spawns.append(b)
		
		if self.num_of_players >= 2:
			b = Bike(self, "P2",
						   self.board_size[0] // 4 * 3 * self.tile_size,
						   self.board_size[1] // 2 * self.tile_size,
						   LEFT, (0, 0, 255), KeysSetup.ijkl)
			spawns.append(b)

		if self.num_of_players >= 3:
			b = Bike(self, "P3",
						   self.board_size[0] // 2 * self.tile_size,
						   self.board_size[1] // 4 * 3 * self.tile_size,
						   UP, (255, 255, 0), KeysSetup.arrows)
			spawns.append(b)

		if self.num_of_players == 4:
			b = Bike(self, "P4",
						   self.board_size[0] // 2 * self.tile_size,
						   self.board_size[1] // 4 * self.tile_size,
						   DOWN, (0, 255, 255), KeysSetup.arrows)
			spawns.append(b)

		self.bikes.add(spawns)


	def process_inputs(self, events, keys):
		if len(self.bikes.sprites()) > 1:
			for b in self.bikes.sprites():
				b.process_inputs(events, keys)
		else:
			if keys[pygame.K_SPACE]:
				self.next = GameScene(self.num_of_players)

	
	def update(self):
		if len(self.bikes.sprites()) > 1:
			self.bikes.update()
		else:
			pass
		#self.trails.update() not needed for now


	def display_background(self, screen):
		first_x = screen.get_rect().x
		first_y = screen.get_rect().y
		last_x = screen.get_rect().width
		last_y = screen.get_rect().height

		for row in range(self.board_size[1]):
			# horizontal lines
			pygame.draw.line(screen, self.line_color, (first_x, first_y + row * self.tile_size), first_x + last_x, first_y + row * self.tile_size, 1)
		for col in range(self.board_size[0]):
			# vertical lines
			pygame.draw.line(screen, self.line_color, (first_x + col * self.tile_size, first_y), (first_x + col * self.tile_size, first_y + last_y), 1)

		# draw the bottom and right lines
		pygame.draw.line(screen, self.line_color, (first_x, first_y + last_y), (first_x + last_x, first_y + last_y), 1)
		pygame.draw.line(screen, self.line_color, (first_x + last_x, first_y), (first_x + last_x, first_y + last_y), 1)


	def display_game_over(self, screen):
		screen.blit(self.game_over_text,(0, 0))
		if not self.win_text:
			try:
				winner = self.bikes.sprites()[0]
				self.win_text = self.the_font.render("%s WINS!" %(winner), 1, winner.color)
			except IndexError:
				self.win_text = self.the_font.render("NO WINNER", 1, (255, 255, 255))
		screen.blit(self.win_text, (10, screen.get_rect().height * 1/7))


	def display(self, screen):
		screen.fill((0, 0, 0))
		self.trails.draw(screen)
		self.bikes.draw(screen)
		if not len(self.bikes.sprites()) > 1:
			self.display_game_over(screen)


	def is_in_bounds(self, rect):
		full = pygame.Rect(0, 0, self.board_size[0] * self.tile_size, self.board_size[1] * self.tile_size)
		return full.contains(rect)