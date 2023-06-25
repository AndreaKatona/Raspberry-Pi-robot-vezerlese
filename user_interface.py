import PySimpleGUI as sg

class Interface:
     """
     A felhasználói felülethez tartozó komponenseknek az osztálya,
     valamint a felhasználói felületen történő eseményeknek a kezelésére
     szolgál.
     """

     def __init__(self,speech_recognizer,client) :
        """
        Az osztály konstruktora.

        Paraméterek:
            speech_recognizer: beszédfelismerő (SpeechRecognition) objektum
            client: kommunikációs (Communication) objetum

        Létrehozott attribútumok:
        - speech_recognizer: beszédfelismerő objektum
        - client: kommunikációs objektum
        - layout: a felhasználói felületen az elemek elrendezése
        - window: a felhasználói felület ablaka

        """

        self.speech_recognizer = speech_recognizer
        self.client = client
        sg.theme('NeutralBlue')

        self.layout =[[sg.Text('Beszélt szöveg:')],
                    [sg.Output(size=(60, 10))],
                    [sg.Button('Kapcsolat létrehozása',key='CON-START'),sg.Button('Kapcsolat leállítás',key='CON-STOP',disabled=True)],
                    [sg.Button('Felvétel indítása', key='START',disabled=True), sg.Button('Felvétel leállítása', key='STOP', disabled=True), 
                     sg.Button('Kilépés', key = 'EXIT')]]
        
        self.window = sg.Window('Beszédfelismerő', self.layout)

     def run(self):
        """
        A felhasználói felület futtatása.
        Amig a felület ablaka nincs lezárva figyeli az eseményeket és kezeli a gombnyomásokat.

        Események:
        - WINDOW_CLOSED: A felhasználó lezárja az ablakot, a kommunikáció lezárúl.
        - EXIT: A felhasználó a 'Kilépés' gombra kattintott, a kommunikásió lezárúl és kilép.
        - CON-START: A felhasználó a 'Kapcsolat létrehozása' gombra kattintott és elindítja a kommunikációt.
        - CON-STOP: A felhasználó a 'Kapcsolat leállítása' gombra kattintott és leállítja a kommunikációt.
        - START: A felhasználó a 'Felvétel indítása' gombra kattintott és elindul a beszédfelismerés.
        - STOP: A felhasználó a 'Felvétel leállítása' gombra kattintott és leállítja a beszédfelismerést.

        """
        while True:
            event, _ = self.window.read(timeout=200)

            if event == sg.WINDOW_CLOSED:
                self.client.close_connection()
                break
         
            if event == 'EXIT':
                self.client.close_connection()
                break
            
            if event == 'CON-START':
                if self.client.start_connection():
                    self.window.Element('CON-START').Update(disabled=True)
                    self.window.Element('CON-STOP').Update(disabled=False)
                    self.window.Element('START').Update(disabled=False)

            if event == 'CON-STOP':
                self.client.close_connection()
                self.window.Element('CON-START').Update(disabled=False)
                self.window.Element('CON-STOP').Update(disabled=True)
                self.window.Element('START').Update(disabled=True)
                self.window.Element('STOP').Update(disabled=True)
                            

            if event == 'START':
                self.speech_recognizer.start()
                self.window.Element('CON-STOP').Update(disabled = True)
                self.window.Element('START').Update(disabled=True)
                self.window.Element('STOP').Update(disabled=False)

            if event == 'STOP':
                self.window.Element('CON-STOP').Update(disabled = False)
                self.speech_recognizer.stop()
                self.window.Element('START').Update(disabled=False)
                self.window.Element('STOP').Update(disabled=True)

            if self.speech_recognizer.data_available.isSet():
                 command=self.speech_recognizer.getLatestCommand()
                 if command:
                    self.client.send(command)
            
            

        self.window.close()



