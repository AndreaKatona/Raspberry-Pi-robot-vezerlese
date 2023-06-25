from user_interface import Interface
from speech import SpeechRecognizer 
from communication import Communication

if __name__ == '__main__':
     """
     Ez a főprogram belépési pontja.
     Inicializálja a felhasználói felületet, beszédfelismerőt és kommunikációt,
     majd elindítja a felhasználói felületet.
     """
     speech_recognizer = SpeechRecognizer()
     client = Communication()
     interface = Interface(speech_recognizer,client)

     interface.run()

