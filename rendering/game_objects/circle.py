from typing import Optional

from .game_object import GameObject
from ..color import Color
from ..point import Point
from ..renderables import CircleRenderable


class Circle(GameObject):
    def __init__(self, diameter: float,
                 color: Color,
                 position: Optional[Point] = None,
                 rotation: float = 0.0,
                 parent: Optional[GameObject] = None):
        if position is None:
            position = Point.zero

        scale = diameter * Point.one
        circle = CircleRenderable(color, 0.5)
        super().__init__(position, scale, rotation, parent, circle)

    @property
    def width(self):
        return self.transform.local_scale.x

    @width.setter
    def width(self, value):
        self.transform.local_scale.x = value

    @property
    def height(self):
        return self.transform.local_scale.y

    @height.setter
    def height(self, value):
        self.transform.local_scale.y = value
