import numpy as np
from OpenGL.GL import *

from .characters import Characters
from ...color import Color
from ...shaders import Shader, ShaderAttribute, ShaderUniform

indices = np.array([[0, 2, 1], [0, 3, 2]], dtype=np.uintc)

uv = np.array([
        [0, 0],
        [1, 0],
        [1, 1],
        [0, 1],
], dtype=np.float32)


class TextRenderable:
    def __init__(self, characters: Characters):
        self._text: str
        self._char_data: list[tuple[np.ndarray, int]]

        self.color = Color.white
        self.font_size = 1.0
        self.characters = characters

        # Note: this calculates the default size values, vertex data, and the offsets
        self.text = ""

        self._shader = Shader.text

        self._position_attribute: ShaderAttribute = self._shader.get_attribute("position")
        self._uv_attribute: ShaderAttribute = self._shader.get_attribute("vertexUV")

        self._color_uniform: ShaderUniform = self._shader.get_uniform("color")
        self._matrix_uniform: ShaderUniform = self._shader.get_uniform("matrix")

        # Vertices
        self._positions_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._positions_buffer)
        glBufferData(GL_ARRAY_BUFFER, 4 * 4 * 2, None, GL_STATIC_DRAW)

        # UVs
        self._uv_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._uv_buffer)
        glBufferData(GL_ARRAY_BUFFER, 4 * uv.size, uv, GL_STATIC_DRAW)

        # Indices
        self._index_buffer = glGenBuffers(1)
        self._indices_length = indices.size
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._index_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 4 * self._indices_length, indices, GL_DYNAMIC_DRAW)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

        self._char_data = []

        x = 0
        y = 0
        for c in self._text:
            ch = self.characters[c]
            _, h = ch.textureSize
            _, by = ch.bearing

            y = min(y, by - h)

        y = -y * self.font_size

        self.height = 0

        for c in self.text:
            ch = self.characters[c]

            w, h = ch.textureSize
            bx, by = ch.bearing

            w *= self.font_size
            h *= self.font_size

            bx *= self.font_size
            by *= self.font_size

            vertices = np.array([
                    [x + bx, y + by],
                    [x + bx + w, y + by],
                    [x + bx + w, y + by - h],
                    [x + bx, y + by - h],
            ], np.float32)

            self._char_data.append((vertices, ch.texture))

            x += (ch.advance >> 6) * self.font_size

            if h > self.height:
                self.height = h

        self.width = x

    def render(self, transform_matrix: np.ndarray):
        self._shader.use()

        # Enable the attributes
        self._uv_attribute.enable()
        self._position_attribute.enable()

        # Set UV
        glBindBuffer(GL_ARRAY_BUFFER, self._uv_buffer)
        self._uv_attribute.use(2, GL_FLOAT)

        # Pass index array
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._index_buffer)

        # Set color
        self._color_uniform.set(self.color.to_numpy)

        # Set transform matrix
        self._matrix_uniform.set(transform_matrix)

        for vertices, texture in self._char_data:
            # Set positions
            glBindBuffer(GL_ARRAY_BUFFER, self._positions_buffer)
            glBufferSubData(GL_ARRAY_BUFFER, 0, 4 * vertices.size, vertices)
            self._position_attribute.use(2, GL_FLOAT)

            # Set the texture for this character
            glBindTexture(GL_TEXTURE_2D, texture)

            # Draw call
            glDrawElements(GL_TRIANGLES, self._indices_length, GL_UNSIGNED_INT, None)

        # Disable the attributes
        self._position_attribute.disable()
        self._uv_attribute.disable()
