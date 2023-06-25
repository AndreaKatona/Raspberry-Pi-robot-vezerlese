import RPi.GPIO as GPIO
import time


class Movement:
    """
    A Movement osztály a robot irányítására szolgál.
    
    """
    
    def __init__(self):
        """
        Az osztály konstruktora.
        
        Létrehozott attribútumok:
        - dir_1: első iránybit meghatározása
        - dir_2: második iránybit meghatározása
        - pwm_pin_1: első PMW pin meghatározása, bal oldali motorhoz
        - pwm_pin_2: második PWM pin meghatározása, jobb oldali motorhoz
        - frequency: frekvencia meghatározása (Hz)
        """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        
        self.dir_1 = 10
        self.dir_2 = 8
        
        self.pwm_pin_1 = 12 #bal
        self.pwm_pin_2 = 32 #jobb
        
        self.speed = 0
        self.frequency = 1000
        
        self.setup()
        
    def setup(self):
        """
        Beállítja a megfelelő pin-ek irányát és generál két PWM jelet.
        """
        GPIO.setup(self.pwm_pin_1, GPIO.OUT)
        GPIO.setup(self.pwm_pin_2, GPIO.OUT)
        
        GPIO.setup(self.dir_1,GPIO.OUT)
        GPIO.setup(self.dir_2,GPIO.OUT)
        
        
        self.pwm1 = GPIO.PWM(self.pwm_pin_1,self.frequency)
        self.pwm2 = GPIO.PWM(self.pwm_pin_2,self.frequency)
        
        self.pwm1.start(0)
        self.pwm2.start(0)
    
    def set_speed(self,speed1,speed2):
        """
        A sebesség beállítására szolgál.
        
        Paraméterek:
            speed1: numerikus érték (0-100), amely meghatározza az első PWM jel periódusát.
            speed2: numerikus érték (0-100), amely meghatározza a második PWM jel periódusát.
        """
        self.speeds = [speed1,speed2]
        
        self.pwm1.ChangeDutyCycle(speed1)
        self.pwm2.ChangeDutyCycle(speed2)

    def stop_movement(self):
        """
        A megfelelő iránybitek és sebesség beállításával a robot mozgását megállítja.  
        """
        GPIO.output(self.dir_1,GPIO.LOW)
        GPIO.output(self.dir_2,GPIO.LOW)
        
        self.set_speed(0,0)
        time.sleep(1)
        
    def forward(self):
        """
        A megfelelő iránybitek és sebesség beállításával a robot mozgását hátrafele irányítja.  
    
        """
        GPIO.output(self.dir_1,GPIO.HIGH)
        GPIO.output(self.dir_2,GPIO.HIGH)
        
        self.set_speed(20,20)
        time.sleep(3)
        self.stop_movement()
        
    def backward(self):
        """
        A megfelelő iránybitek és sebesség beállításával a robot mozgását előre irányítja.
        
        """
        GPIO.output(self.dir_1,GPIO.LOW)
        GPIO.output(self.dir_2,GPIO.LOW)
        
        self.set_speed(90,90)
        time.sleep(2.5)
        self.stop_movement()
    
    def right(self):
        """
        A megfelelő iránybitek és sebesség beállításával a robot balra fordulását valósítja meg.
        
        """
       
        GPIO.output(self.dir_1,GPIO.HIGH)
        GPIO.output(self.dir_2,GPIO.LOW)
        
        self.set_speed(5,95)
        time.sleep(2.5)
        self.stop_movement()
        
    def left(self):
        """
        A megfelelő iránybitek és sebesség beállításával a robot jobbra fordulását valósítja meg.  
         
        """
        GPIO.output(self.dir_1,GPIO.LOW)
        GPIO.output(self.dir_2,GPIO.HIGH)
        
        self.set_speed(95,5)
        time.sleep(2.7)
        self.stop_movement()
    
    def execute_command(self,command_list):
        """
        Végigiterálja a parancsokat tartamazó listát és annak megfelelően végrehajtsa a parancsot.
        
        Paraméter:
            command_list: Lista, ami tartalmazza az utasításokat.
        """
        for command in command_list:
            if command == 'előre':
                self.forward()
            if command == 'hátra':
                self.backward()
            if command == 'jobbra':
                self.right()
            if command == 'balra':
                self.left()

            pass
            
        
    
    def cleanup(self):
        """
        Ez felelős a PWM jelek generálásának leállításával, valamint az erőforrások felszabadításáért.
        """
        self.pwm1.stop()
        self.pwm2.stop()
        GPIO.cleanup()
        
