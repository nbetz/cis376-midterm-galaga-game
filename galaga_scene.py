
import pygame
from Box2D import b2World
import galaga_game_objects
import scene


class GalagaScene(scene.Scene):
    def __init__(self, eng):
        super().__init__()
        enemies = pygame.sprite.Group()
        player = pygame.sprite.Group()
        player_shot = pygame.sprite.Group()
        enemy_shot = pygame.sprite.Group()
        self.e = eng

        self.groups.update({"enemies": enemies, "player": player, "player_shot": player_shot, "enemy_shot": enemy_shot})
        self.w2b = 1 / 100
        self.b2w = 100
        self.timeStep = 1.0 / 60
        self.vel_iters = 6
        self.pos_iters = 2
        self.world = b2World((0, 0), doSleep=False)



class TitleScreen(scene.Scene):
    def __init__(self, eng):
        super().__init__()
        self.game_objects.append(galaga_game_objects.TitleObject(self, eng))
        self.game_objects.append(galaga_game_objects.TitleText(self, 'How To play:', 475, 400))
        self.game_objects.append(galaga_game_objects.TitleText(self, 'You are commanding a ship and are being attacked by enemy ships.', 225, 475))
        self.game_objects.append(galaga_game_objects.TitleText(self, 'Press the space bar to fire your cannons and the ', 225, 500))
        self.game_objects.append(galaga_game_objects.TitleText(self, 'arrow keys to dodge incoming shots.', 225, 525))
        self.game_objects.append(galaga_game_objects.TitleText(self, 'Good luck captain!', 450, 600))
        self.game_objects.append(galaga_game_objects.TitleText(self, 'Press Space to begin!', 850, 680))

    def initial_grid(self, **kwargs):
        pass



    # 'How to play: \n '
    # 'You are commanding a ship and are being attacked by enemy ships. \n'
    # 'Press the space bar to fire your cannons and the '
    # 'arrow keys to dodge incoming shots. \n'
    # 'Good luck captain!



