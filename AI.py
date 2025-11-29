import pygame
from copy import deepcopy
from random import choice, randint
from math import sqrt

log2 = {2 ** i: i for i in range(1, 14)}

class Node:
    def __init__(self, board, parent, action, score, depth) -> None:
        self.board = board
        self.parent = parent
        self.action = action
        self.score = score
        self.val = self.get_val()
        self.depth = depth
    
    def get_val(self):
        """Generate a heuristic value for the node/board state."""

        if self.check_terminal() or self.score == 0:
            return 0
        
        positioning_score = 0

        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j]:
                    positioning_score += (i + j) * (self.board[i][j] ** log2[self.board[i][j]])

        return positioning_score * sqrt(self.score)

    def check_terminal(self):
        """Check if the board is in a terminal state (no moves left)."""

        if not any(row.count(0) for row in self.board):
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    tile = self.board[i][j]
                    if 0 < j < 3 and (tile == self.board[i][j + 1] or tile == self.board[i][j - 1]):
                        return False
                    if 0 < i < 3 and (tile == self.board[i + 1][j] or tile == self.board[i - 1][j]):
                        return False

            return True

    def move(self, action, merged, board):
        """Move the tiles on the board in the specified direction."""

        if not board:
            board = deepcopy(self.board)
        copy = deepcopy(board)
        score = 0
        i_range = []
        j_range = []
        match action:
            case pygame.K_LEFT:
                i_range = range(len(board))
                j_range = range(len(board))
                i_increment = 0
                j_increment = -1

            case pygame.K_RIGHT:
                i_range = range(len(board))
                j_range = range(len(board))[::-1]
                i_increment = 0
                j_increment = 1

            case pygame.K_UP:
                i_range = range(len(board))
                j_range = range(len(board))
                i_increment = -1
                j_increment = 0

            case pygame.K_DOWN:
                i_range = range(len(board))[::-1]
                j_range = range(len(board))
                i_increment = 1
                j_increment = 0

        for i in i_range:
            for j in j_range:
                if board[i][j]:
                    tile = board[i][j]
                    next_i = i + i_increment
                    next_j = j + j_increment
                    if not (0 <= next_i <= 3 and 0 <= next_j <= 3):
                        continue
                    if (
                        tile == board[next_i][next_j]
                        and (next_i, next_j) not in merged
                        and (i, j) not in merged
                    ):
                        board[i][j] = 0
                        board[next_i][next_j] = 2 * tile
                        score += 2 * tile
                        merged.append((next_i, next_j))
                    elif board[next_i][next_j] == 0:
                        board[next_i][next_j] = tile
                        board[i][j] = 0

        if copy != board:
            score += self.move(action, merged, board)[1]
            return board, score

        return False, score

class AI:
    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.board = []
        self.last_best_result = None
        self.explored = []

    def update_board(self, board):
        self.board = deepcopy(board)

    def move(self):
        """Decide the best move to make using a depth-limited search algorithm."""

        self.frontier = [Node(self.board, None, None, 0, 0)]
        self.explored = []
        node = self.search()
        while node.parent.parent:
            node = node.parent

        return node.action

    def add_nodes(self, node):
        """Add neighbouring nodes to the frontier."""

        actions = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
        for action in actions:
            state = node.move(action, [], [])
            if state[0]:
                board, score = state
        
                empty = []
                for i in range(len(board)):
                    for j in range(len(board)):
                        if not board[i][j]:
                            empty.append((i, j))

                x, y = choice(empty)
                if randint(1, 10) == 1:
                    board[x][y] = 4
                else:
                    board[x][y] = 2

                self.frontier.append(Node(board, node, action, node.score + score, node.depth + 1))          

    def search(self):
        """Perform the depth-limited search to find the best move."""

        current = min(self.frontier, key=lambda node: node.depth)
        if current.depth == self.max_depth:
            best_result = max(self.frontier, key=lambda node: node.val)
            self.last_best_result = best_result
            return best_result
        
        self.add_nodes(current)

        if len(self.frontier) == 1:
            self.explored.append(current)
            best_result = max(self.explored, key=lambda node: node.val)
            return best_result      

        self.frontier.remove(current)
        if current.parent:
            self.explored.append(current)
        return self.search()
