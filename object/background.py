import pygame.sprite

import assets
import configs
from layer import Layer


class Background(pygame.sprite.Sprite):
    def __init__(self,index,is_night, *groups):
        self._layer = Layer.BACKGROUND
        if is_night :
            self.image = assets.get_sprite("background-night")
            self.image = pygame.transform.scale(
                self.image, (configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT)
            )
        else:
            self.image = assets.get_sprite("background")
        self.rect = self.image.get_rect(topleft=(configs.SCREEN_WIDTH * index,0))

        super().__init__(*groups)

    def update(self):
        self.rect.x -= 1

        if self.rect.right <= 0:
            self.rect.x = configs.SCREEN_WIDTH