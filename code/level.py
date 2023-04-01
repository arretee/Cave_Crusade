import pygame

from support_functions import debug
from classes import Tile
from player import Player
from enemy import Enemy
from settings import *


class Level:
    def __init__(self, game):
        self.game = game

        self.screen = self.game.screen

        # Groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemies_command_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
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
            enemies=self.enemies,
            pos=(400, 0),
            obstacle_sprites=self.obstacle_sprites
        )

    # Update = Event loop
    def event_loop(self, events):
        self.player.update(events)
        self.enemies.update()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    self.debug_status = not self.debug_status

    def run(self):
        self.screen.fill('#281d2f')
        self.visible_sprites.draw(self.screen)
        self.enemies.draw(self.screen)
        self.player.draw()

        if self.debug_status:
            pygame.draw.rect(self.screen, "red", self.player.hitbox)
            self.enemies_command_sprites.draw(self.screen)
            debug(self.player.health)
            for index, sprite in enumerate(self.enemies.sprites()):
                debug(sprite.health, index*50 + 50, 10)

            for sprite in self.enemies.sprites():
                pygame.draw.rect(self.screen, "red", sprite.hitbox)
