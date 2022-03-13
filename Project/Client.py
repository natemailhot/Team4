#import UI
#import paho.mqtt.client as mqtt
import pygame
from network import Network

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


def draw_window(WIN, game):
    WIN.fill((0,0,0))

    if not game.connected():
        font = pygame.font.SysFont('comicsansms', 64)
        text = font.render("Waiting for Player...", (255,255,255), True)
        WIN.blit(text, text.get_rect(center = (WIDTH/2, HEIGHT/2)))
    else:
        font = pygame.font.SysFont('comicsansms', 64)
        text = font.render('Round 1', False, (255,255,255))
        centerRect = text.get_rect(center = (WIDTH/2, HEIGHT/2))
        WIN.blit(text, centerRect)
    pygame.display.update()

def main():
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

        ## If both player went, display each player's correctness
        if game.bothWent():
            WIN.fill((0,0,0))
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont('comicsansms', 64)

            if game.p1():
                p1Text = font.render('Player 1 is Correct!', False, (255,255,255))
            else:
                p1Text = font.render('Player 1 is Incorrect.', False, (255,255,255))
            if game.p2():
                p2Text = font.render('Player 2 is Correct!', False, (255,255,255))
            else:
                p2Text = font.render('Player 2 is Incorrect.', False, (255,255,255))

            p1Rect = p1Text.get_rect(center = (WIDTH/2, HEIGHT/2 - 50))
            p2Rect = p2Text.get_rect(center = (WIDTH/2, HEIGHT/2 + 50))
            WIN.blit(p1Text, p1Rect)
            WIN.blit(p2Text, p2Rect)
            pygame.display.update()
            pygame.time.delay(2000)



        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        draw_window(WIN, game)
        if game.connected():
            if not game.went[player]:
                game.play(player)

        
        

        
        



def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        WIN.fill((0,0,0))


        font = pygame.font.SysFont('comicsansms', 64)
        subfont = pygame.font.SysFont('comicsansms', 48)
        text = font.render('PitchPerfect.io', False, (255,255,255))
        subtext = subfont.render('Click to Start!', False, (255,255,255))
        centerRect = text.get_rect(center = (WIDTH/2, HEIGHT/2))
        subRect = subtext.get_rect(center = (WIDTH/2, HEIGHT/2 + 100))
        WIN.blit(text, centerRect)
        WIN.blit(subtext, subRect)
        pygame.display.update()



        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
    main()

while True:
    menu_screen()

