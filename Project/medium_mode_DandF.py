import speech_recognition as sr
import pygame

letters = {'alpha': 'A', 'bravo': 'B', 'charlie': 'C', 'delta': 'D', 'echo': 'E', 'foxtrot': 'F', 'golf': 'G'}

def speechRecognition(WIN):
    WIN.fill((0,0,0))
    font = pygame.font.SysFont('comicsansms', 20)
    text = font.render('Calibrating...', True, (255,255,255))
    WIN.blit(text, text.get_rect(center = (WIDTH/2, HEIGHT/2)))
    pygame.display.update()
    pygame.time.delay(2000)

    r = sr.Recognizer()
    m = sr.Microphone()
    
    run = True
    answer = '' #answer in number form
    with m as source: r.adjust_for_ambient_noise(source)
    WIN.fill((0,0,0))
    text = font.render("Ready!", True, (255,255,255))
    WIN.blit(text, text.get_rect(center = (WIDTH/2, HEIGHT/2)))
    pygame.display.update()

    while run:
        WIN.fill((0,0,0))
        with m as source: audio = r.listen(source)
        try:
            # recognize speech using Google Speech Recognition
            i = r.recognize_google(audio)
            # value is the variable here
            
            #speech_input_list = value.split()   #separates speech input into a list of words
            
            if(i == 'alpha' or i == 'Alpha'):
                answer = answer + '0'
            elif(i == 'bravo' or i == 'Bravo'):
                answer = answer + '1'
            elif(i == 'charlie' or i == 'Charlie'):
                answer = answer + '2'
            elif(i == 'delta' or i == 'Delta'):
                answer = answer + '3'
            elif(i == 'echo' or i == 'Echo'):
                answer = answer + '4'
            elif(i == 'foxtrot' or i == 'Foxtrot'):
                answer = answer + '5'
            elif(i == 'golf' or i == 'Golf'):
                answer = answer + '6'
                
                
            #window drawing

            text = font.render(letters[i.lower()], True, (255,255,255))
            WIN.blit(text, text.get_rect(center = (WIDTH/2, HEIGHT/2)))
            pygame.display.update()
        
            
    #speech Recognition errors
        except sr.UnknownValueError:
            run = False
        except sr.RequestError as e:
            return "Uh oh! Couldn't request results from Google Speech Recognition service; {0}"
    return answer
