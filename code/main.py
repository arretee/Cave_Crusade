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

        # temp
        self.screen_width, self.screen_height = screen_resolutions[2]



        if [self.screen_width, self.screen_height] in screen_resolutions:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        else:
            self.screen_width, self.screen_height = screen_resolutions[0]
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.tile_size = self.screen_width / 32
        self.scale = self.tile_size / 8


        # Variabels
        pygame.display.set_caption("Cave Crusade")
        self.clock = pygame.time.Clock()
        self.window = "menu"

        # Setup
        self.menu = Menu(self)
        self.current_level = 1
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
        self.level = Level(self, levels[self.current_level])
        self.window = "level"

    def stop(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
