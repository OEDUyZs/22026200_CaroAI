import random
import uuid

##### Interface #####

SIZE = 540
PIECE = 32

# Board size 9x9
N = 9

MARGIN = 23
GRID = (SIZE - 2 * MARGIN) / (N - 1)


def pixel_conversion(list_points, target):

    index = int((len(list_points) - 1) // 2)

    while True:

        if target < list_points[0]:
            index = 0
            break

        elif target >= list_points[-1]:
            index = len(list_points) - 2
            break

        elif list_points[index] > target:

            if list_points[index - 1] <= target:
                index -= 1
                break

            else:
                index -= 1

        elif list_points[index] <= target:

            if list_points[index + 1] > target:
                break

            else:
                index += 1

    return index


# pygame pixel -> board position
def pos_pixel2map(x, y):

    start = int(MARGIN - GRID // 2)
    end = int(SIZE - MARGIN + GRID // 2)

    list_points = [
        p for p in range(start, end + 1, int(GRID))
    ]

    i = pixel_conversion(list_points, y)
    j = pixel_conversion(list_points, x)

    return (i, j)


# board position -> pygame pixel
def pos_map2pixel(i, j):

    return (
        MARGIN + j * GRID - PIECE / 2,
        MARGIN + i * GRID - PIECE / 2
    )


def create_mapping():

    pos_mapping = {}

    for i in range(N):
        for j in range(N):

            spacing = [
                r for r in range(
                    MARGIN,
                    SIZE - MARGIN + 1,
                    int(GRID)
                )
            ]

            pos_mapping[(i, j)] = (
                spacing[j],
                spacing[i]
            )

    return pos_mapping


##### Evaluation patterns #####

def create_pattern_dict():

    patternDict = {}

    # AI = 1
    # HUMAN = -1

    for x in [1, -1]:

        enemy = -x

        multiplier = x

        # =========================
        # WIN (4)
        # =========================

        patternDict[(x, x, x, x)] = 1000000 * multiplier

        # =========================
        # OPEN 3
        # =========================

        patternDict[(0, x, x, x, 0)] = 100000 * multiplier

        patternDict[(0, x, 0, x, x, 0)] = 100000 * multiplier

        patternDict[(0, x, x, 0, x, 0)] = 100000 * multiplier

        # =========================
        # SEMI OPEN 3
        # =========================

        patternDict[(enemy, x, x, x, 0)] = 10000 * multiplier

        patternDict[(0, x, x, x, enemy)] = 10000 * multiplier

        # =========================
        # OPEN 2
        # =========================

        patternDict[(0, x, x, 0)] = 1000 * multiplier

        patternDict[(0, x, 0, x, 0)] = 1000 * multiplier

        # =========================
        # SEMI OPEN 2
        # =========================

        patternDict[(enemy, x, x, 0)] = 100 * multiplier

        patternDict[(0, x, x, enemy)] = 100 * multiplier

        # =========================
        # SINGLE PRESSURE
        # =========================

        patternDict[(0, x, 0)] = 10 * multiplier

    return patternDict


##### Zobrist Hashing #####

def init_zobrist():

    zTable = [
        [
            [uuid.uuid4().int for _ in range(2)]
            for j in range(N)
        ]
        for i in range(N)
    ]

    return zTable


def update_TTable(table, hash, score, depth):

    table[hash] = [score, depth]