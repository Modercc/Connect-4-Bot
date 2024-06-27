from collections import defaultdict


class AlphaBetaTree(object):

    alpha = float('-inf')
    beta = float('inf')

    def __init__(self, state, count, player):
        self.root = Node(state, count, player, float('-inf'), float('inf'), None)

class Node(object):

    def __init__(self, state, count, player, alpha, beta, parent):
        self.state = state
        self.count = count
        self.player = player
        self.parent = parent
        self.children = defaultdict(lambda: None)
        self.alpha = alpha
        self.beta = beta
        self.optimal_moves = []
        self.index = 0

        if player == 1:
            self.optimal_value = float('-inf')
        else:
            self.optimal_value = float('inf')

    def update(self, move, value):

        if self.player == 1:

            if self.optimal_value < value:
                self.optimal_value = value
                self.optimal_moves = [move]

                if self.alpha < value:
                    self.alpha = value

                    if self.beta < self.alpha:
                        #print('cut')
                        return True

            elif self.optimal_value == value:
                self.optimal_moves.append(move)

        else:

            if self.optimal_value > value:
                self.optimal_value = value
                self.optimal_moves = [move]

                if self.beta > value:
                    self.beta = value

                    if self.beta < self.alpha:
                        #print('cut')
                        return True

            elif self.optimal_value == value:
                self.optimal_moves.append(move)

        return False


