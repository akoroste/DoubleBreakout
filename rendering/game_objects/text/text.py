from .characters import Characters
from .text_renderable import TextRenderable
from ..game_object import GameObject
from ...color import Color
from ...point import Point


class Text(GameObject):
    def __init__(self, text: str,
                 font_file: str = None,
                 font_size: int = None,
                 color: Color = None,
                 position: Point = None,
                 scale: Point = None,
                 rotation: float = 0.0,
                 parent: GameObject = None):
        if font_file is None:
            import os
            file_path = os.path.realpath(__file__)
            base_path = os.path.split(file_path)[0]

            font_file = f"{base_path}/default_fonts/vera.ttf"

        characters = Characters(font_file)
        renderable = TextRenderable(characters)

        renderable.text = text

        if color is not None:
            renderable.color = color

        if font_size is not None:
            renderable.font_size = font_size

        super().__init__(position, scale, rotation, parent, renderable)

    @property
    def text(self):
        return self.renderable.text

    @text.setter
    def text(self, value):
        self.renderable.text = value

    @property
    def width(self):
        return self.renderable.width
