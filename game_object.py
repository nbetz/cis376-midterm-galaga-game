"""Game objects built upon pygame.sprite.Dirtysprite

Provides basic functions for creating GameObjects for a game.
"""

import pygame
from Box2D import b2Vec2, b2FixtureDef, b2CircleShape

from pygame.sprite import AbstractGroup


class GameObject(pygame.sprite.DirtySprite):
    """GameObject class providing basic GameObject info ontop of pygame.sprite.DirtySprite

        Intended to be extended by other classes to provide a base for creating game objects.

        Attributes:
            x: int for x position of object.
            y: int for x position of object.
            last_x: int for last x value during update sequence.
            last_y: int for last y value during update sequence.
            in_scene: scene.Scene that the object belongs to
            *groups: Tuple of pygame Groups that the object belongs to
            image: image of the sprite to be drawn.
            rect: bounding box of the sprite.
        """
    def __init__(self, x: int, y: int, in_scene: "Scene", *groups: AbstractGroup):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.last_x = x
        self.last_y = y
        self.scene = in_scene

class Updater(GameObject):
    def __init__(self, in_scene: "Scene"):
        super().__init__(0, 0, in_scene, in_scene.groups.get('all_sprites'))

    def update(self, **kwargs):
        self.scene.world.Step(self.scene.timeStep, self.scene.vel_iters, self.scene.pos_iters)
        self.scene.world.ClearForces()

class Player(GameObject):
    def __init__(self, in_scene: "Scene"):
        super().__init__(50, 400, in_scene, in_scene.groups.get('all_sprites'), in_scene.groups.get('drawable'), in_scene.groups.get('player'))
        self.body = self.scene.world.CreateDynamicBody(position=(0.5, 4))
        shape = b2CircleShape(radius=.25)
        fixDef = b2FixtureDef(shape=shape, friction=0.3, restitution=.5, density=.5)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2
        d = .25 * self.scene.b2w * 2
        self.image = pygame.Surface((d, d), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        # self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, (0, 101, 164), self.rect.center, .25 * self.scene.b2w)
        self.dirty = 0


    def update(self, **kwargs):
        self.rect.center = self.body.position[0] * self.scene.b2w, 600 - self.body.position[1] * self.scene.b2w
        collided = pygame.sprite.spritecollide(self, self.scene.groups.get('drawable'), False)
        if kwargs.get('type') == 'keydown':
            event = kwargs.get('key')
            if event == pygame.K_SPACE:
                if len(collided) > 0:
                    print('pew pew')
            elif event == pygame.K_w or event == pygame.K_UP:
                self.body.ApplyForce(b2Vec2(0, 1), self.body.position, True)
            elif event == pygame.K_s or event == pygame.K_DOWN:
                self.body.ApplyForce(b2Vec2(0, -1), self.body.position, True)
            self.dirty = 0

        if kwargs.get('type') == 'keyup':
            event = kwargs.get('key')
            if event == pygame.K_w or event == pygame.K_UP:
                self.body.linearVelocity = (0,0)
            elif event == pygame.K_s or event == pygame.K_DOWN:
                self.body.linearVelocity = (0,0)

            self.dirty = 0

class Enemy(GameObject):
    def __init__(self, in_scene: "GalagaScene", x, y):
        super().__init__(x, y, in_scene, in_scene.groups.get('all_sprites'), in_scene.groups.get('drawable'), in_scene.groups.get('enemies'))
        self.image = pygame.Surface([45, 45])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        pygame.draw.rect(self.image, (255, 255, 255), self.rect)
        self.flag = 1
        self.dirty = 0

    #def update(self):
        #if self.flag = 1:


