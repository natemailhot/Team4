import speech_recognition as sr


def speechRecognition():

    r = sr.Recognizer()
    m = sr.Microphone()

    with m as source: r.adjust_for_ambient_noise(source)
    with m as source: audio = r.listen(source)
    try:
        # recognize speech using Google Speech Recognition
        value = r.recognize_google(audio)
        # value is the variable here
        
        #checks for 'D' and 'F'   and   Returns 0 or 1  or "Wrong Answer"
        if value == 'delta foxtrot' or value == 'Delta Foxtrot' or value == 'delta Foxtrot' or value =='Delta foxtrot':
            return [0, 1]
        elif value == 'foxtrot delta' or value == 'Foxtrot Delta' or value == 'Foxtrot delta' or value == 'foxtrot Delta':
            return [1, 0]
        elif value == 'delta delta' or value == 'Delta Delta' or value == 'Delta delta' or value == 'delta Delta':
            return [0, 0]
        elif value == 'foxtrot foxtrot' or value == 'Foxtrot Foxtrot' or value == 'Foxtrot foxtrot' or value == 'foxtrot Foxtrot':
            return [1, 1]
        else:
            print("Wrong Answer")
            
    #speech Recognition errors
    except sr.UnknownValueError:
        print("Oops! Didn't catch that")
    except sr.RequestError as e:
        print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
