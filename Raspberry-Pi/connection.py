import socket
import pickle
import threading


class Server:
    """
    Ez az osztály felelős a szerver elindításáért, a kapcsolatok, valamint
    az üzenetek fogadásáért.
    """
    def __init__(self,robot):
        """
        Az osztály konstruktora.
        
        Paraméter:
            robot: Robot osztály példánya.
            
        Létrehozott attribútumok:
        -robot: Robot osztály példánya
        -HOST: a szerver IP címe
        -PORT: a kapcsolódási port száma
        -server_socket: socket objektum
        -connection: lista a kapcsolatokról, kezdetben üres
        -data_available: Event, ami az adat elérhetőségét jelzi
        -data: mindig a legutóbbi üzenetet tartalmazza
        -lock: zár, amit a kritikus szekcióban használunk
        """
       
        self.robot = robot
        self.HOST =  '192.168.1.222'
        """
        self.HOST = '192.168.0.101'
        """
        self.PORT = 5000
        
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.server_socket.bind((self.HOST,self.PORT))
        self.connection = []
        self.connected_client=False
        self.data_available = threading.Event()
        self.data = ''
        self.lock = threading.Lock()
        
    
        
    def start(self):
        """
        Ebben a metódusban egy új szálban futassuk a kapcsolodásért felelős metódus, valamint
        a utasítást továbbítjuk a végrehajtásra.
        """
        print('Szerver elindítva')
        listener_thread = threading.Thread(target=self.listen)
        listener_thread.start()
        
        try:
        
            while True:
                command = self.getMessage()
                print(command)
                self.robot.execute_command(command)
                
        except KeyboardInterrupt:
            
            self.robot.cleanup()
            self.server_socket.close()
        

    def listen(self):
        """
        Ez a metódus figyeli a kliensek kapcsolódását és elindítja a folyamatot, amiben a kliensek kapcsolatának
        állapotát vizsgálja.Továbbá menti a klienseket és listába tárolja.
    
        """
        self.server_socket.listen(1)
        print('Várakozás a csatlakozásra...')
        while True:
           if not self.connected_client:
            connection, client_address = self.server_socket.accept()
            print('Csatlakozott kliens:', client_address)
            
            self.connected_client=True
            connection_thread = threading.Thread(target = self.handle_connection,args=(connection,))
            connection_thread.start()
            
            with self.lock:
                self.connection.append(connection)
                
    def handle_connection(self,connection):
        """
        A csatlakoyott kliensek állapotát figyeli, és adatokat fogad.
        
        Paraméter:
            connection: kapcsolat objektum
        """
        with connection:
            while True:
                    
                data = connection.recv(1024)
                if data:
                    
                    self.data = pickle.loads(data)
                    self.data_available.set()
                        
                else:
                        
                    break

                
            with self.lock:
                self.connection.remove(connection)
                self.connected_client=False
                print('Kapcsolat lezárva')

    def getMessage(self):
        """
        Ez a metódus várja, hogy az üzenet elérhető legyen és kimenti az adatot, és visszatéríti.
        
        Visszatérít:
        -data: üzenet a klienstől, tartalmazza az utas0tásokat
            
        """
        self.data_available.wait()
        data = self.data
        self.data_available.clear()
        
        return data
    
    