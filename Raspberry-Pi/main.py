from control import Movement
from connection import Server

if __name__ == "__main__":
    
    """
    Ez a főprogram belépési pontja.
    Inicializálja a robot mozgásáért felelős objektumot és elindítja a szervert.
    """
    robot = Movement()
    
    server = Server(robot)
    
    server.start()
    