
import pygame
import scene
import game_object
import engine


class GalagaScene(scene.Scene):
    def __init__(self):
        super().__init__(self)
        enemies = pygame.sprite.Group()
        player = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        self.groups.update({"enemies": enemies, "player": player, "all_sprites": all_sprites})


    def initial_scene(self):
        pass

    def draw(self):
        pass

    def check_win(self) -> bool:
        return False


