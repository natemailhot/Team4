#import UI
#import paho.mqtt.client as mqtt
import pygame
from network import Network
import time

## MQTT Functions
# def on_connect(client, userdata, flags, rc):
#     print("Connection returned result: "+str(rc))

# def on_disconnect(client, userdata, rc):
#     if rc != 0:
#         print("Unexpected Disconnect")
#     else:
#         print("Expected Disconnect")

# def on_message(client, userdata, message):
#     print('Received message: "' + str(message.payload) + '" on topic "' +
#         message.topic + '" with QoS ' + str(message.qos))



## Pygame Inits
pygame.font.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")
MODES = {pygame.K_k: 'Keyboard', pygame.K_i: 'IMU', pygame.K_c: "Camera", pygame.K_s: "Speech"}


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

btns = [Button("Keyboard", 50, 350, (0,0,0)), Button("IMU", 300, 350, (255,0,0)), Button("Speech", 550, 350, (0,255,0)), Button("Camera", 800, 350, (255,255,0))]

def draw_window(WIN, game, round = 0):

    WIN.fill((0,0,0))

    if not game.connected():
        font = pygame.font.SysFont('comicsansms', 64)
        text = font.render("Waiting for Player...", True, (255,255,255))
        WIN.blit(text, text.get_rect(center = (WIDTH/2, HEIGHT/2)))
    else:
        font = pygame.font.SysFont('comicsansms', 64)
        text = font.render('Round ' + str(game.round), False, (255,255,255))
        centerRect = text.get_rect(center = (WIDTH/2, HEIGHT/2))
        WIN.blit(text, centerRect)
    pygame.display.update()



    

def main(MODE):
    n = Network()
    player = int(n.getP())
    print("You are player", player)
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        
        ## If both player went, next round or reset
        if game.bothWent():
            WIN.fill((0,0,0))
            pygame.time.delay(500)

            font = pygame.font.SysFont('comicsansms', 64)

            if game.getP1() and game.getP2():
                txt = font.render('Both players correct!', True, (255,255,255))
                txtRect = txt.get_rect(center = (WIDTH/2, HEIGHT/2))
                WIN.blit(txt, txtRect)
                pygame.display.update()
                pygame.time.delay(5000)
                try:
                    game = n.send("next")
                except:
                    run = False
                    print("Couldn't make new round")
                    break
            else:
                try:
                    if game.getP1():
                        winner = '1'
                    else:
                        winner = '2'

                    txt = font.render('Player ' + winner + ' wins!', True, (255,255,255))
                    txtRect = txt.get_rect(center = (WIDTH/2, HEIGHT/2))
                    WIN.blit(txt, txtRect)
                    pygame.display.update()
                    pygame.time.delay(5000)
                    game = n.send("reset")
                except:
                    run = False
                    print("Couldn't get game")
                    break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        
        if game.connected():
            if game.getWent(player):
                WIN.fill((0,0,0))
                font = pygame.font.SysFont('comicsansms', 64)
                text = font.render("Waiting...", True, (255,255,255))
                WIN.blit(text, text.get_rect(center = (WIDTH/2, HEIGHT/2)))
                pygame.display.update()
            else:
                draw_window(WIN, game)
                game.playSound()
                ans = game.play(player, MODE)
                print(ans)
                n.send(MODE + ' ' + ans)        
        else:
            draw_window(WIN, game)

        


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        WIN.fill((0,0,0))


        font = pygame.font.SysFont('comicsansms', 64)
        subfont = pygame.font.SysFont('comicsansms', 40)
        text = font.render('PitchPerfect.io', False, (255,255,255))
        subtext = subfont.render("Mode: (K)eyboard, (I)MU, (C)amera, (S)peech", False, (255,255,255))
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
                MODE = MODES[event.key]
                print(MODE)
                run = False
    pygame.time.wait(2500)
    main(MODE)

while True:
    menu_screen()

