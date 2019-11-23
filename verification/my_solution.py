def inscribe(contour):
    """ Find area and coordinates of the smallest rectangle
        which inscribes the given contour. """
    def rectangle_area(a, b):
        """ Compute the minimal rectangle area and coordinates
            containing the hull based on the edge (a, b). """
        # Line (a b) is the base of the rectangle. width, height ?
        # We are gonna change coordinates, still in complex plane.
        # Here, `a` is the origin, `b` is a point of x>0-axis.
        # Orthonormal base: (a ; I := a + dx ; J := a + dx * 1j). dx ?
        dx = (b - a) / abs(b - a)
        # The hull in this new base.
        new_hull = [(z - a) / dx for z in hull]
        xs, ys = [z.real for z in new_hull], [z.imag for z in new_hull]

        # Determine coordinates for the rectangle...
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = 0, max(ys, key=abs)  # min(ys, key=abs) == 0
        # In this new base, the rectangle is a simple bounding box.
        rect = (x_min, y_min), (x_min, y_max), (x_max, y_max), (x_max, y_min)
        # Go back to the right base (O, 1, i).
        rect = [a + dx * complex(*pt) for pt in rect]
        # Then to real coordinates.
        rect = [(z.real, z.imag) for z in rect]
        return abs(x_max - x_min) * abs(y_max - y_min), rect

    hull = [complex(*pt) for pt in convex_hull(contour)]
    return min(map(rectangle_area, hull, hull[1:]))


# My improved solution from "https://py.checkio.org/mission/convex-hull/".
from collections import namedtuple
Point = namedtuple('Point', 'x y')


def convex_hull(points):
    def slope(A, B): return (B.y - A.y) / (B.x - A.x)

    def next_high(A):
        try:  # Try to climb vertically.
            return min(B for B in points if B.x == A.x and B.y > A.y)
        except ValueError:
            # On the right of A, we want max slope then minimal abscissa.
            return max((B for B in points if B.x > A.x),
                       key=lambda B: (slope(A, B), -B.x))

    def next_low(A):
        try:  # Try to go down vertically.
            return max(B for B in points if B.x == A.x and B.y < A.y)
        except ValueError:
            # On the left of A, we want max slope then maximal abscissa.
            return max((B for B in points if B.x < A.x),
                       key=lambda B: (slope(A, B), B.x))

    points = {Point(*pt) for pt in points}
    start, middle = min(points), max(points)
    hull = [start]
    # Hull path: start ---high---> middle ---low---> start.
    for goal, next_point in ((middle, next_high), (start, next_low)):
        while hull[-1] != goal:
            pt = next_point(hull[-1])
            points.remove(pt)
            hull.append(pt)
    return hull  # NOTE: hull[-1] == start == hull[0]


if __name__ == '__main__':
    TESTS = [
        ([(1, 1), (1, 2), (0, 2), (3, 5), (3, 4), (4, 4)], 6.0),
        ([(6, 5), (10, 7), (2, 8)], 20.0),
        ([(2, 3), (3, 8), (8, 7), (9, 2), (3, 2),
          (4, 4), (6, 6), (7, 3), (5, 3)], 41.538),
        ([(0, 0), (0, 10), (0, 20), (100, 20), (100, 30),
          (120, 30), (120, 20), (120, 10), (20, 10), (20, 0)], 2679.208),
        ([(10, 250), (60, 300), (300, 60), (250, 10)], 24000.0),
        ([(10, 250), (60, 300), (110, 250), (160, 300),
          (210, 250), (160, 200), (300, 60), (250, 10)], 48000.0),
        ([(10, 5), (30, 105), (190, 105), (210, 5), (32, 7),
          (68, 15), (100, 77), (180, 30), (150, 20)], 20000.0),
        ([(5, 0), (0, 5), (50, 55), (55, 50), (70, 105), (105, 70),
          (120, 125), (125, 120), (170, 175), (175, 170)], 11600.503),
        ([(2, 2), (3, 3), (2, 4), (4, 3), (5, 3),
          (6, 4), (7, 3), (9, 4), (9, 3), (8, 2)], 14.0),
        ([(1, 2), (3, 6), (5, 2), (3, 1)], 16.0),
        ([(0, 2), (3, 5), (6, 2), (4, 1), (2, 1)], 18.0),
        ([(2, 2), (6, 1), (6, 3), (5, 4), (7, 5), (3, 6), (4, 3)], 17.0),
        ]

    from local_visualization import local_visualization

    points_and_rect = []
    for index, (points, answer) in enumerate(TESTS, 1):
        area, rect = inscribe(points)
        assert abs(area - answer) <= 1e-3
        points_and_rect.append((points, rect))

    local_visualization(*points_and_rect, nb_rows=3)
