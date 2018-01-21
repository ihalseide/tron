#!python3

# external libs
import pygame
import logging
import random

# internal libs.
import bikes
from keys_setup import KeysSetup
from constants import *



class SceneBase:

    def __init__(self):
        self.next = self


    def process_inputs(self, events, pressed_keys):
        pass


    def update(self):
        pass


    def render(self, screen):
        pass


    def switch_to_scene(self, next_scene):
        self.next = next_scene


    def terminate(self):
        self.switch_to_scene(None)




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


class TitleScene(SceneBase):

    def __init__(self):
        super().__init__()
        
        pygame.font.init()

        # design
        self.spacing = 40
        self.font = pygame.font.SysFont("Courier New", 40)
        self.selected_color = pygame.color.THECOLORS['white']
        self.unselected_color = pygame.color.THECOLORS['blue']
        
        self.options = ["Play Normal", "Play Modified", "About", "Quit"]
        self.needs_update = True
        self.index = 0


    def process_inputs(self, events, keys):
        
        if keys[pygame.K_DOWN]:
            if self.index < len(self.options) - 1:
                self.index += 1
                self.needs_update = True
        elif keys[pygame.K_UP]:
            if self.index > 0:
                self.index -= 1
                self.needs_update = True
        elif keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
            selected = self.options[self.index]
            if selected == "Play Normal":
                self.switch_to_scene(GameScene(2))
            elif selected == "About":
                self.switch_to_scene(AboutScene())
            elif selected == "Play Modified":
                logging.warn('"Play Modified" was selected, \
                             but it doesn\'t exist yet')
            elif selected == "Quit":
                self.terminate()


    def update(self):
        pass


    def display(self, screen):
        if self.needs_update:
            self.needs_update = False

            screen.fill((0, 0, 0))

            for i, opt in enumerate(self.options):
                y = i * self.spacing
                if i == self.index:
                    c = self.selected_color
                else:
                    c = self.unselected_color
                label = self.font.render(opt, 1, c)
                screen.blit(label, (0, y))

        else:
            pass


class GameScene(SceneBase):

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
            b = bikes.Bike(self, "P1",
                           self.board_size[0] // 4 * self.tile_size,
                           self.board_size[1] // 2 * self.tile_size,
                           RIGHT, (255, 0, 0), KeysSetup.wasd)
            spawns.append(b)
        
        if self.num_of_players >= 2:
            b = bikes.Bike(self, "P2",
                           self.board_size[0] // 4 * 3 * self.tile_size,
                           self.board_size[1] // 2 * self.tile_size,
                           LEFT, (0, 0, 255), KeysSetup.ijkl)
            spawns.append(b)

        if self.num_of_players >= 3:
            b = bikes.Bike(self, "P3",
                           self.board_size[0] // 2 * self.tile_size,
                           self.board_size[1] // 4 * 3 * self.tile_size,
                           UP, (255, 255, 0), KeysSetup.arrows)
            spawns.append(b)

        if self.num_of_players == 4:
            b = bikes.Bike(self, "P4",
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
            pygame.draw.line(screen, self.line_color,
                (first_x, first_y + row * self.tile_size),
                (first_x + last_x, first_y + row * self.tile_size), 1)

            for col in range(self.board_size[0]):
                # vertical lines
                pygame.draw.line(screen, self.line_color, 
                    (first_x + col * self.tile_size, first_y), 
                    (first_x + col * self.tile_size, first_y + last_y), 1)

        # draw the bottom and right lines
        pygame.draw.line(screen, self.line_color, (first_x, first_y + last_y),
            (first_x + last_x, first_y + last_y), 1)
        pygame.draw.line(screen, self.line_color, (first_x + last_x, first_y),
            (first_x + last_x, first_y + last_y), 1)


    def display_game_over(self, screen):
        screen.blit(self.game_over_text,(0, 0))
        if not self.win_text:
            try:
                winner = self.bikes.sprites()[0]
                self.win_text = self.the_font.render("%s WINS!" %(winner), 1,
                                                     winner.color)
            except IndexError:
                self.win_text = self.the_font.render("NO WINNER", 1,
                                                     (255, 255, 255))
        screen.blit(self.win_text, (10, screen.get_rect().height * 1/7))


    def display(self, screen):
        screen.fill((0, 0, 0))
        self.trails.draw(screen)
        self.bikes.draw(screen)
        if not len(self.bikes.sprites()) > 1:
            self.display_game_over(screen)


    def is_in_bounds(self, rect):
        full = pygame.Rect(0, 0, self.board_size[0] * self.tile_size,
                           self.board_size[1] * self.tile_size)
        return full.contains(rect)
