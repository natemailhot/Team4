import os
import random
from pydub import AudioSegment
from pydub.playback import play
import IMU_main
import medium_mode_DandF as speech
import camera
import IMU_main
import camera
import medium_mode_DandF as speech
from game import Game

game = Game(1)
pygame.font.init()

FPS = 60

WIDTH, HEIGHT = 1400, 800
#number of squares per edge of game board
BOARD_EDGE = 5
#size of game board
BOARD_EDGE_SIZE = 500
#size of each square in the game board
SQUARE_EDGE = BOARD_EDGE_SIZE/BOARD_EDGE
TEXT_HEIGHT = (HEIGHT - BOARD_EDGE_SIZE)* 3/4 + BOARD_EDGE_SIZE

DIE_LENGTH = 150

SQUARE_WIDTH = WIDTH//7

def drawBoardGrid(game, players = 2):
    board_height_start = (HEIGHT - BOARD_EDGE_SIZE)/2
    board_width_start = (WIDTH - BOARD_EDGE_SIZE)/2

    for i in range(game.boardH):
        board_width_start = (WIDTH - BOARD_EDGE_SIZE)/2
        for j in range(game.boardW):
            if game.board[i][j] == 0:
                WIN.blit(red,(board_width_start,board_height_start))
            elif game.board[i][j] == 1:
                WIN.blit(yellow,(board_width_start,board_height_start))
            elif game.board[i][j] == 2:
                WIN.blit(blue,(board_width_start,board_height_start))
            else:
                print("ERROR: Board numbers are wrong")
            board_width_start += SQUARE_EDGE
        board_height_start += SQUARE_EDGE

    #for i in range(game.numPlayers):
    r1 = BOARD_EDGE - game.spots[0]//BOARD_EDGE
    c1 = BOARD_EDGE - game.spots[0]%BOARD_EDGE
    r2 = BOARD_EDGE - game.spots[1] // BOARD_EDGE
    c2 = BOARD_EDGE - game.spots[1]%BOARD_EDGE
    w1 = WIDTH - 350
    #(WIDTH - BOARD_EDGE_SIZE)/2 - 2*SQUARE_EDGE
    h1 = 75
    WIN.blit(p1,(w1 - (c1+1)*SQUARE_EDGE, h1 + r1*SQUARE_EDGE))
    if players > 1:
        WIN.blit(p2,(w1 - (c2+1)*SQUARE_EDGE+50,h1 + r2*SQUARE_EDGE))
