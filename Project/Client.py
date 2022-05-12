import pygame
from network import Network
import random
import medium_mode_DandF as speech
import camera
import IMU_main
import camera
import game
from tutorial import tutorial
from pydub import AudioSegment
from pydub.playback import play
# from board import drawBoard


## Pygame Inits
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
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")
MODES = ['Keyboard', 'Camera', 'Speech']
SOUNDS = ['Notes/A3.wav', 'Notes/B3.wav', 'Notes/C4.wav', 'Notes/D4.wav', 'Notes/E4.wav', 'Notes/F4.wav', 'Notes/G4.wav']
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

red=pygame.image.load("Archive/red.jpg")
yellow=pygame.image.load("Archive/yellow.jpg")
blue=pygame.image.load("Archive/blue.jpg")
p1=pygame.image.load("Archive/p1.png")
p2=pygame.image.load("Archive/p2.png")
back=pygame.image.load("Archive/back.jpg")
D1=pygame.image.load("Archive/Dice1.jpg")
D2=pygame.image.load("Archive/Dice2.jpg")
D3=pygame.image.load("Archive/Dice3.jpg")
D4=pygame.image.load("Archive/Dice4.jpg")
D5=pygame.image.load("Archive/Dice5.jpg")
D6=pygame.image.load("Archive/Dice6.jpg")

#adjust images to correct size
red=pygame.transform.scale(red, (SQUARE_EDGE, SQUARE_EDGE))
yellow=pygame.transform.scale(yellow, (SQUARE_EDGE, SQUARE_EDGE))
blue=pygame.transform.scale(blue, (SQUARE_EDGE, SQUARE_EDGE))
p1=pygame.transform.scale(p1, (SQUARE_EDGE//2, SQUARE_EDGE//2))
p2=pygame.transform.scale(p2, (SQUARE_EDGE//2, SQUARE_EDGE//2))
back=pygame.transform.scale(back, (WIDTH, HEIGHT))
D1=pygame.transform.scale(D1, (DIE_LENGTH,DIE_LENGTH))
D2=pygame.transform.scale(D2, (DIE_LENGTH,DIE_LENGTH))
D3=pygame.transform.scale(D3, (DIE_LENGTH,DIE_LENGTH))
D4=pygame.transform.scale(D4, (DIE_LENGTH,DIE_LENGTH))
D5=pygame.transform.scale(D5, (DIE_LENGTH,DIE_LENGTH))
D6=pygame.transform.scale(D6, (DIE_LENGTH,DIE_LENGTH))

DICE = {1:D1, 2:D2, 3:D3, 4:D4, 5:D5, 6:D6}
ROLLED = False ## Client variable to make sure dice roll is only sent once

def playGame(game, WIN):
        if game.currMode == 'Keyboard':
            game.currAnswer = input('^, >, v')
        elif game.currMode == 'IMU':
            game.currAnswer = IMU_main.main()
        elif game.currMode == 'Camera':
            game.currAnswer = camera.camera(game.currRoll, 7)
        elif game.currMode == 'Speech':
            game.currAnswer = speech.speechRecognition(WIN)
        return(game.currAnswer)

def drawWindow(WIN, game):

    WIN.fill((0,0,0))
    font = pygame.font.SysFont('comicsansms', 64)
    text = font.render("Waiting for Player...", True, (255,255,255))
    WIN.blit(text, text.get_rect(center = (WIDTH/2, HEIGHT/2)))
    pygame.display.update()


def drawBoard(WIN, game, turn = False):
    WIN.fill((0,0,0))
    WIN.blit(back,(0,0))
    font = pygame.font.SysFont('comicsansms', 64)

    drawBoardGrid(game)
    if turn:
        txt = font.render('Roll the die!', True, (255,255,255))     
    else:
        txt = font.render("Other player's turn", True, (255,255,255))
    txtRect = txt.get_rect(center = (WIDTH/2, TEXT_HEIGHT))
    WIN.blit(txt, txtRect)
    pygame.display.update()

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



def drawDiceRoll(WIN, roll):
    diceRect = D1.get_rect(center = (WIDTH/2, TEXT_HEIGHT))
    for i in range(50):
        pygame.time.delay(60)
        WIN.fill((0,0,0))
        WIN.blit(back, (0,0))
        num = random.randint(1,6)
        WIN.blit(DICE[num], diceRect)
        pygame.display.update()
    
    
    # # font = pygame.font.SysFont('comicsansms', 64)
    # # txt = font.render('Rolled a ' + str(game.currRoll), True, (255,255,255))
    
    WIN.fill((0,0,0))
    WIN.blit(back, (0,0))
    WIN.blit(DICE[roll], diceRect)
    pygame.display.update()
    pygame.time.delay(3000)
    # ## TO DO: make animation for dice roll

def drawMove(WIN):
    WIN.fill((0,0,0))
    WIN.blit(back, (0,0))
    font = pygame.font.SysFont('comicsansms', 64)
    txt = font.render('Correct!' , True, (255,255,255))
    txtRect = txt.get_rect(center = (WIDTH/2, TEXT_HEIGHT))
    WIN.blit(txt, txtRect)
    pygame.display.update()
    pygame.time.delay(4000)
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
    WIN.blit(back, (0,0))
    font = pygame.font.SysFont('comicsansms', 64)
    txt = font.render("Player " + str(game.winner + 1) + " wins!" , True, (255,255,255))
    txtRect = txt.get_rect(center = (WIDTH/2, TEXT_HEIGHT))
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

    while run:
        clock.tick(FPS)
        try:
            game = n.send("get")
        except:
            menu_screen()


        if not game.connected():
            drawWindow(WIN, game)
        
        else:

            if game.phase == 'board':
                ROLLED = False
                if game.currPlayer == player:
                    drawBoard(WIN, game, True)
                    pygame.time.delay(3000)
                    #IMU_main.main()
                    n.send('board')
                else:
                    drawBoard(WIN, game)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                        
            
            elif game.phase == 'dice':
                if game.currPlayer == player:
                    if not ROLLED:
                        roll = random.randint(1, 6)
                        print(str(roll))
                        n.send(str(roll))
                        drawDiceRoll(WIN, roll)
                # else:
                #     if game.rolled:
                #         drawDiceRoll(WIN, game.currRoll)
                #     n.send('dice')
            
            elif game.phase == 'turn':
                if game.currPlayer == player:
                    if not game.went:
                        playSound(WIN, game)
                        ans = playGame(game, WIN)
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        WIN.fill((0,0,0))
        WIN.blit(back, (0,0))

        font = pygame.font.SysFont('comicsansms', 64)
        subfont = pygame.font.SysFont('comicsansms', 48)
        text = font.render('PitchPerfect.io', False, (255,255,255))
        subtext = subfont.render("Press 't' for tutorial, any other key to start", False, (255,255,255))
        centerRect = text.get_rect(center = (WIDTH/2, HEIGHT/2 - 175))
        subRect = subtext.get_rect(center = (WIDTH/2, HEIGHT/2 + 175))
        WIN.blit(text, centerRect)
        WIN.blit(subtext, subRect)
        pygame.display.update()



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    tutorial(WIN)
                else:
                    run = False
    pygame.time.wait(2500)
    main()
