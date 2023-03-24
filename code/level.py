import pygame

from classes import Tile
from support_functions import import_folder
from settings import pathes


class Level:
    def __init__(self, game):
        self.game = game

        self.screen = self.game.screen

        # Groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        # setup
        self.setup()

    def setup(self):
        image = pygame.Surface((self.game.tile_size,self.game.tile_size))
        image.fill("white")
        for i in range(32):
            y = self.game.tile_size * 15
            x = self.game.tile_size * i
            Tile(image=image,
                 size=self.game.tile_size,
                 pos=(x, y),
                 groups=[self.visible_sprites, self.obstacle_sprites]
                 )



    def event_loop(self, events):
        pass

    def update(self):
        pass

    def run(self):
        self.screen.fill('#281d2f')
        self.visible_sprites.draw(self.screen)
