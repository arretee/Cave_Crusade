import pygame

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

        image.fill("red")
        for i in range(0, 32, 31):
            y = self.game.tile_size * 14
            x = self.game.tile_size * i
            Tile(image=image,
                 size=self.game.tile_size,
                 pos=(x, y),
                 groups=[self.enemies_command_sprites]
                 )



        # Player
        self.player = Player(
            game=self.game,
            pos=(400, 0),
            obstacle_sprites=self.obstacle_sprites
        )

        # Enemy
        Enemy(
            game=self.game,
            enemy_type="knight_blue",
            pos=(800, 200),
            data=characters_data["blue_knigt"],
            obstacle_sprites=self.obstacle_sprites,
            enemies_command_sprites=self.enemies_command_sprites,
            group=self.enemies

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
            for sprite in self.enemies.sprites():
                pygame.draw.rect(self.screen, "red", sprite.hitbox)
