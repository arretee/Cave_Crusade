import pygame


from support_functions import import_folder
from settings import *
from classes import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos, obstacle_sprites):
        super().__init__()

        # Main data / Vriabels
        self.data = characters_data["player"]
        self.game = game
        self.screen = game.screen
        self.setup()
        self.obstacle_sprites = obstacle_sprites

        # Statuses
        self.direction = pygame.math.Vector2()

        self.speed = self.game.scale / self.data["speed"]
        self.gravity_speed = self.game.scale / self.data["gravity_speed"]
        self.jump_speed = self.game.scale / self.data["jump_speed"]

        self.status = "idle"
        self.weapon = "basic"
        self.facing = "left"
        self.onGround = False

        self.timers = {
            "sword_kd": Timer(self.data["sword_kd"]),
            "axe_kd": Timer(self.data["axe_kd"]),
            "bow_kd": Timer(self.data["bow_kd"]),
        }

        self.attack_rect = None

        # Animations
        self.animation_index = 0
        self.animation_speed = self.data["animation_speed"]
        self.animation = self.animations[f"{self.weapon}_{self.status}"]

        # General
        self.y_change = 0
        self.x_change = 0
        self.image = self.animations["basic_idle"][0]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(self.game.scale * self.data["x_inflate"], self.game.scale * self.data["y_inflate"])

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

    # -------------------------------------- User Input - Movement --------------------------------------
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
                if self.status != "attack":
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


        # Attack
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            if not self.weapon == "basic":
                self.attack()

        if self.status == "attack" and self.weapon == "bow":
            self.direction.x = 0

    def gravity(self):
        self.direction.y += self.gravity_speed

    def jump(self):
        self.onGround = False
        self.direction.y += self.jump_speed

    # switch y_change, hitbox, image, rect and animation
    def switch_stasuses(self):
        self.y_change = 0
        self.x_change = 0

        # Get Change of X and Y for image
        if self.weapon != "basic":
            self.y_change = -self.game.scale * 2

        if self.weapon == "basic" and self.status == "run":
            self.y_change = -self.game.scale * 2

        if self.weapon == "sword" and self.status == "attack":
            self.y_change = -self.game.scale * 0.9


        if self.weapon == "bow" and self.status != "idle":
            if self.status == "run":
                self.x_change = self.game.scale * 4
            else:
                self.x_change = self.game.scale * 8



        self.image = self.animations[f"{self.weapon}_{self.status}"][0]
        self.rect = self.image.get_rect(center=self.hitbox.center)


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


    # -------------------------------------- User Input - Attacks --------------------------------------
    def attack(self):
        if not self.timers[f"{self.weapon}_kd"].active:
            self.timers[f"{self.weapon}_kd"].activate()

            self.status = "attack"
            self.switch_stasuses()

            if self.weapon != "bow":
                if self.facing == "right":
                    self.attack_rect = pygame.Rect((self.hitbox.right, self.hitbox.centery), (self.game.scale, self.game.scale))
                if self.facing == "left":
                    self.attack_rect = pygame.Rect((self.hitbox.left + self.game.scale, self.hitbox.centery), (self.game.scale, self.game.scale))

    # -------------------------------------- Animations --------------------------------------
    def animate(self):
        self.animation_index += self.animation_speed

        if self.animation_index >= len(self.animation) and self.status == "attack":
            self.attack_rect = None
            self.animation_index = 0
            self.status = "idle"
            self.switch_stasuses()

        if self.animation_index >= len(self.animation):
            self.animation_index = 0

        if self.facing == "right":
            image = self.animation[int(self.animation_index)]
        else:
            image = pygame.transform.flip(self.animation[int(self.animation_index)], True, False)

        self.image = image
        self.rect = self.image.get_rect(center=self.hitbox.center)
        # self.hitbox = self.rect.inflate(-self.game.scale * 8, -self.game.scale * 6)

    # -------------------------------------- Update And Draw --------------------------------------

    def update(self, events):
        for timer in self.timers.values():
            timer.update()

        if self.attack_rect is not None:
            if self.facing == "right":
                self.attack_rect = pygame.Rect((self.hitbox.right, self.hitbox.centery),
                                               (self.game.scale * 5, self.game.scale * 3))
            if self.facing == "left":
                self.attack_rect = pygame.Rect((self.hitbox.left - self.game.scale * 5, self.hitbox.centery),
                                               (self.game.scale * 5, self.game.scale * 3))


        self.event_loop(events)
        self.gravity()
        self.animate()
        self.move(self.speed)

    def draw(self):
        self.screen.blit(self.image, self.rect)
        if self.attack_rect is not None:
            pygame.draw.rect(self.screen, "blue", self.attack_rect)
