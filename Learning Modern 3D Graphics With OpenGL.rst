Learning Modern 3D Graphics Through OpenGL
==========================================

From http://www.arcsynthesis.org/gltut/


Axes and Handedness
-------------------

http://www.arcsynthesis.org/gltut/Basics/ar02s02.html

Use a left-handed co-ord system throughout (i.e. thumb, index, middle are
x, y and z), oriented thus::

    y
    
    ^  z
    | /
    |/
    -----> x

Thus, when compared to screen, x goes right, y goes up and z goes in, away from
the viewer.


Rasterisation overview
----------------------

0. Vertex shader
................

User supplied vertices are 3 or 4 component vertex positions, along with
up to 15 other user-defined vertex attributes.

Output of vertex shader::

    out vec4 gl_Position;

1. Clip space transform
.......................

Vertex shaders produce 4-component clip-space coords.

4th 'w' component defines the extents of clip space for the vertex, ie. clip
space is a cube extending from -w to +w along each of the X, Y and Z axes. The
value of 'w' may be different for every vertex, even within a single triangle.

The x & y of a clip-space co-ordinate are proportional to the vertice's
screen co-ordinate. The perspective transform is already done by the vertex
shader.

Q: Why have a separate w for each vertex? Do vertices with different w values
actually end up being used in practice?

Q: "Clip-space vertices are output by the vertex processing stage of the
rendering pipeline" - what precisely does this mean?
Presumably it means that vertex shaders output clip space co-ords. So does that
imply there is no separate 'clip space transform' which takes place on the
output of the vertex shader?


2. Normalized coords
....................

Each of x,y,z are divided by w.

Verts which need clipping now lie outside of the -1 to +1 cube.

Q: Are normalized coords only three component then? Or do they have a w of 1?

Q: So is clipping actually done against normalised co-ords? Not in clip-space?
Or does it not matter, so long as we adhere to the specification's resulting
behaviour.

3. Window transform
...................

For a window of size (Xw, Yw), vertices are transformed into window coords,
using the viewport transform. This results in vertices within a region:
    X: 0 - Xw  (0 is left edge)
    Y: 0 - Yw  (0 is bottom edge)
    Z: 0 - 1   (zero is nearest, 1 is farthest)

Window coords are still 3-component, floating point values.

Q: Does this step incorporate the perspective transform?

4. Scan conversion
..................

Triangles produce one fragment for every pixel that is within the 2D area
covered. Adjacent triangles (sharing two vertices) are guaranteed to produce
exactly complimentary sets of fragments, i.e. with no gaps or overlap between
them.

Q: how does this guarantee work if triangle edges are anti-aliased? Is triangle
anti-aliasing deprecated these days in favour of fullscreen antialiasing?

This only uses the vertex x and y positions, but an interpolated z component
associated with each of the resulting fragments.

5. Fragment processing
......................

Fragment shaders provide each fragment with one or more color values and a
single depth value.

Inputs to fragments shaders::

    vec3 in gl_FragCoord

6. Fragment writing
...................

Fragments are written to the destination image. Several fragments may be
written to the same pixel. Combining the depth and color of these can be
done flexibly.


The OpenGL API
--------------

http://www.arcsynthesis.org/gltut/Basics/Intro%20What%20is%20OpenGL.html

Generally goes something like::

    // create storage for the object
    GLuint objectName
    glGenObject(1, &objectName)

    // operate on the object, e.g. modify it or use it
    glBindObject(GL_TARGET, objectName)
    glSomeOperation(GL_TARGET, params)

The target indicates the use to which the object is going to be put. Some types
of objects only have a single possible target. Some object types have many
possible targets. The operations on an object then also specify a target, so
that you could operate on objects bound to different targets.

The Structure of OpenGL
-----------------------

OpenGL is a large state machine. The only commands which don't set or
get this state are those that cause rendering to happen using the current
state. The huge struct that represents the state is called the OpenGL context.

Binding objects as shown above causes the object to be bound to fields in
the context. Any function which then uses the context will read values from
the bound object.

Objects are identified by GLuint handles. Binding value 0 represents unbinding
all objects. The state present before the currently bound object is
restored.

Q: Is the restored state from immediately before the currently bound object,
i.e. from the previously-bound object? Or from before any objects were bound?


Following the Data
------------------

http://www.arcsynthesis.org/gltut/Basics/Tut01%20Following%20the%20Data.html

Q: why does the the vertex data already have four components. I understand
that clipspace has 4, but I asssumed that our application would provide 3,
and the transform into clip-space would add the fourth component.
A: He is able to use 4 components on the input because he specifies that
number to the glVertexAttributePointer call, second attribute GLuint size=4.
Still doesn't explain why he chooses to do this rather than just using 3. Does
it make the transform to clip-space simpler and hence quicker?

