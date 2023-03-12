
import pygame
from Box2D import b2World
import galaga_game_objects
import engine
import game_object
import scene


class GalagaScene(scene.Scene):
    def __init__(self, eng):
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
        self.score = 0
        self.e = eng
        self.game_objects.append(galaga_game_objects.TitleText(self, 'Score: ' + self.score.__str__(), 25, 25))

    def check_win(self):
        if not self.groups.get("enemies"):
            level_two = LevelTwo(self.e)
            engine.Engine.add_scene(self.e, level_two)
            engine.Engine.set_active_scene(self.e, level_two)


class LevelTwo(scene.Scene):
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
        self.score = 0
        self.e = engine
        self.game_objects.append(galaga_game_objects.TitleText(self, 'Score: ' + self.score.__str__(), 25, 25))

    def initial_grid(self, **kwargs):
        self.game_objects.append(game_object.Updater(self))
        self.user_object = game_object.Player(self)
        self.game_objects.append(self.user_object)
        for rows in range(100, 550, 75):
            col_count = 0
            for cols in range(400, 850, 75):
                col_count += 1
                self.game_objects.append(game_object.Enemy(self, cols, rows, col_count))

    def check_win(self):
        if not self.groups.get("enemies"):
            level_three = LevelThree(self.e)
            engine.Engine.add_scene(self.e, level_three)
            engine.Engine.set_active_scene(self.e, level_three)


class LevelThree(LevelTwo):
    def __init__(self, eng):
        super().__init__(eng)

    def initial_grid(self, **kwargs):
        self.game_objects.append(game_object.Updater(self))
        self.user_object = game_object.Player(self)
        self.game_objects.append(self.user_object)
        for rows in range(100, 550, 75):
            for cols in range(400, 850, 75):
                self.game_objects.append(game_object.Enemy(self, cols, rows, 5))

    def check_win(self):
        if not self.groups.get("enemies"):
            go = scene.EndScene(self.e)
            engine.Engine.add_scene(self.e, go)
            engine.Engine.set_active_scene(self.e, go)


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



