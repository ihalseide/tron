import pygame
import random

import bikes
from keys_setup import KeysSetup



class SceneBase:

    def __init__(self):
        self.next = self


    def process_inputs(self, events, pressed_keys):
        raise NotImplemented


    def update(self):
        raise NotImplemented


    def render(self, screen):
        raise NotImplemented


    def switch_to_scene(self, next_scene):
        self.next = next_scene


    def terminate(self):
        self.switch_to_scene(None)




class TitleScene(SceneBase):

    def __init__(self):
        super().__init__()


    def process_inputs(self, events, keys):
        if pygame.K_ESCAPE in keys:
            self.terminate


    def update(self):
        pass


    def display(self, screen):
        #pygame.draw.rect(screen, (255, 255, 255), (0, 0, 20, 20))
        pass



class GameScene(SceneBase):

    # this class also acts as the game board
    # constants
    UP = 1
    DOWN = -1
    RIGHT = 2
    LEFT = -2


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
                           self.RIGHT, (255, 0, 0), KeysSetup.wasd)
            spawns.append(b)
        
        if self.num_of_players >= 2:
            b = bikes.Bike(self, "P2",
                           self.board_size[0] // 4 * 3 * self.tile_size,
                           self.board_size[1] // 2 * self.tile_size,
                           self.LEFT, (0, 0, 255), KeysSetup.ijkl)
            spawns.append(b)

        if self.num_of_players >= 3:
            b = bikes.Bike(self, "P3",
                           self.board_size[0] // 2 * self.tile_size,
                           self.board_size[1] // 4 * 3 * self.tile_size,
                           self.UP, (255, 255, 0), KeysSetup.arrows)
            spawns.append(b)

        if self.num_of_players == 4:
            b = bikes.Bike(self, "P4",
                           self.board_size[0] // 2 * self.tile_size,
                           self.board_size[1] // 4 * self.tile_size,
                           self.DOWN, (0, 255, 255), KeysSetup.arrows)
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
