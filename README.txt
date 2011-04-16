
This repo contains a Python translation of the C samples from the Modern
OpenGL tutorial at
http://www.arcsynthesis.org/gltut (online docs)
and
https://bitbucket.org/alfonse/gltut/overview (repo)


Requirements
------------

Python 2.7
pyglet 1.1.4
PyOpenGL 3.0.1


Changes from original
---------------------

For ease of cross-referencing, I've tried to stay true to the original C
samples. I kept the overall structure of the code, and names of functions
and variables, even when they aren't Pythonic.

I have made changes here and there to make the samples run on my OpenGL2.1
hardware. The original C targets OpenGL3.3. This has required:

 * I removed the 'version 330' lines from all shaders
 * I removed the 'layout(location = 0)' parts from the declaration of
   vertex attributes in the shaders.
 * Function glGenVertexArray is an ARB extension, rather than in the same
   namespace as the other functions.


Thanks
------

Thanks to the mysterious author of the Modern OpenGL tutorial, known to me only
as bitbucket user alfonse.

Thanks to Mike Fletcher for v3 of the Python OpenGL bindings and all their
helper utilities like shader compilation functions.

Thanks to Alex Holkner and Richard Jones for Pyglet.

