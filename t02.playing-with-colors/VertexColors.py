import ctypes
from ctypes import c_void_p
from os.path import dirname, join

from OpenGL import GL
from OpenGL.GL.shaders import compileShader, compileProgram
from OpenGL.GL.ARB.vertex_array_object import glBindVertexArray
import pyglet

from glwrap import glGenVertexArray


null = c_void_p(0)

sizeOfFloat = ctypes.sizeof(GLfloat)

# Three vertices, with an x,y,z & w for each.
vertexData = [
     0.0,  0.5,   0.0, 1.0,
     0.5, -0.366, 0.0, 1.0,
    -0.5, -0.366, 0.0, 1.0,
     1.0,  0.0,   0.0, 1.0,
     0.0,  1.0,   0.0, 1.0,
     0.0,  0.0,   1.0, 1.0,
]
vertexComponents = 4

# the Pyglet window object
window = None

# Integer handle identifying our compiled shader program
theProgram = None

# Integer handle identifying the GPU memory storing our vertex position array
vertexBufferObject = None


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
            loadFile('VertexColors.vert'), GL.GL_VERTEX_SHADER),
        compileShader(
            loadFile('VertexColors.frag'), GL.GL_FRAGMENT_SHADER)
    )


def initialize_vertex_buffer():
    global vertexBufferObject
    vertexBufferObject = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vertexBufferObject)
    array_type = (GL.GLfloat * len(vertexData))
    GL.glBufferData(
        GL.GL_ARRAY_BUFFER, len(vertexData) * sizeOfFloat,
        array_type(*vertexData), GL.GL_STREAM_DRAW # TODO, needs to be stream?
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
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vertexBufferObject)
    GL.glEnableVertexAttribArray(0)
    GL.glEnableVertexAttribArray(1)
    GL.glVertexAttribPointer(1, 4, GL.GL_FLOAT, False, 0, null)
    GL.glVertexAttribPointer(0, 4, GL.GL_FLOAT, False, 0, c_void_p(48))

    GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)

    GL.glDisableVertexAttribArray(0)
    GL.glDisableVertexAttribArray(1)
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

