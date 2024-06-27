import pygame
import sys
from game import Game

pygame.init()

if __name__ == '__main__':
    #print(sys.argv[1], sys.argv[2])
    #game = Game(True, int(sys.argv[1]), int(sys.argv[2]))
    game = Game(True, 0, 2)
    winner = game.run()
    if winner == 0:
        print('It is a draw')
    else:
        print('Winner is player ', winner)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

