#!/usr/bin/env python3

import pygame
import logging

import scenes
from constants import *


def main(title, width, height, fps, start_scene):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    clock = pygame.time.Clock()

    active_scene = start_scene

    while active_scene != None:
        pressed_keys = pygame.key.get_pressed()

        # event filtering
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True

            if quit_attempt:
                logging.info("Quit attempt made")
                active_scene.terminate()
            else:
                filtered_events.append(event)

        active_scene.process_inputs(filtered_events, pressed_keys)
        active_scene.update()
        active_scene.display(screen)

        active_scene = active_scene.next

        pygame.display.flip()
        clock.tick(fps)



if __name__ == "__main__":
    main("Tron Bikes", 500, 500, 30, scenes.TitleScene())
