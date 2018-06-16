from shapely.geometry import Polygon
from math import (
    fabs,
    pow,
    sqrt
)

class Word(object):
    def __init__(self, id, text, word):
        self.id = id
        self.word = word
        self.vertices = self.get_vertices(word['boundingBox'])
        self.text = text

        polygon, expanded_polygon = self.build_polygons()
        self.polygon = polygon
        self.expanded_polygon = expanded_polygon

    @property
    def height(self):
        x, y = self.polygon.exterior.coords.xy
        return fabs(sqrt((
            pow(x[3] - x[0], 2) +
            pow(y[3] - y[0], 2)
        )))

    def build_polygons(self):
        polygon = Polygon(self.vertices)
        expanded_polygon = Polygon(polygon.buffer(1.0).exterior, [self.vertices])
        return polygon, expanded_polygon

    def get_vertices(self, bound):
        return self.reorientate_vertices([
            (bound['vertices'][0]['x'], bound['vertices'][0]['y']),
            (bound['vertices'][1]['x'], bound['vertices'][1]['y']),
            (bound['vertices'][2]['x'], bound['vertices'][2]['y']),
            (bound['vertices'][3]['x'], bound['vertices'][3]['y'])
        ])

    def reorientate_vertices(self, vertices):
        center_x = 0
        center_y = 0
        for vertice in vertices:
            center_x += vertice[0]
            center_y += vertice[1]

        center_x = center_x/4
        center_y = center_y/4

        point_x = vertices[0][0]
        point_y = vertices[0][1]
        if point_x < center_x:
            # 0 --- 1
            # |     |
            # 3 --- 2
            if point_y < center_y:
                return vertices

            # 1 --- 2
            # |     |
            # 0 --- 3
            return [
                vertices[1],
                vertices[2],
                vertices[3],
                vertices[0]
            ]

        # 3 --- 0
        # |     |
        # 2 --- 1
        if point_y < center_y:
            return [
                vertices[3],
                vertices[0],
                vertices[1],
                vertices[2]
            ]

        # 2 --- 3
        # |     |
        # 1 --- 0
        return [
            vertices[2],
            vertices[3],
            vertices[0],
            vertices[1]
        ]

    def debug_polygon(self):
        x, y = self.polygon.exterior.xy
        return "Polygon({}, {}, {}, {})".format(
            (x[0], y[0]),
            (x[1], y[1]),
            (x[2], y[2]),
            (x[3], y[3])
        )
    def debug_expanded_polygon(self):
        x, y = self.polygon.exterior.xy
        return "Polygon({}, {}, {}, {})".format(
            (x[0], y[0]),
            (x[1], y[1]),
            (x[2], y[2]),
            (x[3], y[3])
        )

    def __repr__(self):
        return u"{} - {}".format("\n".join(self.text), self.debug_polygon()).encode('utf-8').strip()
