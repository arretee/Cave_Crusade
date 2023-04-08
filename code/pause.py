import pygame
from classes import Button


class Pause:
    def __init__(self, game, current_screen_copy):
        self.game = game
        self.screen = game.screen
        self.screen_start_copy = current_screen_copy


        # Dark BackGround Create
        darken_percent = 0.5
        self.background = pygame.Surface(current_screen_copy.get_size()).convert_alpha()
        self.background.fill((0, 0, 0, darken_percent * 255))

        # Groups
        self.buttons = pygame.sprite.Group()

        # Setup
        self.setup()


    def setup(self):
        self.colors = {
            "BackGround": '#281d2f',
            "LogoText": '#bf8f30',

            "ButtonMain": '#281d2f',
            "ButtonSecond": '#33233C',
            "ButtonText": '#bf8f30',
            "ButtonBorder": '#241A2A',
        }
        # Logo
        self.logo_image = pygame.font.SysFont('cambria', int(self.game.tile_size * 1.8)).render("Cave Crusade", True, self.colors['LogoText'])
        self.logo_rect = self.logo_image.get_rect(center=(self.game.screen_width / 2, self.game.tile_size * 2))

        # Buttons
        Button(
            pos=(self.game.screen_width / 2, self.game.tile_size * 5),
            main_color=self.colors["ButtonMain"],
            second_color=self.colors["ButtonSecond"],
            text_color=self.colors["ButtonText"],
            border_color=self.colors["ButtonBorder"],
            text="Resume",
            font=pygame.font.SysFont('cambria', int(self.game.tile_size * 1.4)),
            size=(self.game.tile_size * 5, self.game.tile_size * 2),
            group=self.buttons,
            func=self.game.button_resume
        )

        Button(
            pos=(self.game.screen_width / 2, self.game.tile_size * 7.3),
            main_color=self.colors["ButtonMain"],
            second_color=self.colors["ButtonSecond"],
            text_color=self.colors["ButtonText"],
            border_color=self.colors["ButtonBorder"],
            text="Menu",
            font=pygame.font.SysFont('cambria', int(self.game.tile_size * 1.4)),
            size=(self.game.tile_size * 5, self.game.tile_size * 2),
            group=self.buttons,
            func=self.game.button_to_menu
        )

        Button(
            pos=(self.game.screen_width / 2, self.game.tile_size * 9.6),
            main_color=self.colors["ButtonMain"],
            second_color=self.colors["ButtonSecond"],
            text_color=self.colors["ButtonText"],
            border_color=self.colors["ButtonBorder"],
            text="Levels",
            font=pygame.font.SysFont('cambria', int(self.game.tile_size * 1.4)),
            size=(self.game.tile_size * 5, self.game.tile_size * 2),
            group=self.buttons,
            func=self.game.button_to_level_select
        )

        Button(
            pos=(self.game.screen_width / 2, self.game.tile_size * 11.9),
            main_color=self.colors["ButtonMain"],
            second_color=self.colors["ButtonSecond"],
            text_color=self.colors["ButtonText"],
            border_color=self.colors["ButtonBorder"],
            text="Exit",
            font=pygame.font.SysFont('cambria', int(self.game.tile_size * 1.4)),
            size=(self.game.tile_size * 5, self.game.tile_size * 2),
            group=self.buttons,
            func=self.game.stop
        )



    def event_loop(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for sprite in self.buttons.sprites():
                    if sprite.rect.collidepoint(mouse_pos):
                        sprite.call_function()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.button_resume()


    def run(self):
        # Update
        mouse_pos = pygame.mouse.get_pos()
        self.buttons.update(mouse_pos)


        # BackGround
        self.screen.blit(self.screen_start_copy, (0, 0))
        self.screen.blit(self.background, (0, 0))

        # Draw
        self.screen.blit(self.logo_image, self.logo_rect)
        pygame.draw.line(self.screen, '#bf8f30', self.logo_rect.bottomleft, self.logo_rect.bottomright, 2)

        self.buttons.draw(self.screen)
