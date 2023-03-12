import pygame
from Box2D import b2CircleShape, b2FixtureDef, b2Vec2

import engine
import galaga_scene
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
                    # this is where I was trying to add the object to the scene
            elif event == pygame.K_w or event == pygame.K_UP:
                self.body.ApplyForce(b2Vec2(0, 5), self.body.position, True)
            elif event == pygame.K_s or event == pygame.K_DOWN:
                self.body.ApplyForce(b2Vec2(0, -5), self.body.position, True)
            self.dirty = 0

        if kwargs.get('type') == 'keyup':
            event = kwargs.get('key')
            if event == pygame.K_w or event == pygame.K_UP:
                self.body.linearVelocity = (0, 0)
            elif event == pygame.K_s or event == pygame.K_DOWN:
                self.body.linearVelocity = (0, 0)

            self.dirty = 0

class Enemy(game_object.GameObject):
    def __init__(self, in_scene: "GalagaScene", x, y):
        super().__init__(x, y, in_scene, in_scene.groups.get('all_sprites'), in_scene.groups.get('drawable'), in_scene.groups.get('enemies'))
        self.image = pygame.Surface([45, 45])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        pygame.draw.rect(self.image, (255, 255, 255), self.rect)
        self.flag = 0
        self.dirty = 0

    def update(self, **kwargs):
        if self.flag == 30:
            self.flag = self.flag + 1
            self.y = self.y + 10
            self.rect.y = self.rect.y + 10
        elif self.flag == 60:
            self.flag = 0
            self.y = self.y - 10
            self.rect.y = self.rect.y - 10
        else:
            self.flag = self.flag + 1

class Projectile(game_object.GameObject):
    #x pos and y pos can be player/enemy position or some value based on the positon
    # type will be a number that defines what type of projectile it needs to be
    def __init__(self, in_scene: "GalagaScene", xPos, yPos, type):
        print("creating")
        super().__init__(xPos, yPos, in_scene, in_scene.groups.get('all_sprites'), in_scene.groups.get('drawable'), in_scene.groups.get('projectiles'))
        self.body = self.scene.world.CreateDynamicBody(position=(xPos, yPos))
        shape = b2CircleShape(radius= .05)
        # include an if statement here that changes these based on projectile type
        fixDef = b2FixtureDef(shape=shape, friction=0.3, restitution=.5, density=.25)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2
        diameter = .05 * self.scene.b2w * 2
        self.image = pygame.Surface((diameter,diameter), pygame.SCRALPHA, 32)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, (225, 225, 225), self.rect.center, .05 * self.scene.b2w)
        self.dirty = 0
        # i'm thinking type could just be an integer, where 0 represents a player projectile and then other numbers
        # represent the other types of projectiles
        self.proType = type

    def update(self, **kwargs):
        self.rect.center = self.body.position[0] * self.scene.b2w, 600 - self.body.position[1] * self.scene.b2w
        collided = pygame.sprite.spritecollide(self, self.scene.groups.get('drawable'), False)
        # i want this to be logic that makes the bullet disappear when it collides with an enemy or goes off-screen
        #don't think it actually does that though, i just put random values based on my estimate for screen size
        if len(collided) > 0 or self.body.positon[1] > 300:
            self.kill()
            #remove from game objects
        elif self.proType == 0:
            # might only do this once, have a boolean that keeps track
            #im hoping this just makes the bullet go straight at some speed?
            self.body.ApplyLinearImpulse(b2Vec2(0, 5), self.body.position, True)

class TitleObject(game_object.GameObject):
    def __init__(self, in_scene: "TitleScreen", e):
        super().__init__(225, 90, in_scene, in_scene.groups.get('all_sprites'), in_scene.groups.get('drawable'))
        # self.image = pygame.image.load\
        #     ('assets\Galaga-Logo-PNG-File.png').convert_alpha()
        self.image = pygame.image.load('assets\Ship6.png').convert_alpha()
        self.image.set_alpha(255)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.dirty = 0
        self.e = e

    def update(self, **kwargs):
        if kwargs.get('type') == 'keydown':
            event = kwargs.get('key')
            if event == pygame.K_SPACE:
                game_scene = galaga_scene.GalagaScene(self.e)
                engine.Engine.add_scene(self.e, game_scene)
                engine.Engine.set_active_scene(self.e, game_scene)

class TitleText(game_object.GameObject):
    def __init__(self, in_scene: "TitleScreen", text, x, y):
        super().__init__(x, y, in_scene, in_scene.groups.get('all_sprites'), in_scene.groups.get('drawable'))
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.image = self.font.render(text , True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.dirty = 0



