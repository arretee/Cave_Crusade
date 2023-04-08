import pygame
from pytmx import load_pygame

from settings import *
from support_functions import import_folder
from classes import Tile, Button, Button_SelectGroup, Menu_Entity


class SettingsWindow:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.current_resolution = [self.game.screen_width, self.game.screen_height]
        self.selected_resolution = [self.game.screen_width, self.game.screen_height]

        self.colors = {
            "BackGround": '#281d2f',
            "LogoText": '#bf8f30',

            "ButtonMain": '#281d2f',
            "ButtonSecond": '#33233C',
            "ButtonSelected": "#7B6F81",
            "ButtonText": '#bf8f30',
            "ButtonBorder": '#241A2A',
        }

        # Groups
        self.buttons_res = pygame.sprite.Group()
        self.entity = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()

        # Setup
        self.setup()
        self.update_selected()

    def setup(self):
        # -------------------------- Logo --------------------------
        self.logo_image = pygame.font.SysFont('cambria', int(self.game.tile_size * 1.8)).render("Cave Crusade", True,
                                                                                                self.colors['LogoText'])
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
                    group=self.entity)

        # -------------------------- Tiles --------------------------
        tmxdata = load_pygame("../map/menu/menu.tmx")
        layer = tmxdata.get_layer_by_name('Tile Layer 1')

        for x, y, surf in layer.tiles():
            Tile(image=surf.convert_alpha(),
                 size=self.game.tile_size,
                 pos=(x * self.game.tile_size, y * self.game.tile_size),
                 groups=[self.tiles])

        # -------------------------- Resolution Section --------------------------
        self.res_image = pygame.font.SysFont('cambria', int(self.game.tile_size * 1.2)).render("Resolution", True,
                                                                                               self.colors['LogoText'])
        self.res_rect = self.res_image.get_rect(center=(self.game.tile_size * 25, self.game.tile_size * 4))

        Button_SelectGroup(
            pos=(self.game.tile_size * 25 - self.game.tile_size * 2.25, self.game.tile_size * 6),
            main_color=self.colors["ButtonMain"],
            second_color=self.colors["ButtonSecond"],
            selected_color=self.colors["ButtonSelected"],
            text_color=self.colors["ButtonText"],
            border_color=self.colors["ButtonBorder"],
            text="1280 x 720",
            font=pygame.font.SysFont('cambria', int(self.game.tile_size * 0.7)),
            size=(self.game.tile_size * 4, self.game.tile_size * 1.5),
            group=self.buttons_res,
            func=self.new_selected_res
        )

        Button_SelectGroup(
            pos=(self.game.tile_size * 25 + self.game.tile_size * 2.25, self.game.tile_size * 6),
            main_color=self.colors["ButtonMain"],
            second_color=self.colors["ButtonSecond"],
            selected_color=self.colors["ButtonSelected"],
            text_color=self.colors["ButtonText"],
            border_color=self.colors["ButtonBorder"],
            text="1366 x 768",
            font=pygame.font.SysFont('cambria', int(self.game.tile_size * 0.7)),
            size=(self.game.tile_size * 4, self.game.tile_size * 1.5),
            group=self.buttons_res,
            func=self.new_selected_res
        )

        Button_SelectGroup(
            pos=(self.game.tile_size * 25 - self.game.tile_size * 2.25, self.game.tile_size * 8),
            main_color=self.colors["ButtonMain"],
            second_color=self.colors["ButtonSecond"],
            selected_color=self.colors["ButtonSelected"],
            text_color=self.colors["ButtonText"],
            border_color=self.colors["ButtonBorder"],
            text="1600 x 900",
            font=pygame.font.SysFont('cambria', int(self.game.tile_size * 0.7)),
            size=(self.game.tile_size * 4, self.game.tile_size * 1.5),
            group=self.buttons_res,
            func=self.new_selected_res
        )

        Button_SelectGroup(
            pos=(self.game.tile_size * 25 + self.game.tile_size * 2.25, self.game.tile_size * 8),
            main_color=self.colors["ButtonMain"],
            second_color=self.colors["ButtonSecond"],
            selected_color=self.colors["ButtonSelected"],
            text_color=self.colors["ButtonText"],
            border_color=self.colors["ButtonBorder"],
            text="1920 x 1080",
            font=pygame.font.SysFont('cambria', int(self.game.tile_size * 0.7)),
            size=(self.game.tile_size * 4, self.game.tile_size * 1.5),
            group=self.buttons_res,
            func=self.new_selected_res
        )

    def new_selected_res(self, res):
        self.selected_resolution = [int(res.split(" x ")[0]), int(res.split(" x ")[1])]
        self.update_selected()
        print(self.selected_resolution)

    def update_selected(self):
        text = str(self.selected_resolution[0]) + " x " + str(self.selected_resolution[1])
        for sprite in self.buttons_res.sprites():
            if sprite.text == text:
                sprite.select()
            else:
                sprite.unselect()

    def update(self):
        self.entity.update()

    def event_loop(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for sprite in self.buttons_res.sprites():
                    if sprite.rect.collidepoint(mouse_pos):
                        sprite.call_function()

    def run(self):
        self.update()
        self.screen.fill(self.colors["BackGround"])

        self.screen.blit(self.logo_image, self.logo_rect)
        pygame.draw.line(self.screen, '#bf8f30', self.logo_rect.bottomleft, self.logo_rect.bottomright, 2)

        self.screen.blit(self.res_image, self.res_rect)
        pygame.draw.line(self.screen, '#bf8f30', self.res_rect.bottomleft, self.res_rect.bottomright, 2)

        self.tiles.draw(self.screen)
        self.entity.draw(self.screen)
        self.buttons_res.draw(self.screen)
