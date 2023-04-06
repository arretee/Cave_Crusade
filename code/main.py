import pygame
import sys

from menu import Menu
from levels_settings import *
from level import Level
from settings import *


class Game:
    def __init__(self):
        pygame.init()
        # Screen
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h

        # self.screen_width, self.screen_height = 1920, 1080
        self.screen_width, self.screen_height = 1600, 900
        # self.screen_width, self.screen_height = 1280, 720


        if [self.screen_width, self.screen_height] in screen_resolutions:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        else:
            self.screen_width = 1280
            self.screen_height = 720
            self.screen = pygame.display.set_mode((1280, 720))

        self.tile_size = self.screen_width / 32
        self.scale = self.tile_size / 8


        # Variabels
        pygame.display.set_caption("Fantasy World")
        self.clock = pygame.time.Clock()
        self.window = "menu"

        # Setup
        self.menu = Menu(self)
        self.level = None



    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.clock.tick(120)
            match self.window:
                case "menu":
                    self.menu.run()
                    self.menu.event_loop(events)
                case "level":
                    self.level.run()
                    self.level.event_loop(events)

            pygame.display.update()

    def create_level(self):
        self.level = Level(self, test_level)
        self.window = "level"

    def stop(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
