import pygame
from Box2D import b2CircleShape, b2FixtureDef, b2Vec2

import game_object
import scene

class Updater(game_object.GameObject):
    def __init__(self, in_scene: "GalagaScene"):
        super().__init__(0, 0, in_scene, in_scene.groups.get('all_sprites'))

    def update(self, **kwargs):
        self.scene.world.Step(self.scene.timeStep, self.scene.vel_iters, self.scene.pos_iters)
        self.scene.world.ClearForces()

class Player(game_object.GameObject):
    def __init__(self, in_scene: "GalagaScene"):
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
                self.body.ApplyForce(b2Vec2(0, -1), self.body.position, True)
            elif event == pygame.K_s or event == pygame.K_DOWN:
                self.body.ApplyForce(b2Vec2(0, 1), self.body.position, True)
            self.dirty = 0