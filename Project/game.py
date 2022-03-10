 ## Melody Simon-says prototype ##
import os
import random
from pydub import AudioSegment
from pydub.playback import play
import comm
import pygame

## UI Initializing
pygame.font.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PitchPerfect.io")

BLACK = (0,0,0)
WHITE = (255, 255, 255)

FONT = pygame.font.SysFont('comicsansms', 64)
SUBFONT = pygame.font.SysFont('comicsansms', 48)
startText = FONT.render('PitchPerfect.io', False, WHITE)
startText2 = SUBFONT.render('Press Enter to continue', False, WHITE)
centerRect = startText.get_rect(center = (WIDTH/2, HEIGHT/2))
subRect = startText2.get_rect(center = (WIDTH/2, HEIGHT/2 + 100))

FPS = 60

def draw_window(phase):
    WIN.fill(BLACK)
    if phase == 1:
        WIN.blit(startText, centerRect)
        WIN.blit(startText2, subRect)
    
    if phase == 2:
        WIN.blit(FONT.render('Round ' + str(ROUND), False, WHITE), centerRect)

    pygame.display.update()

## MQTT initialization

client = comm.init()

## Game

ROUND = 1
on = True
melody = []
sounds = ['Notes/C3.wav', 'Notes/C#3.wav', 'Notes/D3.wav', 'Notes/D#3.wav',
        'Notes/E3.wav', 'Notes/F3.wav', 'Notes/F#3.wav', 'Notes/G3.wav',
        'Notes/G#3.wav', 'Notes/A3.wav', 'Notes/A#3.wav', 'Notes/B3.wav',
        'Notes/C4.wav', 'Notes/C#4.wav', 'Notes/D4.wav', 'Notes/D#4.wav',
        'Notes/E4.wav', 'Notes/F4.wav', 'Notes/F#4.wav', 'Notes/G4.wav',
        'Notes/G#4.wav', 'Notes/A4.wav', 'Notes/A#4.wav', 'Notes/B4.wav']
seed = 0
PHASE = 1

def main():
    ROUND = 1
    on = True
    melody = []
    sounds = ['Notes/C3.wav', 'Notes/C#3.wav', 'Notes/D3.wav', 'Notes/D#3.wav',
            'Notes/E3.wav', 'Notes/F3.wav', 'Notes/F#3.wav', 'Notes/G3.wav',
            'Notes/G#3.wav', 'Notes/A3.wav', 'Notes/A#3.wav', 'Notes/B3.wav',
            'Notes/C4.wav', 'Notes/C#4.wav', 'Notes/D4.wav', 'Notes/D#4.wav',
            'Notes/E4.wav', 'Notes/F4.wav', 'Notes/F#4.wav', 'Notes/G4.wav',
            'Notes/G#4.wav', 'Notes/A4.wav', 'Notes/A#4.wav', 'Notes/B4.wav']
    seed = 0
    PHASE = 1
        


    pygame.init()
    clock = pygame.time.Clock()
    while on:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
                break

        draw_window(PHASE)

        if PHASE == 1:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    PHASE += 1
                    continue

        if PHASE != 1:
            random.seed(seed)
            melodySize = ROUND+1
            for i in range(melodySize):
                melody.append(random.randint(0, len(sounds)-1))

            relation = [0]*(melodySize-1)
            for i in range(melodySize-1):
                relation[i] = melody[i+1] - melody[i]

            sol = ''
            for i in range(len(relation)):
                if relation[i] < 0:
                    sol += 'v'
                elif relation[i] == 0:
                    sol += '>'
                elif relation[i] > 0:
                    sol += '^'

        ## Publish the melody and correct answer
        #    client.publish('ece180d/test',str(melody), qos=1)
        #    client.publish('ece180d/test', sol, qos=1)

        ## Here's how the keyboard input is processed

            for i in range(melodySize):
                sound = AudioSegment.from_wav(sounds[melody[i]])
                play(sound)

        ## Answer's made on client side instead of this:

            ans = input('Pitch movement (^/v/>): ')
            
        ## How to store subscribed message?
        #    ans = client.loop_start()


            if ans == sol:
                print('Correct!')
                ROUND += 1
            else:
                print('Incorrect, the correct answer is : ' + sol)
                again = input('Play Again? (Y/N)')
                if again == 'N':
                    on = False
                ROUND = 1
            seed += 1
    pygame.quit()

if __name__ == "__main__":
    main()
