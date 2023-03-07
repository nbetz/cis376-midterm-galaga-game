"""Game objects built upon pygame.sprite.Dirtysprite

Provides basic functions for creating GameObjects for a game.
"""

import pygame
import random

from sprite_sheet import SpriteSheet
from pygame.sprite import AbstractGroup
import engine


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


class SpriteSet:
    def __init__(self, in_scene: "Scene"):
        """Initialize attributes to represent the overall set of pieces."""

        self.pieces = []
        self._load_pieces()
        self.scene = in_scene

    def _load_pieces(self):
        """Builds the overall set:
        - Loads images from the sprite sheet.
        - Creates a Piece object, and sets appropriate attributes
          for that piece.
        - Adds each piece to the list self.pieces.
        """
        filename = 'Galaga-GeneralSprites.png'
        piece_ss = SpriteSheet(filename)

        # Create a black king.
        player_rect = (0, 0, 30, 30)
        player_image = piece_ss.image_at(player_rect)

        player_ship = PlayerShip(self.scene)
        player_ship.image = player_image
        self.pieces.append(player_ship)


class PlayerShip(GameObject):
    def __init__(self, in_scene: "Scene"):
        GameObject.__init__(self, 50, 50, in_scene)
        self.add(self.scene.groups.get("player"))
        self.add(self.scene.groups.get("all_sprites"))
        self.image = None
        self.screen = engine.Engine.screen
        self.x = 480
        self.y = 100

    def blitme(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y
        self.screen.blit(self.image, self.rect)






