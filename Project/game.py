 ## Melody Simon-says prototype ##
import os
import random
from pydub import AudioSegment
from pydub.playback import play
#import comm
#import UI


class Game:
    def __init__(self, id):
        self.modes = ['Keyboard', 'Keyboard']
        self.went = [False, False]
        self.ready = False
        self.id = id
        self.answers = ['a', 'a']
        self.keySol = ''
        self.sounds = ['Notes/D3.wav', 'Notes/F3.wav']
        self.melody = []
        self.melodySize = 2
        self.p1 = False
        self.p2 = False
    

    def playSound(self):
        for i in range(self.melodySize):
            sound = AudioSegment.from_wav(self.sounds[self.melody[i]])
            play(sound)

    def makeMelody(self):
        for i in range(self.melodySize):
            self.melody.append(random.randint(0, len(self.sounds)-1))
        
        relation = [0]*(self.melodySize-1)
        for i in range(self.melodySize-1):
            relation[i] = self.melody[i+1] - self.melody[i]

        for i in range(len(relation)):
            if relation[i] < 0:
                self.keySol += 'v'
            elif relation[i] == 0:
                self.keySol += '>'
            elif relation[i] > 0:
                self.keySol += '^'

    def play(self, player):
        self.makeMelody()
        self.playSound()
#        print(player)

        if self.modes[player] == "Keyboard":
            self.answers[player] = input('^, >, v')
            if self.answers[player] == self.keySol:
                if player == 0:
                    self.p1 = True
                else:
                    self.p2 = True
            self.went[player] = True

        if self.modes[player] == "IMU":
            self.answers[player] = IMU_code.run(...)
            if self.answers[player] == self.imuSol:
                if player == 0:
                    self.p1 = True
                else:
                    self.p2 = True
            self.went[player] = True
    
    def getWent(self, player):
        return(self.went[player])

    def getAns(self, player):
        return(self.answers[player])


    def connected(self):
        return self.ready

    def bothWent(self):
        return(self.went[0] and self.went[1])
    
    def resetWent(self):
        self.went = [False, False]
        self.p1 = False
        self.p2 = False
        
















## MQTT initialization

#client = comm.init()

## Game

# ROUND = 1
# on = True
# melody = []
# sounds = ['Notes/C3.wav', 'Notes/C#3.wav', 'Notes/D3.wav', 'Notes/D#3.wav',
#         'Notes/E3.wav', 'Notes/F3.wav', 'Notes/F#3.wav', 'Notes/G3.wav',
#         'Notes/G#3.wav', 'Notes/A3.wav', 'Notes/A#3.wav', 'Notes/B3.wav',
#         'Notes/C4.wav', 'Notes/C#4.wav', 'Notes/D4.wav', 'Notes/D#4.wav',
#         'Notes/E4.wav', 'Notes/F4.wav', 'Notes/F#4.wav', 'Notes/G4.wav',
#         'Notes/G#4.wav', 'Notes/A4.wav', 'Notes/A#4.wav', 'Notes/B4.wav']
# seed = 0
# PHASE = 1

# def main():
#     ROUND = 1
#     on = True
#     melody = []
#     sounds = ['Notes/C3.wav', 'Notes/C#3.wav', 'Notes/D3.wav', 'Notes/D#3.wav',
#             'Notes/E3.wav', 'Notes/F3.wav', 'Notes/F#3.wav', 'Notes/G3.wav',
#             'Notes/G#3.wav', 'Notes/A3.wav', 'Notes/A#3.wav', 'Notes/B3.wav',
#             'Notes/C4.wav', 'Notes/C#4.wav', 'Notes/D4.wav', 'Notes/D#4.wav',
#             'Notes/E4.wav', 'Notes/F4.wav', 'Notes/F#4.wav', 'Notes/G4.wav',
#             'Notes/G#4.wav', 'Notes/A4.wav', 'Notes/A#4.wav', 'Notes/B4.wav']
#     seed = 0
#     PHASE = 1
        


#     pygame.init()
#     clock = pygame.time.Clock()
#     while on:
#         clock.tick(FPS)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 on = False
#                 break

#         UI.draw_window(PHASE)

#         if PHASE == 'START':
#             for event in pygame.event.get():
#                 if event.type == pygame.MOUSEBUTTONDOWN:
#                     PHASE = 'PLAY'
#                     continue

#         if PHASE == 'PLAY':
#             random.seed(seed)
#             melodySize = ROUND+1
#             for i in range(melodySize):
#                 melody.append(random.randint(0, len(sounds)-1))

#             relation = [0]*(melodySize-1)
#             for i in range(melodySize-1):
#                 relation[i] = melody[i+1] - melody[i]

#             sol = ''
#             for i in range(len(relation)):
#                 if relation[i] < 0:
#                     sol += 'v'
#                 elif relation[i] == 0:
#                     sol += '>'
#                 elif relation[i] > 0:
#                     sol += '^'

#         ## Publish the melody and correct answer
#         #    client.publish('ece180d/test',str(melody), qos=1)
#         #    client.publish('ece180d/test', sol, qos=1)

#         ## Here's how the keyboard input is processed

#             for i in range(melodySize):
#                 sound = AudioSegment.from_wav(sounds[melody[i]])
#                 play(sound)

#         ## Answer's made on client side instead of this:

#             ans = input('Pitch movement (^/v/>): ')
            
#         ## How to store subscribed message?
#         #    ans = client.loop_start()

#             if ans == sol:
#                 print('Correct!')
#                 ROUND += 1
#             else:
#                 print('Incorrect, the correct answer is : ' + sol)
#                 again = input('Play Again? (Y/N)')
#                 if again == 'N':
#                     on = False
#                 ROUND = 1
#             seed += 1
#     pygame.quit()

# if __name__ == "__main__":
#     main()
