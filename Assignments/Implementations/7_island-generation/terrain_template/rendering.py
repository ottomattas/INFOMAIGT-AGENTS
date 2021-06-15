from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import panda3d.core as core
import math

class Renderer(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        dlight = core.DirectionalLight('dlight')
        dlight.setDirection(core.LVector3(1, 0, 1))
        dlnode = self.render.attachNewNode(dlight)
        self.render.setLight(dlnode)

        alight = core.AmbientLight('alight')
        alight.setColor((0.3, 0.3, 0.3, 1))
        alnode = self.render.attachNewNode(alight)
        self.render.setLight(alnode)

    def render_heightmap(self, heights, cell_size, colours = None):
        form = core.GeomVertexFormat.get_v3n3c4()

        vdata = core.GeomVertexData('terrain', form, core.Geom.UHStatic)
        vdata.setNumRows(len(heights))

        vertex = core.GeomVertexWriter(vdata, 'vertex')
        normal = core.GeomVertexWriter(vdata, 'normal')
        colour = core.GeomVertexWriter(vdata, 'color')

        for y in range(heights.shape[1]):
            for x in range(heights.shape[0]):
                vertex.addData3(x * cell_size, y * cell_size, heights[x][y])
                if not colours is None:
                    r, g, b = colours[x][y]
                    colour.addData4(r, g, b, 1)
                else:
                    colour.addData4(0.5, 0.5, 0.5, 1)
                normal.addData3(calculate_normal(heights, cell_size, x, y))

        prim = core.GeomTriangles(core.Geom.UHStatic)
        for y in range(heights.shape[1] - 1):
            for x in range(heights.shape[0] - 1):
                base = x + y * heights.shape[0]
                idx = y * heights.shape[0] + x
                prim.add_vertices(base, base + heights.shape[0] + 1, base + heights.shape[0])
                prim.add_vertices(base, base + 1, base + heights.shape[0] + 1)

        geom = core.Geom(vdata)
        geom.addPrimitive(prim)

        node = core.GeomNode('gnode')
        node.addGeom(geom)
        self.render.attachNewNode(node)

def calculate_normal(heights, cell_size, x, y):
    p0 = (x * cell_size, y * cell_size, heights[x][y])
    normals = []

    if x > 0 and y < heights.shape[1] - 1:
        p1 = get_point(heights, cell_size, x - 1, y)
        p2 = get_point(heights, cell_size, x, y + 1)
        normals.append(normalise(cross(sub(p1, p0), sub(p2, p0))))

    if x > 0 and y > 0:
        p1 = get_point(heights, cell_size, x, y - 1)
        p2 = get_point(heights, cell_size, x - 1, y)
        normals.append(normalise(cross(sub(p1, p0), sub(p2, p0))))

    if x < heights.shape[0] - 1 and y > 0:
        p1 = get_point(heights, cell_size, x + 1, y)
        p2 = get_point(heights, cell_size, x, y - 1)
        normals.append(normalise(cross(sub(p1, p0), sub(p2, p0))))

    if x < heights.shape[0] - 1 and y < heights.shape[1] - 1:
        p1 = get_point(heights, cell_size, x, y + 1)
        p2 = get_point(heights, cell_size, x + 1, y)
        normals.append(normalise(cross(sub(p1, p0), sub(p2, p0))))

    normal = [0, 0, 0]
    for n in normals:
        normal[0] += n[0]
        normal[1] += n[1]
        normal[2] += n[2]

    return normalise(normal)

def get_point(heights, cell_size, x, y):
    return (x * cell_size, y * cell_size, heights[x][y])

def cross(v1, v2):
    return  (
                v1[1] * v2[2] - v1[2] * v2[1],
                v1[2] * v2[0] - v1[0] * v2[2],
                v1[0] * v2[1] - v1[1] * v2[0]
            )

def sub(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])

def normalise(vec):
    length = math.sqrt(vec[0] * vec[0] + vec[1] * vec[1] + vec[2] * vec[2])
    return (vec[0] / length, vec[1] / length, vec[2] / length)
