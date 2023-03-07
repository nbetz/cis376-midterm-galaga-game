

import pygame
import scene
import game_object
import engine


class GalagaScene(scene.Scene):
    def __init__(self):
        super().__init__()
        self.sprite_set = game_object.SpriteSet(self)
        enemies = pygame.sprite.Group()
        player = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        self.groups.update({"enemies": enemies, "player": player, "all_sprites": all_sprites})

    def draw(self):
        self.sprite_set.pieces[0].blitme()
        pygame.display.flip()

    def check_win(self) -> bool:
        return False





