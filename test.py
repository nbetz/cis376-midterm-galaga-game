import pygame as pg
from Box2D import *
import game_object
import scene
import engine
import random

w2b = 1 / 100
b2w = 100
gravity = b2Vec2(0.5, -10.0)
world = b2World(gravity, doSleep=False)

timeStep = 1.0 / 60
vel_iters, pos_iters = 6, 2

class TestScene(scene.Scene):
    def __init__(self):
        super().__init__()

    def initial_grid(self, **kwargs):
        self.game_objects.append(Ball())
        self.game_objects.append(Ground(0, 1, 25, .5))
        self.game_objects.append(Ground(2, 2, 1, .25))
        self.game_objects.append(Ground(6, 4, 1, .25))
        self.game_objects.append(Updater())

testscene = TestScene()

class Ground(game_object.GameObject):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, testscene, testscene.groups.get('all_sprites'), testscene.groups.get('drawable'))
        self.body = world.CreateStaticBody(position=(x, y), shapes=b2PolygonShape(box=(w, h)))
        self.image = pg.Surface((2 * w * b2w, 2 * h * b2w))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position.x * b2w, 768 - self.body.position.y * b2w
        self.dirty = 0

class Ball(game_object.GameObject):
    def __init__(self):
        super().__init__(500, 500, testscene, testscene.groups.get('all_sprites'), testscene.groups.get('drawable'))
        self.body = world.CreateDynamicBody(position=(5, 5))
        shape = b2CircleShape(radius=.25)
        fixDef = b2FixtureDef(shape=shape, friction=0.3, restitution=.5, density=.5)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2
        d = .25 * b2w * 2
        self.image = pg.Surface((d, d), pg.SRCALPHA, 32)
        self.image.convert_alpha()
        # self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        pg.draw.circle(self.image, (0, 101, 164), self.rect.center, .25 * b2w)
        self.dirty = 0


    def update(self, **kwargs):
        self.rect.center = self.body.position[0] * b2w, 770 - self.body.position[1] * b2w
        collided = pg.sprite.spritecollide(self, groundGroup, False)
        if(kwargs.get('keydown')):
            event = kwargs.get('keydown')
            if event == pg.KEYDOWN:
                if event == pg.K_SPACE:
                    if len(collided) > 0:
                        self.body.ApplyLinearImpulse(b2Vec2(0, 1), self.body.position, True)
                elif event == pg.K_a:
                    self.body.ApplyLinearImpulse(b2Vec2(-0.5, 0), self.body.position, True)
                elif event == pg.K_d:
                    self.body.ApplyLinearImpulse(b2Vec2(.5, 0), self.body.position, True)
        self.dirty = 0



class Updater(game_object.GameObject):
    def __init__(self):
        super().__init__(0, 0, testscene, testscene.groups.get('all_sprites'))

    def update(self, **kwargs):
        world.Step(timeStep, vel_iters, pos_iters)
        world.ClearForces()

e = engine.Engine(game_fps=60, screen_width=600, screen_height=768)

# set the active scene to the game_scene we created, and start the engine loop

groundGroup = pg.sprite.Group()
e.add_scene(testscene)
e.set_active_scene(testscene)
e.loop()

