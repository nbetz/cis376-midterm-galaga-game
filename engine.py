"""Game engine built upon pygame

Provides basic functions of a game engine for creating games using pygame.

Typical usage example:
  engine = Engine(game_fps, screen_width, screen_height)
  game_scene = scene.Scene()
  engine.add_scene(game_scene)
  engine.set_active_scene(game_scene)
"""

import pygame
import scene


class Engine:
    """Engine class providing game engine to run a game on. Built on pygame.

    Attributes:
        screen_width: int representing the width of the screen.
        screen_height: int representing the height of the scree.
        clock: pygame clock for managing time based events.
        delta_time: float representing the fraction of a second the last frame took.
        screen: pygame surface that the game will be rendered on.
    """
    _running: bool
    _fps: int
    _active_scene: scene.Scene
    _scene_list: list = []
    screen_width: int
    screen_height: int
    clock: pygame.time.Clock
    delta_time: float
    screen: pygame.Surface

    def __init__(self, game_fps: int, screen_width: int, screen_height: int):
        pygame.init()
        Engine._running = False
        Engine._fps = game_fps
        Engine.screen_width = screen_width
        Engine.screen_height = screen_height
        Engine.screen = pygame.display.set_mode((screen_width, screen_height))
        Engine.clock = pygame.time.Clock()
        Engine.delta_time = 0

    def loop(self):
        """runs the engine's game loop
        """
        self._running = True
        pygame.key.set_repeat(500)
        while self._running:
            # INPUT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._active_scene.update_all_objects(type="click", position=event.pos)
                elif event.type == pygame.KEYDOWN:
                    self._active_scene.update_all_objects(type="keydown", key=event.key)

            # Update
            # check win condition
            if self._active_scene.check_win():
                self._running = False
            else:
                # update objects if win condition isn't met
                self._active_scene.update_all_objects(type="main")
            # DISPLAY
            self.screen.fill(pygame.Color('dimgrey'))
            self._active_scene.draw()
            pygame.display.flip()
            self.delta_time = self.clock.tick(self._fps)

    def add_scene(self, game_scene: scene.Scene):
        """adds given scene to the engine's list of scenes

            Args:
                game_scene: a scene to be added to the engine's list of scenes
        """
        self._scene_list.append(game_scene)

    def set_active_scene(self, game_scene: scene.Scene, **kwargs):
        """adds given scene to the engine's list of scenes

            Args:
                game_scene: a scene to be added to the engine's list of scenes
                kwargs: a dictionary of named parameters to be passed to the initial_grid function of the scene to determine what happens on scene creation.
        """
        self._active_scene = game_scene
        self.screen.fill(pygame.Color('dimgrey'))
        game_scene.initial_grid(**kwargs)
        game_scene.draw()
        pygame.display.flip()
