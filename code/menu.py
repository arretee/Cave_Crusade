import pygame
from pytmx import load_pygame

from settings import *
from support_functions import import_folder
from classes import Tile, Button, Menu_Entity


class Menu:
    def __init__(self, game):
        # Basic
        self.game = game
        self.screen = self.game.screen

        self.colors = {
            "BackGround": '#281d2f',
            "LogoText": '#bf8f30',

            "ButtonMain": '#281d2f',
            "ButtonSecond": '#33233C',
            "ButtonText": '#bf8f30',
            "ButtonBorder": '#241A2A',
        }
        # Groups
        self.tiles = pygame.sprite.Group()
        self.entity = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

        self.setup()

    def setup(self):
        # -------------------------- Logo --------------------------
        self.logo_image = pygame.font.SysFont('cambria', int(self.game.tile_size * 1.8)).render("Cave Crusade", True, self.colors['LogoText'])
        self.logo_rect = self.logo_image.get_rect(center=(self.game.tile_size * 25, self.game.tile_size * 2))

        # -------------------------- Player --------------------------
        Menu_Entity(surfaces=import_folder(pathes["character"]["bow"]["idle"], self.game.scale),
                    pos=(self.game.tile_size * 14, self.game.tile_size * 5 + self.game.tile_size * 0.15),
                    group=self.entity,
                    fliped=True)

        # Enemies
        Menu_Entity(surfaces=import_folder(pathes["enemy"]["knight_yellow"]["idle"], self.game.scale),
                    pos=(self.game.tile_size * 8, self.game.tile_size * 7 + self.game.tile_size * 0.15),
                    group=self.entity)

        Menu_Entity(surfaces=import_folder(pathes["enemy"]["knight_red"]["idle"], self.game.scale),
                    pos=(self.game.tile_size * 17, self.game.tile_size * 12 + self.game.tile_size * 0.15),
                    group=self.entity,
                    fliped=True)

        Menu_Entity(surfaces=import_folder(pathes["enemy"]["knight_blue"]["idle"], self.game.scale),
                    pos=(self.game.tile_size * 12, self.game.tile_size * 11 + self.game.tile_size * 0.15),
                    group=self.entity,)


        # -------------------------- Tiles --------------------------
        tmxdata = load_pygame("../map/menu/menu.tmx")
        layer = tmxdata.get_layer_by_name('Tile Layer 1')

        for x, y, surf in layer.tiles():
            Tile(image=surf.convert_alpha(),
                 size=self.game.tile_size,
                 pos=(x * self.game.tile_size, y * self.game.tile_size),
                 groups=[self.tiles])

        # -------------------------- Buttons --------------------------
        # Play
        Button(
            pos=(self.game.tile_size * 25, self.game.tile_size * 5)
            , main_color=self.colors["ButtonMain"]
            , second_color=self.colors["ButtonSecond"]
            , text_color=self.colors["ButtonText"]
            , border_color=self.colors["ButtonBorder"]
            , text="Play"
            , font=pygame.font.SysFont('cambria', int(self.game.tile_size * 1.4))
            , size=(self.game.tile_size * 5.3, self.game.tile_size * 2)
            , group=self.buttons
            , func=self.game.create_level
        )

        # Levels
        Button(
            pos=(self.game.tile_size * 25, self.game.tile_size * 7.5)
            , main_color=self.colors["ButtonMain"]
            , second_color=self.colors["ButtonSecond"]
            , text_color=self.colors["ButtonText"]
            , border_color=self.colors["ButtonBorder"]
            , text="Levels"
            , font=pygame.font.SysFont('cambria', int(self.game.tile_size * 1.4))
            , size=(self.game.tile_size * 5.3, self.game.tile_size * 2)
            , group=self.buttons
            , func=self.game.level_select
        )

        # Settings
        Button(
            pos=(self.game.tile_size * 25, self.game.tile_size * 10)
            , main_color=self.colors["ButtonMain"]
            , second_color=self.colors["ButtonSecond"]
            , text_color=self.colors["ButtonText"]
            , border_color=self.colors["ButtonBorder"]
            , text="Settings"
            , font=pygame.font.SysFont('cambria', int(self.game.tile_size * 1.4))
            , size=(self.game.tile_size * 5.3, self.game.tile_size * 2)
            , group=self.buttons
            , func=self.game.create_settingsWindow
        )

        # Exit
        Button(
            pos=(self.game.tile_size * 25, self.game.tile_size * 12.5)
            , main_color=self.colors["ButtonMain"]
            , second_color=self.colors["ButtonSecond"]
            , text_color=self.colors["ButtonText"]
            , border_color=self.colors["ButtonBorder"]
            , text="EXIT"
            , font=pygame.font.SysFont('cambria', int(self.game.tile_size * 1.4))
            , size=(self.game.tile_size * 5.3, self.game.tile_size * 2)
            , group=self.buttons
            , func=self.game.stop
        )

    def event_loop(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for sprite in self.buttons.sprites():
                    if sprite.rect.collidepoint(mouse_pos):
                        sprite.call_function()


    def update(self):
        self.buttons.update(pygame.mouse.get_pos())
        self.entity.update()

    def run(self):
        self.update()
        self.screen.fill(self.colors["BackGround"])


        self.screen.blit(self.logo_image, self.logo_rect)
        pygame.draw.line(self.screen, '#bf8f30', self.logo_rect.bottomleft, self.logo_rect.bottomright, 2)

        self.tiles.draw(self.screen)
        self.entity.draw(self.screen)
        self.buttons.draw(self.screen)



