from tkinter.tix import TEXT
import pygame
from network import Network
import time
import random
from pydub import AudioSegment
from pydub.playback import play
# from board import drawBoard


## Pygame Inits
pygame.font.init()

WIDTH, HEIGHT = 1400, 800
#number of squares per edge of game board
BOARD_EDGE = 5
#size of game board
BOARD_EDGE_SIZE = 500
#size of each square in the game board
SQUARE_EDGE = BOARD_EDGE_SIZE/BOARD_EDGE
SQUARE_WIDTH = WIDTH//7
#height the game text should be
TEXT_HEIGHT = (HEIGHT - BOARD_EDGE_SIZE)* 3/4 + BOARD_EDGE_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")
MODES = ['Keyboard', 'IMU', 'Camera', 'Speech']
SOUNDS = ['Notes/A3.wav', 'Notes/B3.wav', 'Notes/C4.wav', 'Notes/D4.wav', 'Notes/E4.wav', 'Notes/F4.wav', 'Notes/G4.wav']
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

board = [[0] * BOARD_EDGE for i in range(BOARD_EDGE)]

red=pygame.image.load("red.jpg")
yellow=pygame.image.load("yellow.jpg")
blue=pygame.image.load("blue.jpg")
p1=pygame.image.load("p1.jpg")
p2=pygame.image.load("p2.jpg")

#adjust images to correct size
red=pygame.transform.scale(red, (SQUARE_EDGE, SQUARE_EDGE))
yellow=pygame.transform.scale(yellow, (SQUARE_EDGE, SQUARE_EDGE))
blue=pygame.transform.scale(blue, (SQUARE_EDGE, SQUARE_EDGE))
p1=pygame.transform.scale(p1, (SQUARE_EDGE, SQUARE_EDGE))
p2=pygame.transform.scale(p2, (SQUARE_EDGE, SQUARE_EDGE))

def drawWindow(WIN, game):

    WIN.fill((0,0,0))

    font = pygame.font.SysFont('comicsansms', 64)
    text = font.render("Waiting for Player...", True, (255,255,255))
    WIN.blit(text, text.get_rect(center = (WIDTH/2, HEIGHT/2)))
    pygame.display.update()

def makeBoard():
        for i in range(BOARD_EDGE):
            for j in range(BOARD_EDGE):
                y = random.randint(0, 2)
                board[i][j] = y

def drawBoardGrid(game):
    board_height_start = (HEIGHT - BOARD_EDGE_SIZE)/2
    board_width_start = (WIDTH - BOARD_EDGE_SIZE)/2

    for i in range(game.boardH):
        board_width_start = (WIDTH - BOARD_EDGE_SIZE)/2
        for j in range(game.boardW):
            if board[i][j] == 0:
                WIN.blit(red,(board_width_start,board_height_start))
            elif board[i][j] == 1:
                WIN.blit(yellow,(board_width_start,board_height_start))
            elif board[i][j] == 2:
                WIN.blit(blue,(board_width_start,board_height_start))
            else:
                print("ERROR: Board numbers are wrong")
            board_width_start += SQUARE_EDGE
        board_height_start += SQUARE_EDGE

    #WIN.blit(p1,((WIDTH - BOARD_EDGE_SIZE)/2 - SQUARE_EDGE,(HEIGHT - BOARD_EDGE_SIZE)/2 - SQUARE_EDGE))
    #WIN.blit(p2,((WIDTH - BOARD_EDGE_SIZE)/2 - SQUARE_EDGE,(HEIGHT - BOARD_EDGE_SIZE)/2 - SQUARE_EDGE))

def drawBoard(WIN, game, turn = False):
    WIN.fill((0,0,0))
    font = pygame.font.SysFont('comicsansms', 64)

    #add if statement if you ever want to no print the board
    drawBoardGrid(game)

    if turn:
        txt = font.render('Click to roll', True, (255,255,255))     
    else:
        txt = font.render('Player ' + str(game.currPlayer + 1) + ': ' + str(game.spots[game.currPlayer]), True, (255,255,255))
    txtRect = txt.get_rect(center = (WIDTH/2, TEXT_HEIGHT)) #center for the text
    WIN.blit(txt, txtRect)
    pygame.display.update()

    ## TO DO: draw game board and msg: "Click to roll dice"


def drawDiceRoll(WIN, game):
    WIN.fill((0,0,0))
    font = pygame.font.SysFont('comicsansms', 64)
    txt = font.render('Rolled a ' + str(game.currRoll), True, (255,255,255))
    txtRect = txt.get_rect(center = (WIDTH/2, TEXT_HEIGHT))
    WIN.blit(txt, txtRect)
    pygame.display.update()
    pygame.time.delay(3000)
    ## TO DO: make animation for dice roll

def drawMove(WIN):
    WIN.fill((0,0,0))
    font = pygame.font.SysFont('comicsansms', 64)
    txt = font.render('Move animation' , True, (255,255,255))
    txtRect = txt.get_rect(center = (WIDTH/2, TEXT_HEIGHT))
    WIN.blit(txt, txtRect)
    pygame.display.update()
    pygame.time.delay(3000)
    ## TO DO: make animation for player movement on board

def drawTurn(WIN):
    WIN.fill((0,0,0))
    font = pygame.font.SysFont('comicsansms', 64)
    txt = font.render("Other player's move" , True, (255,255,255))
    txtRect = txt.get_rect(center = (WIDTH/2, TEXT_HEIGHT))
    WIN.blit(txt, txtRect)
    pygame.display.update()

def drawEnd(WIN, game):
    WIN.fill((0,0,0))
    font = pygame.font.SysFont('comicsansms', 64)
    txt = font.render("Player " + str(game.winner + 1) + " wins!" , True, (255,255,255))
    txtRect = txt.get_rect(center = (WIDTH/2, HEIGHT/2))
    WIN.blit(txt, txtRect)
    pygame.display.update()

def drawSound(WIN, note):
    WIN.fill((0,0,0))
    font = pygame.font.SysFont('Arial', 64)
    for i in range(7):
        if i == note:
            pygame.draw.rect(WIN, (255, 0, 0), pygame.Rect(i*SQUARE_WIDTH, HEIGHT//2-(SQUARE_WIDTH//2), SQUARE_WIDTH, SQUARE_WIDTH), 3)
        else:
            pygame.draw.rect(WIN, (0, 255, 0), pygame.Rect(i*SQUARE_WIDTH, HEIGHT//2-(SQUARE_WIDTH//2), SQUARE_WIDTH, SQUARE_WIDTH), 3)
        txt = font.render(LETTERS[i], True, (255,255,255))
        txtRect = txt.get_rect(center = (i*SQUARE_WIDTH + SQUARE_WIDTH//2, HEIGHT//2))
        WIN.blit(txt, txtRect)
    pygame.display.update()

def playSound(WIN,game):
    for i in range(game.currRoll):
        drawSound(WIN, game.melody[i])
        sound = AudioSegment.from_wav(SOUNDS[game.melody[i]])
        play(sound)

def main():
    n = Network()
    player = int(n.getP())
    run = True
    clock = pygame.time.Clock()
    makeBoard()

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            menu_screen()


        if not game.connected():
            drawWindow(WIN, game)
        
        else:

            if game.phase == 'board':
                if game.currPlayer == player:
                    drawBoard(WIN, game, True)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        n.send('board')
                else:
                    drawBoard(WIN, game)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                        
            
            elif game.phase == 'dice':
                if game.currPlayer == player:
                    roll = random.randint(1, 12)
                    n.send(str(roll))
                if game.rolled:
                    drawDiceRoll(WIN, game)
                    n.send('dice')
            
            elif game.phase == 'turn':
                if game.currPlayer == player:
                    if not game.went:
                        playSound(WIN, game)
                        ans = game.play()
                        n.send(ans)
                    else:
                        print("Went")
                        if game.correct:
                            drawMove(WIN)
                            n.send('move')
                        else:
                            n.send('turn')
                else:
                    drawTurn(WIN)
            
            elif game.phase == 'end':
                drawEnd(WIN, game)
                n.send('reset')
                n.close()
                menu_screen()
        

        ## If both player went, next round or reset
        # if game.bothWent():
        #     WIN.fill((0,0,0))
        #     pygame.time.delay(500)

        #     font = pygame.font.SysFont('comicsansms', 64)

        #     if game.getP1() and game.getP2():
        #         txt = font.render('Both players correct!', True, (255,255,255))
        #         txtRect = txt.get_rect(center = (WIDTH/2, HEIGHT/2))
        #         WIN.blit(txt, txtRect)
        #         pygame.display.update()
        #         pygame.time.delay(5000)
        #         try:
        #             game = n.send("next")
        #         except:
        #             run = False
        #             print("Couldn't make new round")
        #             break
        #     else:
        #         try:
        #             if game.getP1():
        #                 winner = '1'
        #             else:
        #                 winner = '2'

        #             txt = font.render('Player ' + winner + ' wins!', True, (255,255,255))
        #             txtRect = txt.get_rect(center = (WIDTH/2, HEIGHT/2))
        #             WIN.blit(txt, txtRect)
        #             pygame.display.update()
        #             pygame.time.delay(5000)
        #             game = n.send("reset")
        #         except:
        #             run = False
        #             print("Couldn't get game")
        #             break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        
        # if game.connected():
        #     if game.getWent(player):
        #         WIN.fill((0,0,0))
        #         font = pygame.font.SysFont('comicsansms', 64)
        #         text = font.render("Waiting...", True, (255,255,255))
        #         WIN.blit(text, text.get_rect(center = (WIDTH/2, HEIGHT/2)))
        #         pygame.display.update()
        #     else:
        #         drawWindow(WIN, game)
        #         game.playSound()
        #         ans = game.play(player, MODE)
        #         print(ans)
        #         n.send(MODE + ' ' + ans)        
        # else:
        #     drawWindow(WIN, game)

        


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        WIN.fill((0,0,0))


        font = pygame.font.SysFont('comicsansms', 64)
        subfont = pygame.font.SysFont('comicsansms', 48)
        text = font.render('PitchPerfect.io', False, (255,255,255))
        subtext = subfont.render("Press any key to start", False, (255,255,255))
        #subtext = subfont.render("Mode: (K)eyboard, (I)MU, (C)amera, (S)peech", False, (255,255,255))
        centerRect = text.get_rect(center = (WIDTH/2, HEIGHT/2))
        subRect = subtext.get_rect(center = (WIDTH/2, HEIGHT/2 + 100))
        WIN.blit(text, centerRect)
        WIN.blit(subtext, subRect)
        # for btn in btns:
        #     btn.draw(WIN)
        pygame.display.update()



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     pos = pygame.mouse.get_pos()
            #     for btn in btns:
            #         if btn.click(pos):
            #             MODE = btn.text
            #             print(MODE)
            #             run = False
            #             break
            if event.type == pygame.KEYDOWN:
                run = False
    pygame.time.wait(2500)
    main()

while True:
    menu_screen()



