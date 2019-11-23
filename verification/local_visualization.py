import matplotlib.pyplot as plt


def local_visualization(*points_and_rect, nb_rows=1):
    """ Visualize differents plots in one. """
    q, r = divmod(len(points_and_rect), nb_rows)
    nb_cols = q + (r > 0)
    for index, (points, rect) in enumerate(points_and_rect, 1):
        plt.subplot(nb_rows, nb_cols, index)
        # Black points.
        plt.plot([p[0] for p in points],
                 [p[1] for p in points],
                 color='black',
                 marker='.',
                 linestyle='')
        # Green rectangle.
        rect.append(rect[0])
        plt.plot([p[0] for p in rect],
                 [p[1] for p in rect],
                 color='green',
                 linestyle='-', lw=.5)
        # Make rectangles look like rectangles.
        plt.axis('equal')
    plt.show()
