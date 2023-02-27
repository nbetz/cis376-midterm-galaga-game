"""Game objects built upon pygame.sprite.Dirtysprite

Provides basic functions for creating GameObjects for a game.
"""

import pygame
import random

from pygame.sprite import AbstractGroup

import engine
import scene


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
