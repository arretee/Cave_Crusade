import pygame
from pytmx import load_pygame

from support_functions import debug
from classes import Level_Tile
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

        # Draw
        self.x_offset = 0
        self.y_offset = 0

        # setup
        self.setup()

        # Debug
        self.debug_status = False

    def setup(self):
        # -------------------------------- DATA --------------------------------
        tmxdata = load_pygame("../map/levels/level_test1.tmx")
        self.map_width = tmxdata.width
        self.map_height = tmxdata.height

        layer_main = tmxdata.get_layer_by_name('main')
        layer_door_entrance = tmxdata.get_layer_by_name('door_start')
        layer_door_exit = tmxdata.get_layer_by_name('door_exit')
        layer_decor = tmxdata.get_layer_by_name('decor')
        layer_enemy_blocks = tmxdata.get_layer_by_name('enemy_blocks')

        # -------------------------------- OFFSETS AND PLAYER --------------------------------
        for x, y, surf in layer_door_entrance.tiles():
            self.x_offset = -x * self.game.tile_size + self.game.screen_width / 2
            player_pos = [self.game.screen_width / 2, y * self.game.tile_size]
            break

        self.min_offsets = [-self.map_width * self.game.tile_size + self.game.screen_width, 0]
        self.max_offsets = [0, 0]

        # X offset
        if self.x_offset > self.max_offsets[0]:
            player_pos[0] = player_pos[0] - self.x_offset
            self.x_offset = self.max_offsets[0]
        elif self.x_offset < self.min_offsets[0]:
            player_pos[0] = player_pos[0] - (self.x_offset - (self.min_offsets[0]))
            self.x_offset = self.min_offsets[0]


        # Player
        self.player = Player(
            game=self.game,
            pos=player_pos,
            enemies=self.enemies,
            obstacle_sprites=self.obstacle_sprites
        )

        # -------------------------------- TILES --------------------------------
        # Basic Tiles
        for x, y, surf in layer_main.tiles():
            Level_Tile(
                image=surf,
                size=self.game.tile_size,
                pos=(x * self.game.tile_size, y * self.game.tile_size),
                groups=[self.visible_sprites, self.obstacle_sprites]
            )

        # Decor
        for x, y, surf in layer_decor.tiles():
            Level_Tile(
                image=surf,
                size=self.game.tile_size,
                pos=(x * self.game.tile_size, y * self.game.tile_size),
                groups=[self.visible_sprites]
            )


        # First update
        # self.update_offsets()
        self.obstacle_sprites.update(self.x_offset)
        self.visible_sprites.update(self.x_offset)
        self.enemies_command_sprites.update(self.x_offset)

    # Update = Event loop
    def update_offsets(self):
        # Update
        # X offset
        if self.player.hitbox.centerx <= self.game.tile_size * 10 and self.x_offset < self.max_offsets[0] and self.player.direction.x != 0:
            self.x_offset += self.player.speed
            self.player.hitbox.centerx = self.game.tile_size * 10
        elif self.player.hitbox.centerx >= self.game.screen_width - self.game.tile_size * 10 and self.x_offset > self.min_offsets[0] and self.player.direction.x != 0:
            self.x_offset -= self.player.speed
            self.player.hitbox.centerx = self.game.screen_width - self.game.tile_size * 10


        # X offset - Max And Min
        if self.x_offset > self.max_offsets[0]:
            self.x_offset = self.max_offsets[0]
        elif self.x_offset < self.min_offsets[0]:
            self.x_offset = self.min_offsets[0]

    def event_loop(self, events):

        self.player.update(events)
        self.update_offsets()

        self.obstacle_sprites.update(self.x_offset)
        self.visible_sprites.update(self.x_offset)
        self.enemies_command_sprites.update(self.x_offset)
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
            debug(self.player.direction)

            for index, sprite in enumerate(self.enemies.sprites()):
                debug(sprite.health, index * 50 + 50, 10)

            for sprite in self.enemies.sprites():
                pygame.draw.rect(self.screen, "red", sprite.hitbox)
