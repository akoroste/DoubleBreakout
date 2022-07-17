import freetype
from OpenGL.GL import *

from .character_slot import CharacterSlot


class Characters(dict):
    def __init__(self, font_file: str):
        super().__init__()

        # disable byte-alignment restriction
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        # noinspection PyTypeChecker
        face = freetype.Face(font_file)
        face.set_char_size(3072)

        # load first 128 characters of ASCII set
        for i in range(0, 128):
            face.load_char(chr(i))
            glyph = face.glyph

            # generate texture
            texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, glyph.bitmap.width, glyph.bitmap.rows, 0,
                         GL_RED, GL_UNSIGNED_BYTE, glyph.bitmap.buffer)

            # texture options
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            # now store character for later use
            self[chr(i)] = CharacterSlot(texture, glyph)

        glBindTexture(GL_TEXTURE_2D, 0)
