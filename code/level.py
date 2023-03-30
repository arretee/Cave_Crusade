import pygame

from classes import Tile
from player import Player
from settings import pathes


class Level:
    def __init__(self, game):
        self.game = game

        self.screen = self.game.screen

        # Groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.player = None

        # setup
        self.setup()

        # Debug
        self.debug_status = False

    def setup(self):
        # Ground
        image = pygame.Surface((self.game.tile_size, self.game.tile_size))
        image.fill("gray30")

        for i in range(32):
            y = self.game.tile_size * 15
            x = self.game.tile_size * i
            Tile(image=image,
                 size=self.game.tile_size,
                 pos=(x, y),
                 groups=[self.visible_sprites, self.obstacle_sprites]
                 )

        # Player
        self.player = Player(
            game=self.game,
            pos=(400, 0),
            obstacle_sprites=self.obstacle_sprites
        )

    def event_loop(self, events):
        self.player.update(events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    self.debug_status = not self.debug_status

    def run(self):
        self.screen.fill('#281d2f')
        self.visible_sprites.draw(self.screen)
        self.player.draw()

        if self.debug_status:
            pygame.draw.rect(self.screen, "red", self.player.hitbox)
