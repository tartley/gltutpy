
from ctypes import c_void_p

from OpenGL import GL
from OpenGL.GL.shaders import compileShader, compileProgram
from OpenGL.GL.ARB.vertex_array_object import glBindVertexArray
import pyglet

from framework import glGenVertexArray

# This is lame. What's the right way to get the sizeof(GLfloat) ?
# Tried sys.getsizeof(GLfloat), sys.getsizeof(GLfloat()),
# GLfloat().__sizeof__(). All give different wrong answers (size of python
# objects, not of underlying C 'float' type)
sizeOfFloat = 4
vertexComponents = 4

vertexPositions = [
     0.75,  0.75,  0.0,  1.0,
     0.75, -0.75,  0.0,  1.0,
    -0.75, -0.75,  0.0,  1.0,
]

strVertexShader = """
in vec4 position;
void main()
{
   gl_Position = position;
}
"""
strFragmentShader = """
out vec4 outputColor;
void main()
{
   outputColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
}
"""


window = None
theProgram = None
positionBufferObject = None


def initialize_program():
    global theProgram
    theProgram = compileProgram(
        compileShader(strVertexShader, GL.GL_VERTEX_SHADER),
        compileShader(strFragmentShader, GL.GL_FRAGMENT_SHADER)
    )


def initialize_vertex_buffer():
    global positionBufferObject
    positionBufferObject = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, positionBufferObject)
    array_type = (GL.GLfloat * len(vertexPositions))
    GL.glBufferData(
        GL.GL_ARRAY_BUFFER, len(vertexPositions) * sizeOfFloat,
        array_type(*vertexPositions), GL.GL_STATIC_DRAW
    )
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)


def init():
    initialize_program()
    initialize_vertex_buffer()
    glBindVertexArray( glGenVertexArray() )


def display():
    GL.glClearColor(0.0, 0.0, 0.0, 0.0)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)
    GL.glUseProgram(theProgram)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, positionBufferObject)
    GL.glEnableVertexAttribArray(0)
    GL.glVertexAttribPointer(
        0, vertexComponents, GL.GL_FLOAT, False, 0, c_void_p(0)
    )
    GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(vertexPositions) / vertexComponents)
    GL.glDisableVertexAttribArray(0)
    GL.glUseProgram(0)


def reshape(width, height):
    GL.glViewport(0, 0, width, height)


def main():
    global window
    window = pyglet.window.Window(resizable=True)
    window.on_draw = display
    window.on_resize = reshape
    init()
    pyglet.app.run()


if __name__ == '__main__':
    main()
