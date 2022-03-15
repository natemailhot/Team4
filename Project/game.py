 ## Melody Simon-says prototype ##
import os
import random
from pydub import AudioSegment
from pydub.playback import play

## Import these to test

#import IMU_main
#import camera
#import medium_mode_DandF as speech


class Game:
    def __init__(self, id):
        self.modes = ['Keyboard', 'Keyboard']
        self.went = [False, False]
        self.ready = False
        self.id = id
        self.answers = ['a', 'a']
        self.keySol = ''
        self.sounds = ['Notes/D3.wav', 'Notes/F3.wav']
        self.melody = [1, 1]
        self.melodySize = 2
        self.p1 = False
        self.p2 = False

        for i in range(self.melodySize):
            self.melody[i] = random.randint(0, len(self.sounds)-1)
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
    

    def playSound(self):
        for i in range(self.melodySize):
            sound = AudioSegment.from_wav(self.sounds[self.melody[i]])
            play(sound)

    # def makeMelody(self):
    #     for i in range(self.melodySize):
    #         self.melody.append(random.randint(0, len(self.sounds)-1))
        
    #     relation = [0]*(self.melodySize-1)
    #     for i in range(self.melodySize-1):
    #         relation[i] = self.melody[i+1] - self.melody[i]

    #     for i in range(len(relation)):
    #         if relation[i] < 0:
    #             self.keySol += 'v'
    #         elif relation[i] == 0:
    #             self.keySol += '>'
    #         elif relation[i] > 0:
    #             self.keySol += '^'

    def getP1(self):
        return(self.p1)

    def getP2(self):
        return(self.p2)
    
    def printMelody(self):
        print(self.melody)
        return


    def play(self, player, mode):

        print(mode)
        if mode == 'Keyboard':
            self.answers[player] = input('^, >, v')

        ## UNCOMMENT TO TEST

        # elif mode == 'IMU':
        #     self.answers[player] = IMU_code.main()
        # elif mode == 'Camera':
        #     self.answers[player] = camera.level_three()
        # elif mode == 'Speech':
        #     self.answers[player] = speech.TODO()

        return(self.answers[player])
            

    def check(self, player, ans):
        self.answers[player] = ans
        if self.modes[player] == "Keyboard" or self.modes[player] ==  "IMU": 
            if ans == self.keySol:
                if player == 0:
                    self.p1 = True
                else:
                    self.p2 = True
        if self.modes[player] == "Camera" or self.modes[player] == "Speech":
            if ans == self.melody:
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
