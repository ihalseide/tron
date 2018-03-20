#!/usr/bin/env python3


class BaseScene:
    def __init__(self):
        self.next = self

    def process_inputs(self, events, pressed_keys):
        pass

    def update(self):
        pass

    def display(self, screen):
        pass

    def switch_to_scene(self, next_scene):
        self.next = next_scene

    def terminate(self):
        self.switch_to_scene(None)
