import math
import sys
import source.utils as utils

sys.setrecursionlimit(3000)

# board size
N = 9


class GomokuAI():

    def __init__(self, depth=3):

        # =========================
        # SEARCH SETTINGS
        # =========================

        self.depth = depth

        # =========================
        # BOARD
        # =========================

        self.boardMap = [
            [0 for _ in range(N)]
            for _ in range(N)
        ]

        self.currentI = -1
        self.currentJ = -1

        self.boardValue = 0

        self.nextBound = {}

        # =========================
        # GAME STATE
        # =========================

        self.turn = 0

        self.lastPlayed = 0

        self.emptyCells = N * N

        # =========================
        # AI
        # =========================

        self.patternDict = utils.create_pattern_dict()

        self.zobristTable = utils.init_zobrist()

        self.rollingHash = 0

        self.TTable = {}

        # =========================
        # STATS
        # =========================

        self.nodeCount = 0

        self.pruneCount = 0

    # =========================================================
    # DEBUG BOARD
    # =========================================================

    def drawBoard(self):

        for i in range(N):

            for j in range(N):

                if self.boardMap[i][j] == 1:
                    state = 'X'

                elif self.boardMap[i][j] == -1:
                    state = 'O'

                else:
                    state = '.'

                print(f'{state}|', end=' ')

            print()

        print()

    # =========================================================
    # VALID MOVE
    # =========================================================

    def isValid(self, i, j, state=True):

        if i < 0 or i >= N:
            return False

        if j < 0 or j >= N:
            return False

        if state:

            if self.boardMap[i][j] != 0:
                return False

        return True

    # =========================================================
    # SET MOVE
    # =========================================================

    def setState(self, i, j, state):

        assert state in (-1, 0, 1)

        self.boardMap[i][j] = state

        self.lastPlayed = state

    # =========================================================
    # COUNT DIRECTION
    # =========================================================

    def countDirection(
        self,
        i,
        j,
        xdir,
        ydir,
        state
    ):

        count = 0

        for step in range(1, 4):

            new_j = j + xdir * step
            new_i = i + ydir * step

            if not self.isValid(new_i, new_j, False):
                break

            if self.boardMap[new_i][new_j] == state:
                count += 1

            else:
                break

        return count

    # =========================================================
    # CHECK WIN (Caro 4 quân)
    # =========================================================

    def isFour(self, i, j, state):

        directions = [
            [(-1, 0), (1, 0)],
            [(0, -1), (0, 1)],
            [(-1, 1), (1, -1)],
            [(-1, -1), (1, 1)]
        ]

        for axis in directions:

            axis_count = 1

            for (xdir, ydir) in axis:

                axis_count += self.countDirection(
                    i,
                    j,
                    xdir,
                    ydir,
                    state
                )

            if axis_count >= 4:
                return True

        return False

    # =========================================================
    # CHILD NODES
    # =========================================================

    def childNodes(self, bound):

        sorted_bound = sorted(
            bound.items(),
            key=lambda el: el[1],
            reverse=True
        )

        for pos in sorted_bound:

            yield pos[0]

    # =========================================================
    # UPDATE SEARCH BOUNDARY
    # =========================================================

    def updateBound(self, new_i, new_j, bound):

        played = (new_i, new_j)

        if played in bound:
            bound.pop(played)

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, 1),
            (1, -1),
            (-1, -1),
            (1, 1)
        ]

        for dir in directions:

            new_col = new_j + dir[0]

            new_row = new_i + dir[1]

            if self.isValid(new_row, new_col) \
                    and (new_row, new_col) not in bound:

                bound[(new_row, new_col)] = 0

    # =========================================================
    # PATTERN COUNTING
    # =========================================================

    def countPattern(
        self,
        i_0,
        j_0,
        pattern,
        score,
        bound,
        flag
    ):

        directions = [
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1)
        ]

        length = len(pattern)

        count = 0

        for dir in directions:

            if dir[0] * dir[1] == 0:

                steps_back = (
                    dir[0] * min(4, j_0)
                    + dir[1] * min(4, i_0)
                )

            elif dir[0] == 1:

                steps_back = min(4, j_0, i_0)

            else:

                steps_back = min(
                    4,
                    N - 1 - j_0,
                    i_0
                )

            i_start = i_0 - steps_back * dir[1]

            j_start = j_0 - steps_back * dir[0]

            z = 0

            while z <= steps_back:

                i_new = i_start + z * dir[1]

                j_new = j_start + z * dir[0]

                index = 0

                remember = []

                while index < length \
                        and self.isValid(i_new, j_new, False) \
                        and self.boardMap[i_new][j_new] == pattern[index]:

                    if self.isValid(i_new, j_new):

                        remember.append((i_new, j_new))

                    i_new += dir[1]

                    j_new += dir[0]

                    index += 1

                if index == length:

                    count += 1

                    for pos in remember:

                        if pos not in bound:
                            bound[pos] = 0

                        bound[pos] += flag * score

                    z += index

                else:

                    z += 1

        return count

    # =========================================================
    # EVALUATION FUNCTION
    # =========================================================

    def evaluate(
        self,
        new_i,
        new_j,
        board_value,
        turn,
        bound
    ):

        value_before = 0

        value_after = 0

        for pattern in self.patternDict:

            score = self.patternDict[pattern]

            value_before += \
                self.countPattern(
                    new_i,
                    new_j,
                    pattern,
                    abs(score),
                    bound,
                    -1
                ) * score

            # make move
            self.boardMap[new_i][new_j] = turn

            value_after += \
                self.countPattern(
                    new_i,
                    new_j,
                    pattern,
                    abs(score),
                    bound,
                    1
                ) * score

            # undo
            self.boardMap[new_i][new_j] = 0

        return board_value + value_after - value_before

    # =========================================================
    # PURE MINIMAX (Cho Level 1 & Báo cáo)
    # =========================================================

    def minimax(
        self,
        depth,
        board_value,
        bound,
        maximizingPlayer
    ):
        
        self.nodeCount += 1

        # terminal node
        if depth <= 0 or self.checkResult() is not None:
            return board_value

        if maximizingPlayer:

            max_val = -math.inf

            for child in self.childNodes(bound):

                i, j = child
                new_bound = dict(bound)

                new_val = self.evaluate(
                    i,
                    j,
                    board_value,
                    1,
                    new_bound
                )

                # make move
                self.boardMap[i][j] = 1
                self.updateBound(i, j, new_bound)

                eval = self.minimax(
                    depth - 1,
                    new_val,
                    new_bound,
                    False
                )

                if eval > max_val:

                    max_val = eval

                    if depth == self.depth:
                        self.currentI = i
                        self.currentJ = j
                        self.boardValue = eval
                        self.nextBound = new_bound

                # undo
                self.boardMap[i][j] = 0

            return max_val

        else:

            min_val = math.inf

            for child in self.childNodes(bound):

                i, j = child
                new_bound = dict(bound)

                new_val = self.evaluate(
                    i,
                    j,
                    board_value,
                    -1,
                    new_bound
                )

                # make move
                self.boardMap[i][j] = -1
                self.updateBound(i, j, new_bound)

                eval = self.minimax(
                    depth - 1,
                    new_val,
                    new_bound,
                    True
                )

                if eval < min_val:

                    min_val = eval

                    if depth == self.depth:
                        self.currentI = i
                        self.currentJ = j
                        self.boardValue = eval
                        self.nextBound = new_bound

                # undo
                self.boardMap[i][j] = 0

            return min_val

    # =========================================================
    # ALPHA-BETA PRUNING (Cho Level 2 & Báo cáo)
    # =========================================================

    def alphaBetaPruning(
        self,
        depth,
        board_value,
        bound,
        alpha,
        beta,
        maximizingPlayer
    ):

        self.nodeCount += 1

        # terminal node
        if depth <= 0 or self.checkResult() is not None:

            return board_value

        # transposition table
        if self.rollingHash in self.TTable:

            stored_score, stored_depth = \
                self.TTable[self.rollingHash]

            if stored_depth >= depth:

                return stored_score

        # =====================================================
        # MAX PLAYER
        # =====================================================

        if maximizingPlayer:

            max_val = -math.inf

            for child in self.childNodes(bound):

                i, j = child

                new_bound = dict(bound)

                new_val = self.evaluate(
                    i,
                    j,
                    board_value,
                    1,
                    new_bound
                )

                # make move
                self.boardMap[i][j] = 1

                self.rollingHash ^= \
                    self.zobristTable[i][j][0]

                self.updateBound(
                    i,
                    j,
                    new_bound
                )

                eval = self.alphaBetaPruning(
                    depth - 1,
                    new_val,
                    new_bound,
                    alpha,
                    beta,
                    False
                )

                if eval > max_val:

                    max_val = eval

                    if depth == self.depth:

                        self.currentI = i
                        self.currentJ = j

                        self.boardValue = eval

                        self.nextBound = new_bound

                alpha = max(alpha, eval)

                # undo
                self.boardMap[i][j] = 0

                self.rollingHash ^= \
                    self.zobristTable[i][j][0]

                if beta <= alpha:

                    self.pruneCount += 1

                    break

            utils.update_TTable(
                self.TTable,
                self.rollingHash,
                max_val,
                depth
            )

            return max_val

        # =====================================================
        # MIN PLAYER
        # =====================================================

        else:

            min_val = math.inf

            for child in self.childNodes(bound):

                i, j = child

                new_bound = dict(bound)

                new_val = self.evaluate(
                    i,
                    j,
                    board_value,
                    -1,
                    new_bound
                )

                # make move
                self.boardMap[i][j] = -1

                self.rollingHash ^= \
                    self.zobristTable[i][j][1]

                self.updateBound(
                    i,
                    j,
                    new_bound
                )

                eval = self.alphaBetaPruning(
                    depth - 1,
                    new_val,
                    new_bound,
                    alpha,
                    beta,
                    True
                )

                if eval < min_val:

                    min_val = eval

                    if depth == self.depth:

                        self.currentI = i
                        self.currentJ = j

                        self.boardValue = eval

                        self.nextBound = new_bound

                beta = min(beta, eval)

                # undo
                self.boardMap[i][j] = 0

                self.rollingHash ^= \
                    self.zobristTable[i][j][1]

                if beta <= alpha:

                    self.pruneCount += 1

                    break

            utils.update_TTable(
                self.TTable,
                self.rollingHash,
                min_val,
                depth
            )

            return min_val

    # =========================================================
    # FIRST MOVE
    # =========================================================

    def firstMove(self):

        self.currentI = 4
        self.currentJ = 4

        self.setState(
            self.currentI,
            self.currentJ,
            1
        )

    # =========================================================
    # RESULT
    # =========================================================

    def checkResult(self):

        if self.isFour(
            self.currentI,
            self.currentJ,
            self.lastPlayed
        ) and self.lastPlayed in (-1, 1):

            return self.lastPlayed

        elif self.emptyCells <= 0:

            return 0

        else:

            return None

    # =========================================================
    # WINNER
    # =========================================================

    def getWinner(self):

        result = self.checkResult()

        if result == 1:

            return 'AI'

        elif result == -1:

            return 'PLAYER'

        return 'NONE'