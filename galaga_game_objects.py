import pygame
from Box2D import b2CircleShape, b2FixtureDef, b2Vec2, b2PolygonShape

import engine
import galaga_scene
import game_object
import scene

"""
Upper and lower objects are made to keep the ship on the screen.

They are simply invisible static Box2D bodies.
"""
class Upper(game_object.GameObject):
    def __init__(self, in_scene: "Scene"):
        super().__init__(25, 25, in_scene, in_scene.groups.get('all_sprites'))
        self.body = self.scene.world.CreateStaticBody(position=(0.5, 5.6))
        shape = b2PolygonShape(box=(10, .3))
        fixDef = b2FixtureDef(shape=shape, friction=1, restitution=0, density=.5)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2

class Lower(game_object.GameObject):
    def __init__(self, in_scene: "Scene"):
        super().__init__(25, 545, in_scene, in_scene.groups.get('all_sprites'))
        self.body = self.scene.world.CreateStaticBody(position=(0.5, 0.4))
        shape = b2PolygonShape(box=(10, .3))
        fixDef = b2FixtureDef(shape=shape, friction=1, restitution=0, density=.5)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2


class Updater(game_object.GameObject):
    """
    class that helps to update Box2D forces and bodies
    """
    def __init__(self, in_scene: "GalagaScene"):
        super().__init__(0, 0, in_scene, in_scene.groups.get('all_sprites'))

    def update(self, **kwargs):
        self.scene.world.Step(self.scene.timeStep, self.scene.vel_iters, self.scene.pos_iters)
        self.scene.world.ClearForces()


class TitleObject(game_object.GameObject):
    """
    class to set make rect object for galaga sprite on the title screen

    checks for input to start the game
    """
    def __init__(self, in_scene: "TitleScreen", eng):
        super().__init__(225, 90, in_scene, in_scene.groups.get('all_sprites'), in_scene.groups.get('drawable'))
        self.image = pygame.image.load('assets\Galaga-Logo-PNG-File.png').convert_alpha()
        self.image.set_alpha(255)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.dirty = 0
        self.e = eng

    def update(self, **kwargs):
        if kwargs.get('type') == 'keydown':
            event = kwargs.get('key')
            if event == pygame.K_SPACE:
                game_scene = galaga_scene.GalagaScene(self.e)
                engine.Engine.add_scene(self.e, game_scene)
                engine.Engine.set_active_scene(self.e, game_scene)

class TitleText(game_object.GameObject):
    """
    class that makes text object to display text on given scene
    """
    def __init__(self, in_scene: "TitleScreen", text, x, y):
        super().__init__(x, y, in_scene, in_scene.groups.get('all_sprites'), in_scene.groups.get('drawable'))
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.image = self.font.render(text , True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.dirty = 0

class GameOverObject(game_object.GameObject):
    """
    class to set make rect object for game over sprite on the ending screen

    checks for input to exit the game
    """
    def __init__(self, in_scene: "EndScene", e):
        super().__init__(340, 90, in_scene, in_scene.groups.get('all_sprites'), in_scene.groups.get('drawable'))
        self.image = pygame.image.load \
            ('assets\game_over1.png').convert_alpha()
        self.image.set_alpha(255)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.dirty = 0
        self.e = e

    def update(self, **kwargs):
        if kwargs.get('type') == 'keydown':
            event = kwargs.get('key')
            #i want to restart the game if you win
            #if event == pygame.K_SPACE:
                #game_scene = galaga_scene.GalagaScene(self.e)
                #engine.Engine.add_scene(self.e, game_scene)
                #engine.Engine.set_active_scene(self.e, game_scene)
            if event == pygame.K_ESCAPE:
                exit()


class EndText(game_object.GameObject):
    """
    class that makes text object to display text on given scene
    """
    def __init__(self, in_scene: "EndScene", text, x, y):
        super().__init__(x, y, in_scene, in_scene.groups.get('all_sprites'), in_scene.groups.get('drawable'))
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.image = self.font.render(text, True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.dirty = 0

class WinGameObject(game_object.GameObject):
    """
    class to set make rect object for win game sprite on the ending screen

    checks for input to exit the game
    """
    def __init__(self, in_scene: "WinScene", e):
        super().__init__(250, 90, in_scene, in_scene.groups.get('all_sprites'), in_scene.groups.get('drawable'))
        self.image = pygame.image.load \
            ('assets\you-win.png').convert_alpha()
        self.image.set_alpha(255)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.dirty = 0
        self.e = e

    def update(self, **kwargs):
        if kwargs.get('type') == 'keydown':
            event = kwargs.get('key')
            #i want to restart the game if you win
            #if event == pygame.K_SPACE:
                #game_scene = galaga_scene.GalagaScene(self.e)
                #engine.Engine.add_scene(self.e, game_scene)
                #engine.Engine.set_active_scene(self.e, game_scene)
            if event == pygame.K_ESCAPE:
                exit()

class WinText(game_object.GameObject):
    """
    class that makes text object to display text on given scene
    """
    def __init__(self, in_scene: "WinScene", text, x, y):
        super().__init__(x, y, in_scene, in_scene.groups.get('all_sprites'), in_scene.groups.get('drawable'))
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.image = self.font.render(text, True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.dirty = 0



