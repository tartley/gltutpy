import ctypes
from ctypes import c_void_p
from os.path import dirname, join

from OpenGL import GL
from OpenGL.GL.shaders import compileShader, compileProgram
from OpenGL.GL.ARB.vertex_array_object import glBindVertexArray
import pyglet

from glwrap import glGenVertexArray


null = c_void_p(0)

sizeOfFloat = ctypes.sizeof(GL.GLfloat)

# Three vertices, with an x,y,z & w for each.
vertexPositions = [
     0.75,  0.75,  0.0,  1.0,
     0.75, -0.75,  0.0,  1.0,
    -0.75, -0.75,  0.0,  1.0,
]
vertexComponents = 4

# the Pyglet window object
window = None

# Integer handle identifying our compiled shader program
theProgram = None

# Integer handle identifying the GPU memory storing our vertex position array
positionBufferObject = None


def loadFile(filename):
    with open(join(dirname(__file__), filename)) as fp:
        return fp.read()


def initialize_program():
    """
    Instead of calling OpenGL's shader compilation functions directly
    (glShaderSource, glCompileShader, etc), we use PyOpenGL's wrapper
    functions, which are much simpler to use.
    """
    global theProgram
    theProgram = compileProgram(
        compileShader(
            loadFile('FragPosition.vert'), GL.GL_VERTEX_SHADER),
        compileShader(
            loadFile('FragPosition.frag'), GL.GL_FRAGMENT_SHADER)
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


# Called once at application start-up.
# Must be called after we have an OpenGL context, i.e. after the pyglet
# window is created
def init():
    initialize_program()
    initialize_vertex_buffer()
    glBindVertexArray( glGenVertexArray() )


# Called to redraw the contents of the window
def display():
    GL.glClearColor(0.0, 0.0, 0.0, 0.0)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)

    GL.glUseProgram(theProgram)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, positionBufferObject)
    GL.glEnableVertexAttribArray(0)
    GL.glVertexAttribPointer(0, vertexComponents, GL.GL_FLOAT, False, 0, null)

    GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(vertexPositions) / vertexComponents)

    GL.glDisableVertexAttribArray(0)
    GL.glUseProgram(0)


# Called when the window is resized, including once at application start-up
def reshape(width, height):
    GL.glViewport(0, 0, width, height)


def main():
    global window
    window = pyglet.window.Window(resizable=True, fullscreen=False)
    window.on_draw = display
    window.on_resize = reshape
    init()
    # pyglet's default keyboard handler will exit when escape is pressed
    pyglet.app.run()


if __name__ == '__main__':
    main()

