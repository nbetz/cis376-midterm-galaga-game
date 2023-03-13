"""Game objects built upon pygame.sprite.Dirtysprite

Provides basic functions for creating GameObjects for a game.
"""
import random

import pygame
from Box2D import b2Vec2, b2FixtureDef, b2PolygonShape
import scene
import engine

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
    pygame.mixer.init()
    bulletSound = pygame.mixer.Sound("assets/fire.wav")

    def __init__(self, in_scene: "Scene"):
        super().__init__(75, 400, in_scene, in_scene.groups.get('all_sprites'), in_scene.groups.get('drawable'),
                         in_scene.groups.get('player'))
        self.body = self.scene.world.CreateDynamicBody(position=(0.75, 4))
        shape = b2PolygonShape(box=(.5, .3))
        fixDef = b2FixtureDef(shape=shape, friction=0.3, restitution=.5, density=.5)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2
        d = .25 * self.scene.b2w * 2
        self.image = pygame.image.load("assets/Ship5.png")
        self.image.convert_alpha()
        # TODO maybe use image center?
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position[0] * self.scene.b2w, 600 - self.body.position[1] * self.scene.b2w
        self.dirty = 0

    def update(self, **kwargs):
        self.rect.center = self.body.position[0] * self.scene.b2w, 600 - self.body.position[1] * self.scene.b2w
        collided = pygame.sprite.spritecollide(self, self.scene.groups.get('drawable'), False)
        if kwargs.get('type') == 'keydown':
            event = kwargs.get('key')
            if event == pygame.K_SPACE:
                if len(collided) > 0:
                    projectile = Projectile(self.scene, (self.body.position[0] * self.scene.b2w) + 70,
                                            600 - (self.body.position[1] * self.scene.b2w), 0)
                    self.scene.game_objects.append(projectile)
                    pygame.mixer.Sound.play(self.bulletSound)
            elif event == pygame.K_w or event == pygame.K_UP:
                self.body.linearVelocity = (0, 0)
                self.body.ApplyLinearImpulse(b2Vec2(0, 0.3), self.body.position, True)
                #self.body.ApplyForce(b2Vec2(0, 3), self.body.position, True)
            elif event == pygame.K_s or event == pygame.K_DOWN:
                self.body.linearVelocity = (0, 0)
                self.body.ApplyLinearImpulse(b2Vec2(0, -0.3), self.body.position, True)
                #self.body.ApplyForce(b2Vec2(0, -3), self.body.position, True)
            self.dirty = 0

        if kwargs.get('type') == 'keyup':
            event = kwargs.get('key')
            if event == pygame.K_w or event == pygame.K_UP:
                self.body.linearVelocity = (0, 0)
            elif event == pygame.K_s or event == pygame.K_DOWN:
                self.body.linearVelocity = (0, 0)

            self.dirty = 0


class Enemy(GameObject):
    def __init__(self, in_scene: "GalagaScene", x, y, enemy_type: int):
        super().__init__(x, y, in_scene, in_scene.groups.get('all_sprites'), in_scene.groups.get('drawable'),
                         in_scene.groups.get('enemies'))
        self.flag = 0
        self.dirty = 0
        if enemy_type <= 3:
            self.image = pygame.image.load("assets/Ship1.png")
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            self.type = 1

        elif enemy_type == 4:
            self.image = pygame.image.load("assets/Ship2.png")
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            self.type = 2
        else:
            self.image = pygame.image.load("assets/Ship3.png")
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            self.type = 3

    def update(self, **kwargs):
        # print(self.y)
        if self.flag <= 30 and self.flag % 10 == 0:
            self.flag = self.flag + 1
            self.y = self.y + 10
            self.rect.y = self.rect.y + 10
        elif 30 < self.flag <= 60 and self.flag % 10 == 0:
            self.flag = self.flag + 1
            self.y = self.y - 10
            self.rect.y = self.rect.y - 10
        elif self.flag > 60:
            self.flag = 1
        else:
            self.flag = self.flag + 1
            if random.randint(0, 10000) < 5:
                projectile = Projectile(self.scene, (self.x - 50),
                                        self.y, self.type)


class Projectile(GameObject):
    explosionSound = pygame.mixer.Sound("assets/explosion.wav")

    # x pos and y pos can be player/enemy position or some value based on the positon
    # type will be a number that defines what type of projectile it needs to be
    def __init__(self, in_scene: "GalagaScene", xPos: int, yPos: int, projectile_type: int):
        if projectile_type == 0:
            super().__init__(xPos, yPos, in_scene, in_scene.groups.get('all_sprites'), in_scene.groups.get('drawable'),
                         in_scene.groups.get('player_shot'))
        else:
            super().__init__(xPos, yPos, in_scene, in_scene.groups.get('all_sprites'), in_scene.groups.get('drawable'),
                             in_scene.groups.get('enemy_shot'))
        self.body = self.scene.world.CreateDynamicBody(position=(xPos * self.scene.w2b, (600 - yPos) * self.scene.w2b))
        shape = b2PolygonShape(box=(.15, .03))
        # include an if statement here that changes these based on projectile type
        fixDef = b2FixtureDef(shape=shape, friction=0.3, restitution=.5, density=.25)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2
        diameter = .05 * self.scene.b2w * 2
        # self.image = pygame.image.load("assets/shot.png")
        # self.image.convert_alpha()
        # self.rect = self.image.get_rect()
        if projectile_type == 0:
            self.image = pygame.image.load("assets/shot.png")
        else:
            # CHANGE
            self.image = pygame.image.load("assets/shot-flip.png")
            #self.image = pygame.image.load("assets/shot-flip.png")
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position[0] * self.scene.b2w, 600 - self.body.position[1] * self.scene.b2w
        self.dirty = 0
        self.type = projectile_type
        if projectile_type == 0:
            self.body.ApplyForce(b2Vec2(1, 0), self.body.position, True)
        elif projectile_type == 1:
            self.body.ApplyForce(b2Vec2(-1, 0), self.body.position, True)
        elif projectile_type == 2 or projectile_type == 3:
            player_body_position = self.scene.user_object.body.position
            self.body.ApplyForce(b2Vec2((player_body_position[0] - self.body.position[0])/10,
                                        (player_body_position[1] - self.body.position[1])/10), self.body.position, True)

    def update(self, **kwargs):
        self.rect.center = self.body.position[0] * self.scene.b2w, 600 - self.body.position[1] * self.scene.b2w
        if self.type == 0:
            collided = pygame.sprite.spritecollide(self, self.scene.groups.get('enemies'), False)
            collided_w_projectile = pygame.sprite.spritecollide(self, self.scene.groups.get('enemy_shot'), False)
        else:
            collided = pygame.sprite.spritecollide(self, self.scene.groups.get('player'), False)
            collided_w_projectile = pygame.sprite.spritecollide(self, self.scene.groups.get('player_shot'), False)

        if len(collided) > 0 or len(collided_w_projectile) > 0 or self.body.position[0] > 9 or self.body.position[0] < 0:
            self.kill()
            if len(collided) > 0:
                self.scene.score = self.scene.score + 100
                collided[0].kill()
                if self.type > 0:
                    pygame.mixer.Sound.play(self.explosionSound)
                    # this is where i did eveything for setting a new scene
                    # for sprite in self.scene.groups.get('all_sprites').sprites():
                    #     sprite.kill()
                    game_scene = scene.EndScene(engine)
                    self.scene.e.add_scene(game_scene)
                    self.scene.e.set_active_scene(game_scene)
                    #
                    print('Game Over!')
                    #exit()
            if len(collided_w_projectile) > 0:
                collided_w_projectile[0].kill()
        if self.type == 3:
            self.body.linearVelocity = (0, 0)
            player_body_position = self.scene.user_object.body.position
            if (player_body_position[1] - self.body.position[1])/10 > -0.3:
                self.body.ApplyForce(b2Vec2(-0.3, (player_body_position[1] - self.body.position[1])/10), self.body.position, True)
            else:
                self.body.ApplyForce(b2Vec2((player_body_position[0] - self.body.position[0]/10),
                                        (player_body_position[1] - self.body.position[1])/10), self.body.position, True)
        self.dirty = 0

class GameOverObject(GameObject):
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
            # if event == pygame.K_SPACE:
            #     game_scene = galaga_scene.GalagaScene(engine)
            #     engine.Engine.add_scene(self.e, game_scene)
            #     engine.Engine.set_active_scene(self.e, game_scene)
            if event == pygame.K_ESCAPE:
                exit()


class EndText(GameObject):
    def __init__(self, in_scene: "EndScene", text, x, y):
        super().__init__(x, y, in_scene, in_scene.groups.get('all_sprites'), in_scene.groups.get('drawable'))
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.image = self.font.render(text, True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.dirty = 0


