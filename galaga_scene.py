
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
        self.time = 0
        self.e = eng
        self.game_objects.append(galaga_game_objects.ScoreText(self, 25, 25))
        self.game_objects.append(galaga_game_objects.Upper(self))
        self.game_objects.append(galaga_game_objects.Lower(self))


    def check_win(self):
        if not self.groups.get("enemies"):
            level_two = LevelTwo(self.e, self.score, self.user_object.rect.centerx, self.user_object.rect.centery)
            self.e.add_scene(level_two)
            self.e.set_active_scene(level_two)



class LevelTwo(scene.Scene):
    def __init__(self, eng, score, player_x, player_y):
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
        self.score = score
        self.time = 0
        self.e = eng
        self.game_objects.append(galaga_game_objects.ScoreText(self, 25, 25))
        self.game_objects.append(galaga_game_objects.Upper(self))
        self.game_objects.append(galaga_game_objects.Lower(self))
        self.playerx = player_x
        self.playery = player_y

    def initial_grid(self, **kwargs):
        self.game_objects.append(game_object.Updater(self))
        self.user_object = game_object.Player(self, x=self.playerx, y=self.playery)
        self.game_objects.append(self.user_object)
        for rows in range(100, 550, 75):
            col_count = 0
            for cols in range(400, 850, 75):
                col_count += 1
                if 4 > col_count == 4:
                    cols = cols + 15
                if col_count == 5:
                    cols = cols + 30
                if col_count == 6:
                    cols = cols + 45
                self.game_objects.append(game_object.Enemy(self, cols, rows, col_count))

    def check_win(self):
        if not self.groups.get("enemies"):
            level_three = LevelThree(self.e, self.score, self.user_object.rect.centerx, self.user_object.rect.centery)
            self.e.add_scene(level_three)
            self.e.set_active_scene(level_three)


class LevelThree(LevelTwo):
    def __init__(self, eng, score, player_x, player_y):
        super().__init__(eng, score, player_x, player_y)
        self.playerx = player_x
        self.playery = player_y
        self.game_objects.append(galaga_game_objects.ScoreText(self, 25, 25))
        self.game_objects.append(galaga_game_objects.Upper(self))
        self.game_objects.append(galaga_game_objects.Lower(self))

    def initial_grid(self, **kwargs):
        self.game_objects.append(game_object.Updater(self))
        self.user_object = game_object.Player(self, x=self.playerx, y=self.playery)
        self.game_objects.append(self.user_object)
        for rows in range(100, 550, 75):
            for cols in range(400, 952, 86):
                self.game_objects.append(game_object.Enemy(self, cols, rows, 5))

    def check_win(self):
        if not self.groups.get("enemies"):
            go = WinScene(self.e)
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
        self.game_objects.append(galaga_game_objects.TitleText(self, 'Press Space to begin!', 850, 570))

    def initial_grid(self, **kwargs):
        pass

#I can't get this to run in the game_objects class, so it is also in scene.py
# class EndScene(scene.Scene):
#     def __init__(self, eng):
#         super().__init__()
#         self.game_objects.append(galaga_game_objects.GameOverObject(self, eng))
#         #self.game_objects.append(galaga_game_objects.EndText(self, "Press Space Bar to play again", 400, 400))
#         self.game_objects.append(galaga_game_objects.EndText(self, "Press Escape key to quit", 420, 500))
#
#
#     def initial_grid(self, **kwargs):
#         pass

class WinScene(scene.Scene):

    def __init__(self, eng):
        super().__init__()
        self.game_objects.append(galaga_game_objects.WinGameObject(self, eng))
        #self.game_objects.append(galaga_game_objects.EndText(self, "Press Space Bar to play again", 400, 400))
        #self.game_objects.append(galaga_game_objects.WinText(self, "Congratulations! You have destroyed all the enemy ships.", 420, 400))
        self.game_objects.append(galaga_game_objects.WinText(self, "Press Escape key to quit", 420, 525))

    def initial_grid(self, **kwargs):
        pass