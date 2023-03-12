"""Game scene for managing gameobjects for a game engine.

Provides basic functions of a game scene for creating games.

Typical usage example:
  game_scene = scene.Scene()
  engine.add_scene(game_scene)
"""
from Box2D import b2World

import game_object
import pygame
import random
import engine


class Scene:
    """Scene class providing basic info for managing a set of GameObjects in a game scene

    Intended to be extended by other classes to provide a base for creating game objects.

    Attributes:
    game_objects: list of game objects in the scene.
    groups: dictionary storing all the sprite groups and their string names.
    rand: random number generator
    user_object: GameObject of the player
    tile_size: int representing how large of a square each sprite should be.
    """

    def __init__(self):
        all_sprites = pygame.sprite.Group()
        drawable = pygame.sprite.Group()
        self.game_objects = []
        self.groups = {"all_sprites": all_sprites, "drawable": drawable}
        self.rand = random.Random
        self.user_object: game_object.GameObject = None
        enemies = pygame.sprite.Group()
        player = pygame.sprite.Group()
        player_shot = pygame.sprite.Group()
        enemy_shot = pygame.sprite.Group()
        projectiles = pygame.sprite.Group()
        self.groups.update({"enemies": enemies, "player": player, "player_shot": player_shot, "enemy_shot": enemy_shot,
                            "projectiles": projectiles})
        self.w2b = 1 / 100
        self.b2w = 100
        self.timeStep = 1.0 / 60
        self.vel_iters = 6
        self.pos_iters = 2
        self.world = b2World((0, 0), doSleep=False)

    def update_all_objects(self, *args, **kwargs):
        """calls update() method for all updatable game objects in scene

            Args:
                *args: A tuple of arguments to be passed to each updatable object.
                **kwargs: A dictionary of named arguments to be passed to each updatable object.
            """
        all_sprites = self.groups.get("all_sprites")
        all_sprites.update(*args, **kwargs)

    def draw(self):
        """calls pygame draw function for all objects in scene
        """
        self.groups.get("drawable").draw(engine.Engine.screen)

    def check_win(self) -> bool:
        """checks if win condition is met in scene.

        Returns:
            boolean representing if the win condition has been met. Defaults to always being False
        """
        return False

    def initial_grid(self, **kwargs):
        """initializes board upon being set. Only implemented in child classes.

        Args:
            **kwargs: A dictionary of named arguments to be used as initialization parameters.
        """
        self.game_objects.append(game_object.Updater(self))
        self.user_object = game_object.Player(self)
        self.game_objects.append(self.user_object)
        for rows in range(100, 550, 75):
            col_count = 0
            for cols in range(400, 850, 75):
                col_count += 1
                self.game_objects.append(game_object.Enemy(self, cols, rows, col_count))


class EndScene(Scene):
    def __init__(self, engine):
        super().__init__()
        self.game_objects.append(game_object.GameOverObject(self, engine))
        self.game_objects.append(game_object.EndText(self, "Press Space Bar to play again", 400, 400))
        self.game_objects.append(game_object.EndText(self, "Press Escape key to quit", 420, 500))


    def initial_grid(self, **kwargs):
        pass