import pygame


# --------------------------------------- Menu Section ---------------------------------------
class Tile(pygame.sprite.Sprite):
    def __init__(self, image, size, pos, groups):
        super().__init__(groups)

        self.image = pygame.transform.scale(image, (size, size)).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, main_color, second_color, text_color, border_color, text, font, size, group, func):
        super().__init__(group)

        self.text = text
        self.font = font

        self.main_color = main_color
        self.second_color = second_color
        self.text_color = text_color
        self.border_color = border_color

        self.size = size

        # Press func
        self.func = func

        # --------- Sprite General ---------
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect(center=pos)

        # --------- Setup ---------
        # BackGround
        self.background_image = pygame.Surface((self.size[0] - 6, self.size[1] - 6))
        self.background_image.fill(self.main_color)
        self.background_rect = self.background_image.get_rect(topleft=(3, 3))

        # text
        self.text_image = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_image.get_rect(center=(self.size[0] / 2, self.size[1] / 2))

        # ------- Draw Button ----------
        self.image.fill(self.border_color)  # border
        self.image.blit(self.background_image, self.background_rect)  # background
        self.image.blit(self.text_image, self.text_rect)  # text

        # ----- For Update -----
        self.background_second_image = pygame.Surface((self.size[0] - 6, self.size[1] - 6))
        self.background_second_image.fill(self.second_color)
        self.background_second_rect = self.background_second_image.get_rect(topleft=(3, 3))

    def call_function(self):
        self.func()

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.image.fill(self.border_color)  # border
            self.image.blit(self.background_second_image, self.background_second_rect)  # background
            self.image.blit(self.text_image, self.text_rect)  # text
        else:
            self.image.fill(self.border_color)  # border
            self.image.blit(self.background_image, self.background_rect)  # background
            self.image.blit(self.text_image, self.text_rect)  # text


class Menu_Entity(pygame.sprite.Sprite):
    def __init__(self, surfaces, pos, group, fliped=False):
        super().__init__(group)
        self.fliped = fliped

        self.frame_index = 0
        self.animation_speed = 0.06

        self.surfaces = surfaces
        self.image = surfaces[0] if not fliped else pygame.transform.flip(surfaces[0], True, False)
        self.rect = self.image.get_rect(bottomright=pos)

    def update(self):
        self.frame_index += self.animation_speed

        if self.frame_index > len(self.surfaces):
            self.frame_index = 0

        self.image = self.surfaces[int(self.frame_index)] if not self.fliped else pygame.transform.flip(
            self.surfaces[int(self.frame_index)], True, False)


# --------------------------------------- Level Section ---------------------------------------
class Timer:
    def __init__(self, duration, func=None):
        self.duration = duration
        self.func = func

        self.start_time = 0
        self.active = False

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.start_time >= self.duration:
            if self.func and self.start_time != 0:
                self.func()

            self.deactivate()


class Level_Tile(pygame.sprite.Sprite):
    def __init__(self, image, size, pos, groups):
        super().__init__(groups)

        self.pos = pos

        self.image = pygame.transform.scale(image, (size, size)).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self, x_shift, ):
        self.rect.x = self.pos[0] + x_shift


class Spike(pygame.sprite.Sprite):
    def __init__(self, image, size, hitbox_size, pos, groups, status):
        super().__init__(groups)

        self.pos = pos

        self.image = pygame.transform.scale(image, (size, size)).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.pos)
        if status == "left":
            self.hitbox = pygame.Surface(hitbox_size).get_rect(topleft=self.rect.topleft)
        elif status == "right":
            self.hitbox = pygame.Surface(hitbox_size).get_rect(
                topleft=(self.rect.right - hitbox_size[0], self.rect.top))
        elif status == "top":
            self.hitbox = pygame.Surface(hitbox_size).get_rect(topleft=self.rect.topleft)
        elif status == "bottom":
            self.hitbox = pygame.Surface(hitbox_size).get_rect(
                topleft=(self.rect.left, self.rect.bottom - hitbox_size[1]))
        self.hitbox_pos = self.hitbox.topleft

    def update(self, x_shift):
        self.rect.x = self.pos[0] + x_shift
        self.hitbox.x = self.hitbox_pos[0] + x_shift


class Arrow(pygame.sprite.Sprite):
    def __init__(self, start_pos, direction, speed, obstacle_sprites, groups, tilesize):
        super().__init__(groups)
        self.obstacle_sprites = obstacle_sprites

        self.pos = start_pos
        if direction == "left":
            self.x_direction = -1 * speed
        else:
            self.x_direction = speed

        self.image = pygame.image.load("../graphics/items/arrow.png")
        self.image = pygame.transform.scale(self.image, (tilesize / 1.5, tilesize * 1.5))

        if direction == "right":
            self.image = pygame.transform.rotate(self.image, 270)
            self.rect = self.image.get_rect(topleft=start_pos)
        else:
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect = self.image.get_rect(topright=start_pos)

        self.hitbox = self.rect.inflate(-self.rect.width * 0.5, -self.rect.height * 0.5)
        self.hitbox_x = self.hitbox.left

    def update(self, x_shift):
        self.hitbox_x += self.x_direction
        self.hitbox.left = self.hitbox_x + x_shift
        self.rect.left = -self.rect.width * 0.25 + self.hitbox.left

        # collision
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if self.x_direction > 0:
                    self.hitbox.right = sprite.rect.left
                    self.x_direction = 0
                elif self.x_direction < 0:
                    self.hitbox.left = sprite.rect.right
                    self.x_direction = 0


class Key(pygame.sprite.Sprite):
    def __init__(self, pos, type, scale, groups):
        super().__init__(groups)

        self.pos = pos
        self.max_y = int(pos[1] + scale * 2)
        self.min_y = int(pos[1] - scale * 2)
        self.direction_y = scale / 20

        if type == "gold":
            self.image = pygame.image.load("../graphics/items/key_gold.png")
        else:
            self.image = pygame.image.load("../graphics/items/key_silver.png.png")

        self.image = pygame.transform.scale(self.image, (7 * scale / 2, 12 * scale / 2))
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self, x_shift):
        self.rect.x = self.pos[0] + x_shift

        if int(self.pos[1]) == self.max_y:
            self.direction_y = -self.direction_y
        elif int(self.pos[1]) == self.min_y:
            self.direction_y = -self.direction_y

        self.pos[1] += self.direction_y
        self.rect.y = self.pos[1]

        # --------------------------------------- InterFace Section ---------------------------------------


# --------------------------------------- Interface ---------------------------------------
class HealtBar(pygame.sprite.Sprite):
    def __init__(self, pos, size, health, colors):
        super().__init__()
        self.tile_size = size[0] / 3
        self.start_health = health

        self.colors = colors
        self.pixel_for_hp = (self.tile_size * 3 - self.tile_size * 0.2) / health

        self.image = pygame.Surface(size)
        self.image.fill(colors["background"])
        sub_image = pygame.Surface(
            (self.tile_size * 3 - self.tile_size * 0.2, self.tile_size / 2 - self.tile_size * 0.2))
        sub_image.fill(colors["main"])
        self.image.blit(sub_image, (self.tile_size * 0.1, self.tile_size * 0.1))

        self.rect = self.image.get_rect(topleft=pos)

    def update(self, health):
        self.image.fill(self.colors["background"])
        if health <= 0:
            health = 1
        sub_image = pygame.Surface((self.pixel_for_hp * health, self.tile_size / 2 - self.tile_size * 0.2))
        sub_image.fill(self.colors["main"])
        self.image.blit(sub_image, (self.tile_size * 0.1, self.tile_size * 0.1))


class InventorySection(pygame.sprite.Sprite):
    def __init__(self, button_num, image, image_size, scale, pos, size, colors):
        super().__init__()

        self.button_num = button_num
        self.colors = colors
        self.size = size
        self.font = pygame.font.SysFont("cambria", int(scale) * 2)

        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect(topleft=pos)

        self.image_tool = pygame.transform.scale(image, (image_size[0] * scale, image_size[1] * scale))
        self.rect_tool = self.image_tool.get_rect(center=(self.size[0] / 2, self.size[1] / 2))

        self.image.fill(self.colors["border"])
        self.sup_image = pygame.Surface((self.size[0] * 0.8, self.size[1] * 0.8))
        self.sup_image.fill(self.colors["main"])
        self.image.blit(self.sup_image, (self.size[0] * 0.1, self.size[1] * 0.1))
        self.image.blit(self.image_tool, self.rect_tool)

        self.image.blit(self.font.render(str(self.button_num), True, self.colors['text']),
                        (self.size[0] * 0.75, self.size[1] * 0.66))

    def selected(self):
        self.image.fill(self.colors["border"])
        self.sup_image = pygame.Surface((self.size[0] * 0.8, self.size[1] * 0.8))
        self.sup_image.fill(self.colors["selected"])
        self.image.blit(self.sup_image, (self.size[0] * 0.1, self.size[1] * 0.1))
        self.image.blit(self.image_tool, self.rect_tool)

        self.image.blit(self.font.render(str(self.button_num), True, self.colors['text']),
                        (self.size[0] * 0.75, self.size[1] * 0.66))

    def unselected(self):
        self.image.fill(self.colors["border"])
        self.sup_image = pygame.Surface((self.size[0] * 0.8, self.size[1] * 0.8))
        self.sup_image.fill(self.colors["main"])
        self.image.blit(self.sup_image, (self.size[0] * 0.1, self.size[1] * 0.1))
        self.image.blit(self.image_tool, self.rect_tool)

        self.image.blit(self.font.render(str(self.button_num), True, self.colors['text']),
                        (self.size[0] * 0.75, self.size[1] * 0.66))


class InventorySection_Counter(pygame.sprite.Sprite):
    def __init__(self, button_num, image, image_size, scale, pos, size, colors, counter):
        super().__init__()

        self.button_num = button_num
        self.size = size
        self.counter = counter

        self.colors = colors
        self.font = pygame.font.SysFont("cambria", int(scale) * 2)
        self.font_counter = pygame.font.SysFont("cambria", int(scale) * 3)

        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect(topleft=pos)

        self.image_tool = pygame.transform.scale(image, (image_size[0] * scale, image_size[1] * scale))
        self.rect_tool = self.image_tool.get_rect(center=(self.size[0] / 2, self.size[1] / 2))

        self.image.fill(self.colors["border"])
        self.sup_image = pygame.Surface((self.size[0] * 0.8, self.size[1] * 0.8))
        self.sup_image.fill(self.colors["main"])
        self.image.blit(self.sup_image, (self.size[0] * 0.1, self.size[1] * 0.1))
        self.image.blit(self.image_tool, self.rect_tool)

        self.image.blit(self.font.render(str(self.button_num), True, self.colors['text']),
                        (self.size[0] * 0.75, self.size[1] * 0.66))
        self.image.blit(self.font_counter.render(str(self.counter), True, self.colors['text']),
                        (self.size[0] * 0.1, self.size[1] * 0.05))

    def update_counter(self, counter):
        self.counter = counter

        self.image.fill(self.colors["border"])
        self.sup_image = pygame.Surface((self.size[0] * 0.8, self.size[1] * 0.8))
        self.sup_image.fill(self.colors["main"])
        self.image.blit(self.sup_image, (self.size[0] * 0.1, self.size[1] * 0.1))
        self.image.blit(self.image_tool, self.rect_tool)

        self.image.blit(self.font.render(str(self.button_num), True, self.colors['text']),
                        (self.size[0] * 0.75, self.size[1] * 0.66))
        self.image.blit(self.font_counter.render(str(self.counter), True, self.colors['text']),
                        (self.size[0] * 0.1, self.size[1] * 0.05))

    def selected(self):
        self.image.fill(self.colors["border"])
        self.sup_image = pygame.Surface((self.size[0] * 0.8, self.size[1] * 0.8))
        self.sup_image.fill(self.colors["selected"])
        self.image.blit(self.sup_image, (self.size[0] * 0.1, self.size[1] * 0.1))
        self.image.blit(self.image_tool, self.rect_tool)

        self.image.blit(self.font.render(str(self.button_num), True, self.colors['text']),
                        (self.size[0] * 0.75, self.size[1] * 0.66))
        self.image.blit(self.font_counter.render(str(self.counter), True, self.colors['text']),
                        (self.size[0] * 0.1, self.size[1] * 0.05))

    def unselected(self):
        self.image.fill(self.colors["border"])
        self.sup_image = pygame.Surface((self.size[0] * 0.8, self.size[1] * 0.8))
        self.sup_image.fill(self.colors["main"])
        self.image.blit(self.sup_image, (self.size[0] * 0.1, self.size[1] * 0.1))
        self.image.blit(self.image_tool, self.rect_tool)

        self.image.blit(self.font.render(str(self.button_num), True, self.colors['text']),
                        (self.size[0] * 0.75, self.size[1] * 0.66))
        self.image.blit(self.font_counter.render(str(self.counter), True, self.colors['text']),
                        (self.size[0] * 0.1, self.size[1] * 0.05))


class StatisticShow(pygame.sprite.Sprite):
    def __init__(self, text, scale, colors, max_num, size, pos):
        super().__init__()
        # General
        self.text = text
        self.size = size
        self.colors = colors
        self.tile_size = scale * 8
        self.pos = pos
        self.font = pygame.font.SysFont("cambria", int(scale) * 3)
        self.max_num = max_num
        self.cur_num = max_num
        self.pixels_for_one = (size[0] - self.tile_size * 0.2) / max_num

        self.image = pygame.Surface(size).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        # sup images
        sup_image = pygame.Surface((size[0] - self.tile_size * 0.2, size[1] - self.tile_size * 0.2))
        sup_image.fill(self.colors["main"])

        self.text_image = self.font.render(self.text, True, self.colors['text'])
        self.text_rect = self.text_image.get_rect(center=(self.rect.centerx-pos[0], self.rect.centery-pos[1]))


        # draw everything
        self.image.fill(self.colors["borders"])
        self.image.blit(sup_image, (self.tile_size * 0.1, self.tile_size * 0.1))
        self.image.blit(self.text_image, self.text_rect)


    def update(self, cur_num):
        if self.cur_num != cur_num:
            self.cur_num = cur_num
            self.image.fill(self.colors["borders"])
            sub_image = pygame.Surface((self.pixels_for_one * cur_num, self.size[1] - self.tile_size * 0.2))
            sub_image.fill(self.colors["main"])
            self.image.blit(sub_image, (self.tile_size * 0.1, self.tile_size * 0.1))
            self.image.blit(self.text_image, self.text_rect)

