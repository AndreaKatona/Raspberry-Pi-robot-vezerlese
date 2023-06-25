import speech_recognition as sr
import threading

class SpeechRecognizer:
    """
    A SpeechRecognizer osztály kezeli a hang rögzítését és a felismert adatot, valamint a felismerés elkezdését és leállítását.
    """

    def __init__(self) :
        """
        Az osztály konstruktora.

        Létrehozott attribútumok:
        - r: A speech_recognition csomag objektuma, a felismerés folyamatára szolgál.
        - stop_listening: Egy Bool típusú adat, ami a felismerés leállítását jelzi, kezdetben False.
        - stop_event: Event, ami a felismerés folyamatának futását jelzi. 
        - data_available: Event, amely jelzi, hogy a felismerésnek van adata.
        - thread: Egy új szál amiben a recognitionProcess fut.
        - data: A felismerésből kiszűrt adat, kezdetben üres.
        - keywords: Lista a kulcsszavakkal.
        """

        self.r = sr.Recognizer()
        self.stop_event = threading.Event()
        self.data_available = threading.Event()
        self.thread = threading.Thread(target = self.recognitionProcess)
        self.data = ""
        self.keywords = ["előre", "hátra", "jobbra", "balra"]

    def recognitionProcess(self):

        with sr.Microphone() as source:
         while not self.stop_event.is_set():
             audio = None
             print("\nKérlek beszélj, hallgatlak.\n")
             try:
                 audio = self.r.listen(source, timeout=10, phrase_time_limit=8)
 
             except sr.WaitTimeoutError:
                 print("Nem volt érzékelve beszéd, kezd újra!")
                 continue  

             if audio is not None and not self.stop_event.is_set():
                 try:
                     print("...")
                     text = self.r.recognize_google(audio, language="hu-HU")
                     if text:
                         self.data = text.lower()
                         self.data_available.set()
                         print("Felismert szöveg: " + self.data)

                 except sr.UnknownValueError:
                     print("Nem sikerült felismerni a beszédet.")
                 except sr.RequestError as e:
                     print("Hiba történt a Google Speech API hívása közben: {0}".format(e))


    def start(self):
        """
        Beszédfelismerés elindítása.
        Ha a beszédfelismerés nem fut, akkor elindítja a folyamatot.
        """
        if not self.thread.is_alive():

            print("Beszédfelismerés elinditása...\n")
            self.thread = threading.Thread(target = self.recognitionProcess)
 
            self.stop_event.clear()
            self.thread.start()

    def stop(self):
        """
        A beszédfelismerés leállítására szolgál.
        Ha a beszédfelismerés fut, akkor leállítja a folyamatot.
        """
        if self.thread.is_alive():
            print("Beszédfelismerés leállítása...")
            self.stop_event.set()
            self.thread.join()
        
    def getLatestCommand(self):
        """
        A legutolsó parancs lekérése és feldolgozása.
        Várakozik, ameddig elérhetővé vális a felimerés eredménye.
        A felismert szöveget szavakra bontja, majd kiszűri a kulcsszavakat és listába tárolja.
        A feldolgozás után törli az event-et

        Visszatérít: 
        - keywords_found: lista a kulcsszavakkal
        """
        self.data_available.wait()
        words = self.data.split()
        keywords_found = [word for word in words if word in self.keywords]
        self.data_available.clear()
        
        return keywords_found
