import pygame
from network import Network
import time
import random


## Pygame Inits
pygame.font.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")
MODES = ['Keyboard', 'IMU', 'Camera', 'Speech']

def drawWindow(WIN, game):

    WIN.fill((0,0,0))

    font = pygame.font.SysFont('comicsansms', 64)
    text = font.render("Waiting for Player...", True, (255,255,255))
    WIN.blit(text, text.get_rect(center = (WIDTH/2, HEIGHT/2)))
    pygame.display.update()


def drawBoard(WIN, game, turn = False):
    WIN.fill((0,0,0))
    font = pygame.font.SysFont('comicsansms', 64)
    if turn:
        txt = font.render('Click to roll', True, (255,255,255))     
    else:
        txt = font.render('Player ' + str(game.currPlayer + 1) + ': ' + str(game.spots[game.currPlayer]), True, (255,255,255))
    txtRect = txt.get_rect(center = (WIDTH/2, HEIGHT/2))
    WIN.blit(txt, txtRect)
    pygame.display.update()
    # for i in range(game.boardH):
    #     for j in range(game.boadW):

    ## TO DO: draw game board and msg: "Click to roll dice"


def drawDiceRoll(WIN, game):
    WIN.fill((0,0,0))
    font = pygame.font.SysFont('comicsansms', 64)
    txt = font.render('Rolled a ' + str(game.currRoll), True, (255,255,255))
    txtRect = txt.get_rect(center = (WIDTH/2, HEIGHT/2))
    WIN.blit(txt, txtRect)
    pygame.display.update()
    pygame.time.delay(3000)
    ## TO DO: make animation for dice roll

def drawMove(WIN):
    WIN.fill((0,0,0))
    font = pygame.font.SysFont('comicsansms', 64)
    txt = font.render('Move animation' , True, (255,255,255))
    txtRect = txt.get_rect(center = (WIDTH/2, HEIGHT/2))
    WIN.blit(txt, txtRect)
    pygame.display.update()
    pygame.time.delay(3000)
    ## TO DO: make animation for player movement on board

def drawTurn(WIN):
    WIN.fill((0,0,0))
    font = pygame.font.SysFont('comicsansms', 64)
    txt = font.render("Other player's move" , True, (255,255,255))
    txtRect = txt.get_rect(center = (WIDTH/2, HEIGHT/2))
    WIN.blit(txt, txtRect)
    pygame.display.update()

def drawEnd(WIN, game):
    WIN.fill((0,0,0))
    font = pygame.font.SysFont('comicsansms', 64)
    txt = font.render("Player " + str(game.winner + 1) + " wins!" , True, (255,255,255))
    txtRect = txt.get_rect(center = (WIDTH/2, HEIGHT/2))
    WIN.blit(txt, txtRect)
    pygame.display.update()


def main():
    n = Network()
    player = int(n.getP())
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            pygame.quit()
            break


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
                        game.playSound()
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

