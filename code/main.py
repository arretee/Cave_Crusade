import pygame
import sys

from menu import Menu
from levels_settings import *
from level import Level
from pause import Pause
from settings_window import SettingsWindow
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
        self.current_level = 2
        self.level = None
        self.pause = None
        self.settingsWindow = None


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
                case "pause":
                    self.pause.run()
                    self.pause.event_loop(events)
                case "settings":
                    self.settingsWindow.run()
                    self.settingsWindow.event_loop(events)

            pygame.display.update()

    def create_level(self):
        self.level = Level(self, levels[self.current_level])
        self.window = "level"

    def create_pause(self):
        self.pause = Pause(self, self.screen.copy())
        self.window = "pause"

    def create_settingsWindow(self):
        self.settingsWindow = SettingsWindow(self)
        self.window = "settings"


    #  ------------------------------------- Buttons from Menu -------------------------------------
    def stop(self):
        pygame.quit()
        sys.exit()


    def level_select(self):
        pass


    # ------------------------------------- Buttons From Pause -------------------------------------
    def button_resume(self):
        self.window = "level"
        self.pause = None

    def button_to_menu(self):
        self.window = "menu"
        self.pause = None
        self.level = None
        self.settingsWindow = None

    def button_to_level_select(self):
        pass



if __name__ == '__main__':
    game = Game()
    game.run()
