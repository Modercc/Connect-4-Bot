import pygame
import random
import copy
from collections import defaultdict
from falling_chip import FallingChip
from tree import AlphaBetaTree, Node


class Game(object):
    width = 800
    height = 600
    radius = 20
    falling_chip = None
    next_player = 1
    colors = [(221, 191, 163), (221, 79, 79), (238, 234, 162), (8, 42, 123)]
    moves = []

    def __init__(self, isAnimated, player1, player2):

        self.isAnimated = isAnimated
        self.numCols = 7
        self.numRows = 6
        self.positioning = {}
        self.state = defaultdict(int)
        self.count = defaultdict(int)
        self.players = None, player1, player2

        if isAnimated:
            self.isFalling = False
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption('4 in a Row')
            self.clock = pygame.time.Clock()

            space = 20
            self.board_width = self.numCols * 2 * self.radius + (self.numCols + 1) * space
            self.board_x = (self.width - self.board_width) / 2
            self.board_height = self.numRows * 2 * self.radius + (self.numRows + 1) * space
            self.board_y = (self.height - self.board_height) / 2

            for i in range(self.numRows):
                for j in range(self.numCols):
                    hole_x = self.board_x + (j + 1) * (space + 2 * self.radius) - self.radius
                    hole_y = self.board_y + (i + 1) * (space + 2 * self.radius) - self.radius
                    self.positioning[(i, j)] = (hole_x, hole_y)

    def run(self):

        while True:
            self.clock.tick(27)
            self.render()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            if not self.isFalling:
                if self.players[self.next_player] == 0:
                    self.human()

                elif self.players[self.next_player] == 1:
                    self.random_strategy()

                elif self.players[self.next_player] == 2:
                    alphabetatree = AlphaBetaTree(self.state, self.count, self.next_player)
                    self.mini_max(alphabetatree.root, 7)

            elif self.falling_chip.fell():
                '''
                row = self.numRows - 1 - self.count[self.falling_chip.column]
                col = self.falling_chip.column
                self.state[(row, col)] = self.next_player
                self.count[col] += 1
                self.next_player = 3 - self.next_player
                '''
                self.state, self.count, self.next_player = self.updateGame(self.state, self.count, self.falling_chip.column, self.next_player)
                self.moves.append(self.falling_chip.column)
                self.isFalling = False
                result = self.checkResult(self.state)
                self.render()
                if result is not None:
                    return result

    def updateGame(self, state, count, move, current_player):
        state_copy = copy.copy(state)
        count_copy = copy.copy(count)

        row = self.numRows - 1 - count[move]
        col = move
        state_copy[(row, col)] = current_player
        count_copy[col] += 1
        next_player = 3 - current_player

        return state_copy, count_copy, next_player

    def toss_a_chip(self, col):
        x = self.positioning[(0, col)][0]
        y = self.board_y - 3 * self.radius
        rest_y = self.positioning[(self.numRows - 1 - self.count[col], col)][1]
        self.falling_chip = FallingChip(x, y, rest_y, self.colors[self.next_player], col)
        self.isFalling = True

    def render(self):
        self.screen.fill(self.colors[0])
        pygame.draw.rect(self.screen, self.colors[3], (self.board_x, self.board_y, self.board_width, self.board_height))

        for i in range(self.numRows):
            for j in range(self.numCols):
                pygame.draw.circle(self.screen, self.colors[self.state[(i, j)]], self.positioning[(i, j)], self.radius)

        if self.falling_chip is not None and not self.falling_chip.fell():
            pygame.draw.circle(self.screen, self.falling_chip.color, self.falling_chip.get_xy(), self.radius)
            self.falling_chip.move()

        pygame.display.update()

    def checkResult(self, state):
        # check for a winning row pattern
        for i in range(self.numRows):
            for j in range(self.numCols - 3):
                if state[(i, j)] != 0 and state[(i, j)] == state[(i, j + 1)] and state[
                    (i, j + 1)] == state[(i, j + 2)] and state[(i, j + 2)] == state[(i, j + 3)]:
                    return state[(i, j)] * (-2) + 3

        # check for a winning column pattern
        for j in range(self.numCols):
            for i in range(self.numRows - 3):
                if state[(i, j)] != 0 and state[(i, j)] == state[(i + 1, j)] and state[
                    (i + 1, j)] == state[(i + 2, j)] and state[(i + 2, j)] == state[(i + 3, j)]:
                    return state[(i, j)] * (-2) + 3

        # check for diagonals
        for i in range(self.numRows - 3):
            for j in range(self.numCols - 3):
                if state[(i, j)] != 0 and state[(i, j)] == state[(i + 1, j + 1)] and state[
                    (i + 1, j + 1)] == state[(i + 2, j + 2)] and state[(i + 2, j + 2)] == state[
                    (i + 3, j + 3)]:
                    return state[(i, j)] * (-2) + 3

                if state[(i, j + 3)] != 0 and state[(i, j + 3)] == state[(i + 1, j + 2)] and state[
                    (i + 1, j + 2)] == state[(i + 2, j + 1)] and state[(i + 2, j + 1)] == state[
                    (i + 3, j)]:
                    return state[(i, j + 3)] * (-2) + 3

        if self.count == [self.numRows for i in range(self.numCols)]:
            return 0

        return None

    def human(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_1] and self.count[0] < self.numRows:
            self.toss_a_chip(0)
        elif keys[pygame.K_2] and self.count[1] < self.numRows:
            self.toss_a_chip(1)
        elif keys[pygame.K_3] and self.count[2] < self.numRows:
            self.toss_a_chip(2)
        elif keys[pygame.K_4] and self.count[3] < self.numRows:
            self.toss_a_chip(3)
        elif keys[pygame.K_5] and self.count[4] < self.numRows:
            self.toss_a_chip(4)
        elif keys[pygame.K_6] and self.count[5] < self.numRows:
            self.toss_a_chip(5)
        elif keys[pygame.K_7] and self.count[6] < self.numRows:
            self.toss_a_chip(6)

    def possible_moves(self, count):
        moves = []

        for col in range(self.numCols):
            if count[col] < self.numRows:
                moves.append(col)

        return moves

    def random_strategy(self):
        pygame.time.delay(1000)

        moves = self.possible_moves(self.count)
        random_move = random.choice(moves)
        self.toss_a_chip(random_move)

    def mini_max(self, start_node, depth):
        node = start_node
        table = {}

        while True:
            index = node.index
            possible_moves = self.possible_moves(node.count)

            if index == len(possible_moves):

                if node == start_node:

                    print('Player', node.player, ': Moves: ', node.optimal_moves, '-> Value:', node.optimal_value)
                    decision = self.heuristic(node.optimal_moves, self.state, self.count, self.next_player)
                    self.toss_a_chip(decision)
                    return
                else:
                    table[self.turn_tuple(node.state)] = node.optimal_value
                    node = node.parent
                    depth += 1

            else:
                next_move = possible_moves[index]

                if node.children[next_move] is None:
                    state, count, player = self.updateGame(node.state, node.count, next_move, node.player)

                    if depth == 1:
                        outcome = 0

                    elif self.turn_tuple(state) in table:
                        outcome = table[self.turn_tuple(state)]

                    else:
                        outcome = self.checkResult(state)

                    if outcome is None:
                        node.children[next_move] = Node(state, count, player, node.alpha, node.beta, node)
                        node = node.children[next_move]
                        depth -= 1

                    else:
                        node.children[next_move] = outcome
                        node.index += 1
                        should_prune = node.update(next_move, outcome)

                        if should_prune:
                            node = node.parent
                            depth += 1
                else:
                    outcome = node.children[next_move].optimal_value
                    node.index += 1

                    should_prune = node.update(next_move, outcome)

                    if should_prune:
                        node = node.parent
                        depth += 1

    def turn_tuple(self, dict):
        ls = []

        for i in range(self.numRows):
            for j in range(self.numCols):
                ls.append(dict[(i, j)])

        return tuple(ls)

    def heuristic(self, moves, state, count, player):
        score = defaultdict(int)

        for move in moves:
            state1, _, _ = self.updateGame(state, count, move, player)
            state2, _, _ = self.updateGame(state, count, move, 3 - player)

            # check for a winning row pattern
            for i in range(self.numRows):
                for j in range(self.numCols - 3):
                    win_count = 0
                    lose_count = 0
                    for k in range(4):
                        if state1[(i, j + k)] == player:
                            win_count += 1
                        elif state1[(i, j + k)] == 3 - player:
                            lose_count += 1
                    score[move] += self.score_move(win_count, lose_count)

                    win_count = 0
                    lose_count = 0
                    for k in range(4):
                        if state2[(i, j + k)] == 3 - player:
                            win_count += 1
                        elif state2[(i, j + k)] == player:
                            lose_count += 1
                    score[move] -= self.score_move(win_count, lose_count)

            # check for a winning column pattern
            for j in range(self.numCols):
                for i in range(self.numRows - 3):
                    win_count = 0
                    lose_count = 0
                    for k in range(4):
                        if state1[(i + k, j)] == player:
                            win_count += 1
                        elif state1[(i + k, j)] == 3 - player:
                            lose_count += 1
                    score[move] += self.score_move(win_count, lose_count)

                    win_count = 0
                    lose_count = 0
                    for k in range(4):
                        if state2[(i + k, j)] == 3 - player:
                            win_count += 1
                        elif state2[(i + k, j)] == player:
                            lose_count += 1
                    score[move] -= self.score_move(win_count, lose_count)

            # check for diagonals
            for i in range(self.numRows - 3):
                for j in range(self.numCols - 3):
                    win_count = 0
                    lose_count = 0
                    for k in range(4):
                        if state1[(i + k, j + k)] == player:
                            win_count += 1
                        elif state1[(i + k, j + k)] == 3 - player:
                            lose_count += 1
                    score[move] += self.score_move(win_count, lose_count)

                    win_count = 0
                    lose_count = 0
                    for k in range(4):
                        if state2[(i + k, j + k)] == 3 - player:
                            win_count += 1
                        elif state2[(i + k, j + k)] == player:
                            lose_count += 1
                    score[move] -= self.score_move(win_count, lose_count)

                    win_count = 0
                    lose_count = 0
                    for k in range(4):
                        if state1[(i + k, j + 3 - k)] == player:
                            win_count += 1
                        elif state1[(i + k, j + 3 - k)] == 3 - player:
                            lose_count += 1
                    score[move] += self.score_move(win_count, lose_count)

                    win_count = 0
                    lose_count = 0
                    for k in range(4):
                        if state2[(i + k, j + 3 - k)] == 3 - player:
                            win_count += 1
                        elif state2[(i + k, j + 3 - k)] == player:
                            lose_count += 1
                    score[move] -= self.score_move(win_count, lose_count)

        best_move = moves[0]
        for move in moves:
            print('Move', move, ': Score', score[move])
            if score[best_move] < score[move]:
                best_move = move

            elif score[best_move] == score[move] and abs(best_move - self.numCols / 2) > abs(move - self.numCols / 2):
                best_move = move

        return best_move


    def score_move(self, good_tokens, bad_tokens):
        score = 0

        if bad_tokens == 0:
            if good_tokens == 2:
                score += 1

            elif good_tokens == 3:
                score += 5

        return score

'''
    def get_node(self):
        node = self.alphabetatree.root

        for move in self.moves:

            if node.children[move] is None:
                state, count, player = self.updateGame(node.state, node.count, move, node.player)
                node.children[move] = Node(state, count, player, float('-inf'), float('inf'), node)

            node = node.children[move]

        return node
'''





