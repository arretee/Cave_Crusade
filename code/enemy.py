import pygame

from settings import *
from support_functions import import_folder
from classes import Timer


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, enemy_type, pos, data, obstacle_sprites, enemies_command_sprites, group):
        super().__init__(group)

        # General
        self.game = game
        self.screen = self.game.screen
        self.enemy_type = enemy_type
        self.data = data
        self.obstacle_sprites = obstacle_sprites
        self.enemies_command_sprites = enemies_command_sprites

        # Animations
        self.status = "run"
        self.import_animations()
        self.animation_index = 0
        self.animation_speed = self.data["animation_speed"]
        self.animation = self.animations["run"]

        # Movement
        self.health = self.data["health"]

        self.timers = {
            "MoveAfterHit_kd": Timer(self.data["MoveAfterHit_kd"], self.stop_baunce),
        }
        self.direction = pygame.math.Vector2(1, 0)
        self.facing = "right"

        self.speed = self.game.scale / self.data["speed"]
        self.gravity_speed = self.game.scale / self.data["gravity_speed"]
        self.jump_speed = self.game.scale / self.data["jump_speed"]

        # Sprite General
        self.y_change = 0
        self.x_change = 0

        self.image = self.animation[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(self.game.scale * self.data["x_inflate"], self.game.scale * self.data["y_inflate"])

        # Temp
        self.switch_stasuses()

    # -------------------------------------- Movement --------------------------------------
    def gravity(self):
        self.direction.y += self.gravity_speed

    def move(self):
        self.hitbox.x += int(self.direction.x * self.speed)
        self.collision('horizontal')
        self.hitbox.y += int(self.direction.y)
        self.collision('vertical')

        self.rect.center = (self.hitbox.centerx + (self.x_change if self.facing == "right" else -self.x_change), self.hitbox.centery + self.y_change)

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites.sprites() + self.enemies_command_sprites.sprites():
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.rect.left
                        self.direction.x = -1
                        self.facing = "left"
                    elif self.direction.x < 0:
                        self.direction.x = 1
                        self.facing = "right"
                        self.hitbox.left = sprite.rect.right



        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                        self.direction.y = 0
                        self.onGround = True

                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.rect.bottom

    def switch_stasuses(self):
        self.y_change = 0
        self.x_change = 0

        # Get Change of X and Y for image
        if self.data[self.status]:
            self.x_change = self.game.scale * self.data["x_" + self.status]
            self.y_change = self.game.scale * self.data["y_" + self.status]

        self.image = self.animations[self.status][0]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        self.animation = self.animations[self.status]
        self.animation_index = 0

    # -------------------------------------- Attack --------------------------------------
    def attack(self, player_x):
        if player_x > self.hitbox.centerx:
            self.facing = "right"
        else:
            self.facing = "left"

        self.direction.x = 0
        self.status = "attack"
        self.switch_stasuses()

    def attack_from_player(self, player_x, damage):
        self.timers["MoveAfterHit_kd"].activate()
        self.health -= damage
        if player_x > self.hitbox.x:
            self.direction.x = -self.game.scale / self.data["HitBounceX"]
            self.direction.y = -self.game.scale / self.data["HitBounceY"]
            self.facing = "right"
        else:
            self.direction.x = self.game.scale / self.data["HitBounceX"]
            self.direction.y = -self.game.scale / self.data["HitBounceY"]
            self.facing = "left"

    def stop_baunce(self):
        if self.facing == "right":
            self.direction.x = 1
        else:
            self.direction.x = -1

    # -------------------------------------- Animations --------------------------------------
    def import_animations(self):
        scale = self.game.scale
        self.animations = {
            "attack": [], "idle": [], "run": []
        }

        for key in self.animations.keys():
            self.animations[key] = import_folder(
                path=pathes["enemy"][self.enemy_type][key],
                scale=scale
            )

    def animate(self):
        self.animation_index += self.animation_speed

        if self.animation_index >= len(self.animation) and self.status == "attack":
            self.animation_index = 0
            self.status = "run"
            self.switch_stasuses()
            if self.facing == "left":
                self.direction.x = -1
            else:
                self.direction.x = 1

        elif self.animation_index >= len(self.animation):
            self.animation_index = 0

        if self.animation_index >= len(self.animation):
            self.animation_index = 0

        if self.facing == "right":
            image = self.animation[int(self.animation_index)]
        else:
            image = pygame.transform.flip(self.animation[int(self.animation_index)], True, False)

        self.image = image
        self.rect = self.image.get_rect(center=self.hitbox.center)
        self.rect.center = (self.hitbox.centerx + (self.x_change if self.facing == "right" else -self.x_change), self.hitbox.centery + self.y_change)

    # -------------------------------------- Update and Draw --------------------------------------
    def update(self):
        if self.health <= 0:
            self.kill()

        for timer in self.timers.values():
            timer.update()

        self.gravity()
        self.move()
        self.animate()
