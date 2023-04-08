import pygame


from support_functions import import_folder
from settings import *
from classes import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos, enemies, spikes, obstacle_sprites):
        super().__init__()

        # Main data / Vriabels
        self.data = characters_data["player"]
        self.game = game
        self.spikes = spikes
        self.enemies = enemies
        self.screen = game.screen
        self.setup()
        self.obstacle_sprites = obstacle_sprites

        # Statuses
        self.health = self.data["health"]
        self.max_health = self.data["health"]
        self.direction = pygame.math.Vector2()

        self.speed = self.game.scale / self.data["speed"]
        self.gravity_speed = self.game.scale / self.data["gravity_speed"]
        self.jump_speed = self.game.scale / self.data["jump_speed"]

        self.arrows = 3
        self.potion = 3

        self.status = "idle"
        self.weapon = "basic"
        self.facing = "left"
        self.onGround = False

        self.timers = {
            # Weapons KD
            "sword_kd": Timer(self.data["sword_kd"]),
            "axe_kd": Timer(self.data["axe_kd"]),
            "bow_kd": Timer(self.data["bow_kd"]),
            "potion_kd": Timer(self.data["potion_kd"]),

            # Hit KD
            "MoveAfterHit_kd": Timer(self.data["MoveAfterHit_kd"]),
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
                        self.game.level.InterFace.update_inventory()
                        self.switch_stasuses()
                    elif event.key == pygame.K_1:
                        self.weapon = "axe"
                        self.game.level.InterFace.update_inventory()
                        self.switch_stasuses()
                    elif event.key == pygame.K_2:
                        self.weapon = "bow"
                        self.game.level.InterFace.update_inventory()
                        self.switch_stasuses()
                    elif event.key == pygame.K_3:
                        self.weapon = "sword"
                        self.game.level.InterFace.update_inventory()
                        self.switch_stasuses()

                # Jump
                if event.key == pygame.K_SPACE and self.onGround:
                    self.jump()

        # Movement
        if not self.timers["MoveAfterHit_kd"].active:
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
            else:
                self.potion_use()

        if self.status == "attack" and self.weapon == "bow":
            self.direction.x = 0

    def gravity(self):
        if round(self.direction.y) == 0:
            self.direction.y = 7 * self.gravity_speed
        self.direction.y += self.gravity_speed

    def jump(self):
        if int(self.direction.y) == 0:
            self.onGround = False
            self.direction.y = self.jump_speed

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
                        self.direction.x = 0
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.rect.right
                        self.direction.x = 0

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                        self.direction.y = 0
                        self.onGround = True

                    elif self.direction.y < 0:
                        self.direction.y = 0
                        self.hitbox.top = sprite.rect.bottom


    # -------------------------------------- Enemies Collisions --------------------------------------
    def enemyCollision(self):
        for sprite in self.enemies.sprites():
            if self.hitbox.colliderect(sprite.hitbox):
                sprite.attack(self.hitbox.centerx)
                if not self.timers["MoveAfterHit_kd"].active:
                    self.timers["MoveAfterHit_kd"].activate()
                    print("damage")
                    self.health -= sprite.data["damage"]
                    self.onGround = False
                    if sprite.hitbox.x > self.hitbox.x:
                        self.direction.x = -self.game.scale / self.data["HitBounceX"]
                        self.direction.y = -self.game.scale / self.data["HitBounceY"]
                    else:
                        self.direction.x = self.game.scale / self.data["HitBounceX"]
                        self.direction.y = -self.game.scale / self.data["HitBounceY"]

    def checkHitEnemy(self):
        for sprite in self.enemies.sprites():
            if self.attack_rect.colliderect(sprite.hitbox):
                if not sprite.timers["MoveAfterHit_kd"].active:
                    sprite.attack_from_player(player_x=self.hitbox.centerx, damage=self.data[f"{self.weapon}_damage"])

    def checkSpikeCollision(self):
        for sprite in self.spikes.sprites():
            if self.hitbox.colliderect(sprite.hitbox):
                self.timers["MoveAfterHit_kd"].activate()
                self.health -= 50
                self.onGround = False
                if sprite.hitbox.x > self.hitbox.x:
                    self.direction.x = -self.game.scale / self.data["HitBounceX"]
                    self.direction.y = -self.game.scale / self.data["HitBounceY"]
                else:
                    self.direction.x = self.game.scale / self.data["HitBounceX"]
                    self.direction.y = -self.game.scale / self.data["HitBounceY"]


    # -------------------------------------- User Input - Attacks / Heal--------------------------------------
    def attack(self):
        if not self.timers[f"{self.weapon}_kd"].active and not (self.weapon == "bow" and self.arrows == 0):
            self.timers[f"{self.weapon}_kd"].activate()

            self.status = "attack"
            self.switch_stasuses()

            if self.weapon != "bow":
                if self.facing == "right":
                    self.attack_rect = pygame.Rect((self.hitbox.right, self.hitbox.centery),
                                                   (self.game.scale * (10 if self.weapon == "sword" else 5), self.game.scale * 3))
                if self.facing == "left":
                    self.attack_rect = pygame.Rect((self.hitbox.left - self.game.scale * 5, self.hitbox.centery),
                                                   (self.game.scale * (10 if self.weapon == "sword" else 5), self.game.scale * 3))

    def potion_use(self):
        if self.health < 100 and not self.timers["potion_kd"].active:
            self.health += 25
            if self.health > 100:
                self.health = 100

            self.potion -= 1
            self.timers["potion_kd"].activate()
            self.game.level.InterFace.inventory[3].update_counter(self.potion)
            self.game.level.InterFace.update_inventory()


    # -------------------------------------- Animations --------------------------------------
    def animate(self):
        self.animation_index += self.animation_speed

        if self.animation_index >= len(self.animation) and self.status == "attack":
            self.attack_rect = None
            self.animation_index = 0
            self.status = "idle"
            self.switch_stasuses()

        if self.animation_index >= len(self.animation)-2 and self.status == "attack" and self.weapon == "bow" and not self.animation_index - self.animation_speed >= len(self.animation)-2 :
            if self.facing == "left":
                self.game.level.create_arrow(self.hitbox.left)
            else:
                self.game.level.create_arrow(self.hitbox.right)
            self.arrows -= 1
            self.game.level.InterFace.inventory[1].update_counter(self.arrows)
            self.game.level.InterFace.update_inventory()



        elif self.animation_index >= len(self.animation):
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

        self.event_loop(events)


        if self.attack_rect is not None:
            if self.facing == "right":
                self.attack_rect = pygame.Rect((self.hitbox.right, self.hitbox.centery),
                                               (self.game.scale * (10 if self.weapon == "sword" else 5), self.game.scale * 3))
            if self.facing == "left":
                self.attack_rect = pygame.Rect((self.hitbox.left - self.game.scale * (10 if self.weapon == "sword" else 5), self.hitbox.centery),
                                               (self.game.scale * (10 if self.weapon == "sword" else 5), self.game.scale * 3))

            self.checkHitEnemy()

        self.enemyCollision()
        self.checkSpikeCollision()
        self.animate()
        self.gravity()
        self.move(self.speed)

    def draw(self):
        self.screen.blit(self.image, self.rect)
