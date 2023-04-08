import pygame

from classes import HealtBar, InventorySection, InventorySection_Counter, StatisticShow


class InterFace:
    def __init__(self, game, level, player):
        self.game = game
        self.level = level
        self.screen = self.game.screen
        self.player = player

        self.bars = []

        self.setup()

    def setup(self):
        # ------------------------------- Health Bar -------------------------------
        self.health_bar = HealtBar(
            pos=(self.game.screen_width - self.game.tile_size * 0.5 - self.game.tile_size * 3, self.game.tile_size * 0.5),
            size=(self.game.tile_size * 3, self.game.tile_size / 2),
            health=100,
            colors={
                "background": "black",
                "main": "#C72A14",
            }
        )

        # ------------------------------- Inventory -------------------------------
        colors = {
            "main": "gray30",
            "border": "black",
            "text": "#F6F4C4",
            "selected": "#539DA2",
        }
        self.inventory = []

        # Axe
        self.inventory.append(
            InventorySection(
                button_num=1,
                image=pygame.image.load("../graphics/items/axe.png").convert_alpha(),
                image_size=[8, 9],
                scale=self.game.scale,
                pos=(self.game.tile_size * 0.5 + (self.game.tile_size * 1.25 + self.game.tile_size * 0.25) * 0, self.game.tile_size * 0.5),
                size=(self.game.tile_size * 1.25, self.game.tile_size * 1.25),
                colors=colors,

            )
        )

        # Bow
        self.inventory.append(
            InventorySection_Counter(
                button_num=2,
                image=pygame.image.load("../graphics/items/arrow.png").convert_alpha(),
                image_size=[6, 9],
                scale=self.game.scale,
                pos=(self.game.tile_size * 0.5 + (self.game.tile_size * 1.25 + self.game.tile_size * 0.25) * 1, self.game.tile_size * 0.5),
                size=(self.game.tile_size * 1.25, self.game.tile_size * 1.25),
                colors=colors,
                counter=self.player.arrows,

            )
        )


        # Sword
        self.inventory.append(
            InventorySection(
                button_num=3,
                image=pygame.image.load("../graphics/items/sword.png").convert_alpha(),
                image_size=[7, 10],
                scale=self.game.scale,
                pos=(self.game.tile_size * 0.5 + (self.game.tile_size * 1.25 + self.game.tile_size * 0.25) * 2, self.game.tile_size * 0.5),
                size=(self.game.tile_size * 1.25, self.game.tile_size * 1.25),
                colors=colors,

            )
        )

        # Potion
        self.inventory.append(
            InventorySection_Counter(
                button_num=4,
                image=pygame.image.load("../graphics/items/potion_red.png").convert_alpha(),
                image_size=[7, 8],
                scale=self.game.scale,
                pos=(self.game.tile_size * 0.5 + (self.game.tile_size * 1.25 + self.game.tile_size * 0.25) * 3, self.game.tile_size * 0.5),
                size=(self.game.tile_size * 1.25, self.game.tile_size * 1.25),
                colors=colors,
                counter=self.player.potion,
            )
        )

        # ------------------------------- Keys Show -------------------------------
        self.keys_bar = StatisticShow(
            text="Keys",
            scale=self.game.scale,
            colors={"borders": 'black', "main": "#BBBE13", "text": "#FFF1F3"},
            max_num=self.level.start_num_of_keys,
            size=(self.game.tile_size * 3, self.game.tile_size / 2),
            pos=(self.game.screen_width - self.game.tile_size * 0.5 - self.game.tile_size * 7, self.game.tile_size * 0.5)
        )
        self.bars.append(self.keys_bar)

        # ------------------------------- Mobs Show -------------------------------
        self.mobs_bar = StatisticShow(
            text="Mobs",
            scale=self.game.scale,
            colors={"borders": 'black', "main": "#AF70FF", "text": "#FFF1F3"},
            max_num=len(self.level.enemies),
            size=(self.game.tile_size * 3, self.game.tile_size / 2),
            pos=(self.game.screen_width - self.game.tile_size * 0.5 - self.game.tile_size * 7, self.game.tile_size * 1.5)
        )
        self.bars.append(self.mobs_bar)


    def update_inventory(self):
        # called from player event loop
        for tool in self.inventory:
            tool.unselected()

        if self.player.weapon == "axe":
            self.inventory[0].selected()
        elif self.player.weapon == "bow":
            self.inventory[1].selected()
        elif self.player.weapon == "sword":
            self.inventory[2].selected()
        elif self.player.weapon == "basic":
            self.inventory[3].selected()


    def update(self):
        self.health_bar.update(self.player.health)
        self.mobs_bar.update(len(self.level.enemies))


    def draw(self):
        self.screen.blit(self.health_bar.image, self.health_bar.rect)

        if self.keys_bar.cur_num != 0:
            self.screen.blit(self.keys_bar.image, self.keys_bar.rect)
        else:
            if self.keys_bar in self.bars:
                self.bars.remove(self.keys_bar)
                if self.mobs_bar in self.bars:
                    self.mobs_bar.rect.topleft = self.keys_bar.rect.topleft


        if self.mobs_bar.cur_num != 0:
            self.screen.blit(self.mobs_bar.image, self.mobs_bar.rect)
        else:
            if self.mobs_bar in self.bars:
                self.bars.remove(self.mobs_bar)

        for section in self.inventory:
            self.screen.blit(section.image, section.rect)
