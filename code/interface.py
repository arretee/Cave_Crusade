import pygame

from classes import HealtBar


class InterFace:
    def __init__(self, game, level, player):
        self.game = game
        self.level = level
        self.screen = self.game.screen
        self.player = player

        self.setup()

    def setup(self):
        self.health_bar = HealtBar(
            pos=(self.game.tile_size * 0.5, self.game.tile_size * 0.5),
            size=(self.game.tile_size * 3, self.game.tile_size / 2),
            health=100,
            colors={
                "background": "black",
                "main": "#C72A14",
            }
        )

    def update(self):
        self.health_bar.update(self.player.health)

    def draw(self):
        self.screen.blit(self.health_bar.image, self.health_bar.rect)
