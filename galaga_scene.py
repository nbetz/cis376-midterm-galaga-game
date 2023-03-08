
import pygame
from Box2D import b2World
import galaga_game_objects
import scene


class GalagaScene(scene.Scene):
    def __init__(self):
        super().__init__()
        enemies = pygame.sprite.Group()
        player = pygame.sprite.Group()
        player_shot = pygame.sprite.Group()
        enemy_shot = pygame.sprite.Group()

        self.groups.update({"enemies": enemies, "player": player, "player_shot": player_shot, "enemy_shot": enemy_shot})
        self.w2b = 1 / 100
        self.b2w = 100
        self.timeStep = 1.0 / 60
        self.vel_iters = 6
        self.pos_iters = 2
        self.world = b2World((0, 0), doSleep=False)



    def initial_scene(self):
        self.game_objects.append(galaga_game_objects.Updater(self))
        self.game_objects.append(galaga_game_objects.Player(self))
        for rows in range(100, 550, 90):
            for cols in range(400, 850, 90):
                self.game_objects.append(galaga_game_objects.Enemy(self, cols, rows))

    def check_win(self) -> bool:
        return False


