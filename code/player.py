import pygame


from support_functions import import_folder
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos, obstacle_sprites):
        super().__init__()

        self.game = game
        self.screen = game.screen
        self.setup()
        self.obstacle_sprites = obstacle_sprites

        # Statuses
        self.direction = pygame.math.Vector2()

        self.speed = self.game.scale / 2
        self.gravity_speed = self.game.scale / 75
        self.jump_speed = -self.game.scale

        self.status = "idle"
        self.weapon = "basic"
        self.facing = "left"
        self.onGround = False

        # Animations
        self.animation_index = 0
        self.animation_speed = 0.07
        self.animation = self.animations[f"{self.weapon}_{self.status}"]

        # General
        self.y_change = 0
        self.x_change = 0
        self.image = self.animations["basic_idle"][0]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-self.game.scale * 8, -self.game.scale * 6)


    def setup(self):
        # Textures
        scale = self.game.scale
        self.animations = {
            "axe_attack": [], "axe_run": [], "axe_idle": [],
            "bow_attack": [], "bow_run": [], "bow_idle": [],
            "sword_attack": [], "sword_run": [], "sword_idle": [],
            "basic_idle": [], "basic_jump": [], "basic_run": [],
        }

        for key in self.animations.keys():
            self.animations[key] = import_folder(
                path=pathes["character"][key.split("_")[0]][key.split("_")[1]],
                scale=scale
            )

    # -------------------------------------- User Input / Movement --------------------------------------
    def move(self, speed):
        self.hitbox.x += int(self.direction.x * speed)
        self.collision('horizontal')
        self.hitbox.y += int(self.direction.y)
        self.collision('vertical')

        self.rect.center = (self.hitbox.centerx + (self.x_change if self.facing == "right" else -self.x_change), self.hitbox.centery + self.y_change)


    def event_loop(self, events):
        keys = pygame.key.get_pressed()

        for event in events:
            if event.type == pygame.KEYDOWN:
                # Weapon Swap
                if event.key == pygame.K_4:
                    self.weapon = "basic"
                    self.switch_stasuses()
                elif event.key == pygame.K_1:
                    self.weapon = "axe"
                    self.switch_stasuses()
                elif event.key == pygame.K_2:
                    self.weapon = "bow"
                    self.switch_stasuses()
                elif event.key == pygame.K_3:
                    self.weapon = "sword"
                    self.switch_stasuses()

                # Jump
                if event.key == pygame.K_SPACE and self.onGround:
                    self.jump()



        # Movement
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.facing = "left"
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.facing = "right"
        else:
            self.direction.x = 0

        if self.status == "idle" and self.direction.x != 0:
            self.status = "run"
            self.switch_stasuses()
        elif self.status == "run" and self.direction.x == 0:
            self.status = "idle"
            self.switch_stasuses()


    def gravity(self):
        self.direction.y += self.gravity_speed

    def jump(self):
        self.onGround = False
        self.direction.y += self.jump_speed

    # switch y_change, hitbox, image, rect and animation
    def switch_stasuses(self):
        self.y_change = 0
        self.x_change = 0

        if self.weapon != "basic":
            self.y_change = -self.game.scale * 2

        if self.weapon == "basic" and self.status == "run":
            self.y_change = -self.game.scale * 2


        self.image = self.animations[f"{self.weapon}_{self.status}"][0]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        self.hitbox = self.rect.inflate(-self.game.scale * 8, -self.game.scale * 6)


        self.animation = self.animations[f"{self.weapon}_{self.status}"]
        self.animation_index = 0

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.rect.left
                    elif self.direction.x < 0:
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

    # -------------------------------------- Animations --------------------------------------
    def animate(self):
        self.animation_index += self.animation_speed

        if self.animation_index >= len(self.animation):
            self.animation_index = 0

        if self.facing == "right":
            image = self.animation[int(self.animation_index)]
        else:
            image = pygame.transform.flip(self.animation[int(self.animation_index)], True, False)

        self.image = image
        self.rect = self.image.get_rect(center=self.hitbox.center)
        self.hitbox = self.rect.inflate(-self.game.scale * 8, -self.game.scale * 6)

    # -------------------------------------- Update And Draw --------------------------------------

    def update(self, events):
        self.event_loop(events)
        self.gravity()
        self.animate()
        self.move(self.speed)

    def draw(self):
        self.screen.blit(self.image, self.rect)

