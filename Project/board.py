import pygame

COLORS = [(255, 0, 0), (0, 255, 0), (0,0,255)]
squareSize = 20

def drawBoard(WIN, game, turn = False):
    WIN.fill((0,0,0))
    font = pygame.font.SysFont('comicsansms', 64)
    if turn:
        txt = font.render('Click to roll', True, (255,255,255))
    else: 
        for row in range(game.boardH):
            for col in range(game.boardW):
                pygame.draw.rect(WIN, COLORS[game.board[game.boardW*row+col]], (row*squareSize, col *squareSize, squareSize, squareSize))
            pygame.display.update()