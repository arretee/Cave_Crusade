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


class Menu_Player(pygame.sprite.Sprite):
    def __init__(self, surfaces, pos, group):
        super().__init__(group)

        self.frame_index = 0
        self.animation_speed = 0.06

        self.surfaces = surfaces
        self.image = surfaces[0]
        self.rect = self.image.get_rect(bottomright=pos)

    def update(self):
        self.frame_index += self.animation_speed

        if self.frame_index > len(self.surfaces):
            self.frame_index = 0

        self.image = self.surfaces[int(self.frame_index)]


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





