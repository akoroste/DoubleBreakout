from __future__ import annotations

import os
from typing import Dict

import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

file_path = os.path.realpath(__file__)
base_path = os.path.split(file_path)[0]


class ShaderProperties(type):
    _shader_cache: Dict[str, Shader] = dict()

    @property
    def unlit(cls):
        return cls._try_get("unlit")

    @property
    def circle(cls):
        return cls._try_get("circle")

    @property
    def text(cls):
        return cls._try_get("text")

    def _try_get(cls, shader_name: str):
        if shader_name in cls._shader_cache:
            return cls._shader_cache[shader_name]

        return Shader(shader_name)


class Shader(metaclass=ShaderProperties):
    def __init__(self, shader_name: str):
        vertex_path = f"{base_path}/{shader_name}/{shader_name}.vert"
        fragment_path = f"{base_path}/{shader_name}/{shader_name}.frag"

        with open(vertex_path, "r") as file:
            vertex = file.read()

        with open(fragment_path, "r") as file:
            fragment = file.read()

        self._shader = compileProgram(compileShader(vertex, GL_VERTEX_SHADER),
                                      compileShader(fragment, GL_FRAGMENT_SHADER))

    def use(self):
        glUseProgram(self._shader)

    def get_attribute(self, attribute_name: str):
        return ShaderAttribute(self, attribute_name)

    def get_uniform(self, uniform_name: str):
        return ShaderUniform(self, uniform_name)

    def get_attribute_location(self, attribute_name: str):
        return glGetAttribLocation(self._shader, attribute_name)

    def get_uniform_location(self, uniform_name: str):
        return glGetUniformLocation(self._shader, uniform_name)


class ShaderAttribute:
    def __init__(self, shader: Shader, attribute_name: str):
        location = shader.get_attribute_location(attribute_name)

        if location == -1:
            raise Exception(f"Attribute {attribute_name} not found in shader {shader}")

        self.location = location

    def use(self, size: int, gl_type, normalized=False, stride=False, pointer=None):
        normalized = GL_FALSE if not normalized else GL_TRUE
        stride = 0 if not stride else stride

        glVertexAttribPointer(self.location, size, gl_type, normalized, stride, pointer)

    def enable(self):
        glEnableVertexAttribArray(self.location)

    def disable(self):
        glDisableVertexAttribArray(self.location)


class ShaderUniform:
    def __init__(self, shader: Shader, uniform_name: str):
        location = shader.get_uniform_location(uniform_name)

        if location == -1:
            raise Exception(f"Uniform {uniform_name} not found in shader {shader}")

        self.name = uniform_name
        self.location = location

    def set(self, value):
        if isinstance(value, np.ndarray):
            if value.ndim == 1:
                if value.size == 1:
                    glUniform1fv(self.location, 1, value)
                elif value.size == 2:
                    glUniform2fv(self.location, 1, value)
                elif value.size == 3:
                    glUniform3fv(self.location, 1, value)
                elif value.size == 4:
                    glUniform4fv(self.location, 1, value)
                else:
                    raise Exception(f"Uniform \"{self.name}\" cannot be set with {value}")
            else:
                assert value.ndim == 2
                assert value.dtype == np.float32

                w, h = value.shape
                assert w == h

                if w == 2:
                    glUniformMatrix2fv(self.location, 1, GL_FALSE, value)
                elif w == 3:
                    glUniformMatrix3fv(self.location, 1, GL_FALSE, value)
                elif w == 4:
                    glUniformMatrix4fv(self.location, 1, GL_FALSE, value)
                else:
                    raise Exception(f"Uniform \"{self.name}\" cannot be set with {value}")

        elif isinstance(value, float):
            glUniform1f(self.location, value)

        else:
            raise Exception(f"Uniform \"{self.name}\" cannot be set with {value}")
