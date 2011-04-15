
from OpenGL import GL
from OpenGL.GL.ARB import vertex_array_object

# I'm not entirely sure what I have to go fishing around inside OpenGL.GL.ARB
# to find this function, nor why PyOpenGL doesn't provide a more pythonic
# wrapper for it. I suspect it might be because I only have OpenGL2.1 instead
# of 3.0 or greater.
def glGenVertexArray():
    '''
    Return the integer ID of the created vertex object array
    '''
    vao_id = GL.GLuint(0)
    vertex_array_object.glGenVertexArrays(1, vao_id)
    return vao_id.value

