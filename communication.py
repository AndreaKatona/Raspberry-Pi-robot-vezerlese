import socket
import pickle

class Communication:
    """
    A Communication osztály a szervehez való kapcsolódást, 
    adatküldést és lecsatlakozást kezeli.
    """

    def __init__(self):
        """
        Az osztály adattagjainak az inicializálása a kapcsolat
        létrehozásához szükséges atribútumokkal.

        Létrehozott attribútumok:
        - HOST: Szerver IP címe
        - PORT: Csatlakozási port száma
        - client_socket: Kliens socket, kezdetben nincs.
        """
        self.HOST = '192.168.1.222'
        #self.HOST = '192.168.0.101'
        self.PORT = 5000
        self.client_socket = None

    def start_connection(self):
        """
        A szerverrel való kommunikációs socket 
        létrehozása és csatlakozása.
        """
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.HOST, self.PORT))
            print('Kapcsolat létrehozva')
            return True
        except Exception :
            print('Hiba a csatlakozás során, kérem próbálja újra')
            return False
            
        
    def send(self, msg):
        """
        Az üzenet elküldése listaként a szervernek.

        Paraméter:
            msg: Az üzenet amit szeretnénk küldeni lista formában.
        """
        
        serialized_list = pickle.dumps(msg)
        self.client_socket.sendall(serialized_list)
 
    def close_connection(self):
        """
        A szerverrel való kapcsolatnak a lezárása.
        """
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
            print('Kapcsolat lezárva')
