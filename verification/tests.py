from my_solution import inscribe
from random import randint
from math import hypot


def random_point(MIN=0, MAX=300):  # Too crazy?!
    """ Random 2D point with random number of decimals. """
    x, y = randint(0, 2), randint(0, 2)
    return tuple(randint(MIN, MAX * 10**i) / 10**i
                 if i else randint(MIN, MAX)
                 for i in (x, y))


def distance(x1, y1, x2, y2): return hypot(x2 - x1, y2 - y1)


def colinear(x1, y1, x2, y2): return x1 * y2 == y1 * x2


def random_points(min_distance=10):
    nb_points = randint(3, 30)
    while True:
        result = []
        while len(result) != nb_points:
            # It could be an infinite loop if min_distance is too big.
            pt = random_point()
            # TEST "there won't be two (or more) similar dots"
            if all(distance(*pt, *a) >= min_distance for a in result):
                result.append(pt)
        # TEST "there won't be a case with all the dots on the same line"
        pt = result[0]
        vectors = ((pt[0] - a[0], pt[1] - a[1]) for a in result[1:])
        v1 = next(vectors)
        if not all(colinear(*v1, *v2) for v2 in vectors):
            return result
        # It's very unlikely for random points to be all colinears.
        # Start again if that happens...


TESTS = {
    "Basics": [
        {
            "input": [[(1, 1), (1, 2), (0, 2), (3, 5), (3, 4), (4, 4)]],
            "answer": 6.0,
            'explanation': [(0.0, 2.0), (1.0, 1.0), (4.0, 4.0), (3.0, 5.0)],
        },
        {
            "input": [[(6, 5), (10, 7), (2, 8)]],
            "answer": 20.0,
            'explanation': [(2.0, 8.0), (1.692, 5.538), (9.692, 4.538), (10.0, 7.0)],
        },
        {
            "input": [[(2, 3), (3, 8), (8, 7), (9, 2), (3, 2), (4, 4), (6, 6), (7, 3), (5, 3)]],
            "answer": 41.538,
            'explanation': [(1.846, 2.231), (8.769, 0.846), (9.923, 6.615), (3.0, 8.0)],
        },
        {
            "input": [
                [(0, 0), (0, 10), (0, 20), (100, 20), (100, 30), (120, 30), (120, 20), (120, 10), (20, 10), (20, 0)]],
            "answer": 2679.208,
            'explanation': [(-1.98, 19.802), (0.198, -1.98), (121.98, 10.198), (119.802, 31.98)],
        },
        {
            "input": [[(10, 250), (60, 300), (300, 60), (250, 10)]],
            "answer": 24000.0,
            'explanation': [(10.0, 250.0), (250.0, 10.0), (300.0, 60.0), (60.0, 300.0)],
        },
        {
            "input": [[(10, 250), (60, 300), (110, 250), (160, 300), (210, 250), (160, 200), (300, 60), (250, 10)]],
            "answer": 48000.0,
            'explanation': [(10.0, 250.0), (250.0, 10.0), (350.0, 110.0), (110.0, 350.0)],
        }
    ],
    "Extra": [
        {
            "input": [[(10, 5), (30, 105), (190, 105), (210, 5), (32, 7), (68, 15), (100, 77), (180, 30), (150, 20)]],
            "answer": 20000.0,
            'explanation': [(10.0, 105.0), (10.0, 5.0), (210.0, 5.0), (210.0, 105.0)],
        },
        {
            "input": [[(5, 0), (0, 5), (50, 55), (55, 50), (70, 105), (105, 70), (120, 125), (125, 120), (170, 175), (175, 170)]],
            "answer": 11600.503,
            'explanation': [(-23.96, 39.228), (3.993, -0.705), (198.96, 135.772), (171.007, 175.705)],
        },
        {
            "input": [[(2, 2), (3, 3), (2, 4), (4, 3), (5, 3), (6, 4), (7, 3), (9, 4), (9, 3), (8, 2)]],
            "answer": 14.0,
            'explanation': [(2.0, 2.0), (9.0, 2.0), (9.0, 4.0), (2.0, 4.0)],
        },
        {
            "input": [[(1, 2), (3, 6), (5, 2), (3, 1)]],
            "answer": 16.0,
            'explanation': [(1.0, 2.0), (4.2, 0.4), (6.2, 4.4), (3.0, 6.0)],
        },
        {
            "input": [[(0, 2), (3, 5), (6, 2), (4, 1), (2, 1)]],
            "answer": 18.0,
            'explanation': [(0.0, 2.0), (3.0, -1.0), (6.0, 2.0), (3.0, 5.0)],
        },
        {
            "input": [[(2, 2), (6, 1), (6, 3), (5, 4), (7, 5), (3, 6), (4, 3)]],
            "answer": 17.0,
            'explanation': [(2.0, 2.0), (6.0, 1.0), (7.0, 5.0), (3.0, 6.0)],
        }
    ],
    'Random': [],
    }

for _ in range(10):
    pts = random_points()
    area, rect = inscribe(pts)
    rect = [(round(x, 3), round(y, 3)) for x, y in rect]
    TESTS['Random'].append(dict(input=[pts], answer=area, explanation=rect))


if __name__ == '__main__':
    # To visualize on local machine.
    from pprint import pprint
    import matplotlib.pyplot as plt
    pprint(TESTS)

    all_tests = [test for lst in TESTS.values() for test in lst]
    print(len(all_tests), 'tests.')

    for index, test in enumerate(all_tests, 1):
        points = test['input'][0]

        # To remember to add explanations for the 12 first tests.
        try:
            rect = test['explanation']
        except KeyError:
            print(f'explanation missing at test #{index}')
            rect = inscribe(points)[1]
            rect = [(round(x, 3), round(y, 3)) for x, y in rect]
            print(rect)
        rect.append(rect[0])  # useful to visualize all four edges.

        # In each subplot: black points in a green rectangle, the smallest one.
        plt.subplot(5, 5, index)  # nb_row, nb_col, index
        plt.plot([p[0] for p in points],
                 [p[1] for p in points],
                 color='black',
                 marker='.',
                 linestyle='')
        plt.plot([p[0] for p in rect],
                 [p[1] for p in rect],
                 color='green',
                 linestyle='-', lw=.5)
        plt.axis('equal')  # rectangles look like rectangles now.
    plt.show()
