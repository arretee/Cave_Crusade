import pygame
from pytmx import load_pygame

from interface import InterFace
from support_functions import debug
from classes import Level_Tile, Spike, Arrow, Key
from player import Player
from enemy import Enemy
from settings import *


class Level:
    def __init__(self, game, data):
        self.game = game

        self.screen = self.game.screen

        self.level_data = data

        # -------------------------------- Groups --------------------------------
        # main
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.keys = pygame.sprite.Group()

        self.start_door = pygame.sprite.Group()
        self.exit_door = pygame.sprite.Group()

        # enemies and for enemies
        self.enemies_command_sprites = pygame.sprite.Group()
        self.island_borders = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # player and for player
        self.arrows = pygame.sprite.Group()
        self.player = None

        # Draw
        self.x_offset = 0
        self.y_offset = 0

        # setup
        self.exit_door_status = "closed"
        self.setup()
        self.InterFace = InterFace(self.game, self, self.player)
        self.InterFace.update_inventory()

        # Debug
        self.debug_status = False
    # -------------------------------- level create --------------------------------
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
                groups=[self.visible_sprites, self.start_door]
            )

        for x, y, surf in layer_door_exit.tiles():
            Level_Tile(
                image=surf,
                size=self.game.tile_size,
                pos=(x * self.game.tile_size, y * self.game.tile_size),
                groups=[self.visible_sprites, self.exit_door]
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

        layer_enemy_island_borders = tmxdata.get_layer_by_name('island_borders')
        for x, y, surf in layer_enemy_island_borders.tiles():
            Level_Tile(
                image=surf,
                size=self.game.tile_size,
                pos=(x * self.game.tile_size, y * self.game.tile_size),
                groups=[self.island_borders]
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
                island_borders=self.island_borders,
                moving=True if enemy[3] == "moving" else False,
                facing=enemy[2],
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
        for x, y, surf in layer_keys.tiles():
            Key(
                pos=[x * self.game.tile_size, y * self.game.tile_size],
                type="gold",
                scale=self.game.scale,
                groups=[self.visible_sprites, self.keys]
            )
        self.start_num_of_keys = len(self.keys)


        # First update
        self.obstacle_sprites.update(self.x_offset)
        self.visible_sprites.update(self.x_offset)
        self.enemies_command_sprites.update(self.x_offset)

    # -------------------------------- Arrows --------------------------------
    def create_arrow(self, x):
        Arrow(
            start_pos=[x - self.x_offset, self.player.hitbox.centery - self.player.hitbox.height / 5],
            direction=self.player.facing,
            speed=self.game.scale * self.player.data["arrow_speed"],
            obstacle_sprites=self.obstacle_sprites,
            groups=[self.arrows],
            tilesize=self.game.tile_size
        )

    def update_arrows(self):
        self.arrows.update(self.x_offset)

        for enemy in self.enemies.sprites():
            for arrow in self.arrows.sprites():
                if enemy.rect.colliderect(arrow) and arrow.x_direction != 0:
                    arrow.kill()
                    enemy.attack_from_player(self.player.hitbox.centerx, self.player.data["bow_damage"])


    # -------------------------------- Update = Event loop --------------------------------
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
        self.island_borders.update(self.x_offset)
        self.enemies_command_sprites.update(self.x_offset)
        self.update_arrows()
        self.enemies.update(self.x_offset)

        self.InterFace.update()

        for key in self.keys.sprites():
            if key.rect.colliderect(self.player.hitbox):
                key.kill()
                self.InterFace.keys_bar.update(len(self.keys))

        if self.exit_door_status == "closed":
            if len(self.keys) == 0 and len(self.enemies) == 0:
                self.exit_door_status = "open"
                for inxed, sprite in enumerate(self.exit_door.sprites()):
                    sprite.image = self.start_door.sprites()[inxed].image

        if self.exit_door_status == "open":
            if self.exit_door.sprites()[0].rect.colliderect(self.player.hitbox):
                self.game.window = "menu"
                self.game.current_level += 1
                self.game.level = None
                self.game.create_level()



        if self.player.health <= 0:
            self.game.create_level()


        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    self.debug_status = not self.debug_status
                if event.key == pygame.K_ESCAPE:
                    self.game.create_pause()

    # -------------------------------- Run --------------------------------
    def run(self):
        self.screen.fill('#281d2f')
        self.arrows.draw(self.screen)
        self.visible_sprites.draw(self.screen)
        self.enemies.draw(self.screen)
        self.player.draw()

        self.InterFace.draw()

        if self.debug_status:
            pygame.draw.rect(self.screen, "red", self.player.hitbox)
            self.enemies_command_sprites.draw(self.screen)
            pos = "Mouse pos in Tiles = [X = " + str((-self.x_offset + pygame.mouse.get_pos()[0]) // self.game.tile_size), " , Y = ", str(pygame.mouse.get_pos()[1] // self.game.tile_size), "]"
            debug(pos)

            for sprite in self.enemies.sprites():
                pygame.draw.rect(self.screen, "red", sprite.hitbox)
