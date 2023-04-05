import pygame
from pytmx import load_pygame

from support_functions import debug
from classes import Level_Tile, Spike
from player import Player
from enemy import Enemy
from settings import *


class Level:
    def __init__(self, game, data):
        self.game = game

        self.screen = self.game.screen

        self.level_data = data

        # Groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemies_command_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
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
        tmxdata = load_pygame(self.level_data["tmx_path"])
        self.map_width = tmxdata.width
        self.map_height = tmxdata.height


        # -------------------------------- OFFSET AND PLAYER --------------------------------
        layer_door_start = tmxdata.get_layer_by_name('door_start')
        for x, y, surf in layer_door_start.tiles():
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
            spikes=self.spikes,
            obstacle_sprites=self.obstacle_sprites
        )

        # -------------------------------- TILES --------------------------------
        # -------------- Basic Tiles --------------
        layer_main = tmxdata.get_layer_by_name('main')
        for x, y, surf in layer_main.tiles():
            Level_Tile(
                image=surf,
                size=self.game.tile_size,
                pos=(x * self.game.tile_size, y * self.game.tile_size),
                groups=[self.visible_sprites, self.obstacle_sprites]
            )

        # -------------- Decor --------------
        layer_decor = tmxdata.get_layer_by_name('decor')
        for x, y, surf in layer_decor.tiles():
            Level_Tile(
                image=surf,
                size=self.game.tile_size,
                pos=(x * self.game.tile_size, y * self.game.tile_size),
                groups=[self.visible_sprites]
            )

        # -------------- Doors --------------
        layer_door_start = tmxdata.get_layer_by_name('door_start')
        layer_door_exit = tmxdata.get_layer_by_name('door_exit')

        for x, y, surf in layer_door_start.tiles():
            Level_Tile(
                image=surf,
                size=self.game.tile_size,
                pos=(x * self.game.tile_size, y * self.game.tile_size),
                groups=[self.visible_sprites]
            )

        for x, y, surf in layer_door_exit.tiles():
            Level_Tile(
                image=surf,
                size=self.game.tile_size,
                pos=(x * self.game.tile_size, y * self.game.tile_size),
                groups=[self.visible_sprites]
            )

        # -------------- EnemyBlocks --------------
        layer_enemy_blocks = tmxdata.get_layer_by_name('enemy_blocks')
        for x, y, surf in layer_enemy_blocks.tiles():
            Level_Tile(
                image=surf,
                size=self.game.tile_size,
                pos=(x * self.game.tile_size, y * self.game.tile_size),
                groups=[self.enemies_command_sprites]
            )
        # -------------- Enemies --------------
        for enemy in self.level_data["enemies"].values():
            Enemy(
                game=self.game,
                enemy_type=enemy[1],
                pos=(enemy[0][0] * self.game.tile_size, enemy[0][1] * self.game.tile_size),
                data=characters_data[enemy[1]],
                obstacle_sprites=self.obstacle_sprites,
                enemies_command_sprites=self.enemies_command_sprites,
                group=self.enemies
            )


        # -------------- Spikes --------------
        layer_spikes_right = tmxdata.get_layer_by_name("spikes_right")
        layer_spikes_left = tmxdata.get_layer_by_name("spikes_left")
        layer_spikes_bottom = tmxdata.get_layer_by_name("spikes_bottom")
        layer_spikes_top = tmxdata.get_layer_by_name("spikes_top")

        # right
        for x, y, surf in layer_spikes_right.tiles():
            Spike(
                image=surf,
                size=self.game.tile_size,
                hitbox_size=(self.game.tile_size * 0.4, self.game.tile_size),
                pos=(self.game.tile_size * x, self.game.tile_size * y),
                groups=[self.spikes, self.visible_sprites],
                status="right"
            )
        # left
        for x, y, surf in layer_spikes_left.tiles():
            Spike(
                image=surf,
                size=self.game.tile_size,
                hitbox_size=(self.game.tile_size * 0.4, self.game.tile_size),
                pos=(self.game.tile_size * x, self.game.tile_size * y),
                groups=[self.spikes, self.visible_sprites],
                status="left"
            )

        # bottom
        for x, y, surf in layer_spikes_bottom.tiles():
            Spike(
                image=surf,
                size=self.game.tile_size,
                hitbox_size=(self.game.tile_size, self.game.tile_size * 0.4),
                pos=(self.game.tile_size * x, self.game.tile_size * y),
                groups=[self.spikes, self.visible_sprites],
                status="bottom"
            )
        # top
        for x, y, surf in layer_spikes_top.tiles():
            Spike(
                image=surf,
                size=self.game.tile_size,
                hitbox_size=(self.game.tile_size, self.game.tile_size * 0.4),
                pos=(self.game.tile_size * x, self.game.tile_size * y),
                groups=[self.spikes, self.visible_sprites],
                status="top"
            )

        # -------------- Keys --------------
        layer_keys = tmxdata.get_layer_by_name("keys_door")
        # -------------- Coins --------------
        layer_coins = tmxdata.get_layer_by_name("coins")


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
        self.enemies.update(self.x_offset)

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
            print("Mouse pos in Tiles = [X = ", (-self.x_offset + pygame.mouse.get_pos()[0]) // self.game.tile_size, " , Y = ", pygame.mouse.get_pos()[1] // self.game.tile_size, "]")

            pygame.draw.rect(self.screen, "red", self.player.hitbox)
            self.enemies_command_sprites.draw(self.screen)
            debug(self.player.direction)

            for sprite in self.enemies.sprites():
                pygame.draw.rect(self.screen, "red", sprite.hitbox)

            for sprite in self.spikes.sprites():
                pygame.draw.rect(self.screen, "blue", sprite.hitbox)
