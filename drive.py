#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep
import curses
import csv
import picamera
import picamera.array
from PIL import Image
import os
import thread

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

class Camera:
    imgsPath = "data/imgs/"

    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.vflip = True
        self.stream = picamera.array.PiYUVArray(self.camera)
    
    def capture(self):
        self.camera.capture(self.stream, format='yuv')
        image = self.stream.array[200:,:, 0]
        self.stream.seek(0)
        self.stream.truncate()
        im = Image.fromarray(image)
        imgPath = self.imgsPath + str(len(os.listdir(self.imgsPath))) + ".jpeg"
        im.save(imgPath)
        

class Controller:

    MotorFront1 = 36
    MotorFront2 = 38
    MotorFront = 40

    MotorBack1 = 37
    MotorBack2 = 35
    MotorBack = 33
    
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.MotorFront1, GPIO.OUT)
        GPIO.setup(self.MotorFront2, GPIO.OUT)
        GPIO.setup(self.MotorFront, GPIO.OUT)
        GPIO.output(self.MotorFront, 0)

        GPIO.setup(self.MotorBack1, GPIO.OUT)
        GPIO.setup(self.MotorBack2, GPIO.OUT)
        GPIO.setup(self.MotorBack, GPIO.OUT)
        GPIO.output(self.MotorBack, 0)

    def front(self,f1,f2,f):
        GPIO.output(self.MotorFront1, f1)
        GPIO.output(self.MotorFront2, f2)
        GPIO.output(self.MotorFront, f)

    def rear(self,b1,b2,b):
        GPIO.output(self.MotorBack1, b1)
        GPIO.output(self.MotorBack2, b2)
        GPIO.output(self.MotorBack, b)
    
    def steering(self, carCtrl, direction):
        char = screen.getch()
        if char == ord('d'):
            carCtrl.front(0, 1, 1)
            direction = 1
        elif char == ord('a'):
            carCtrl.front(1, 0, 1)
            direction = 2
        elif char == ord('s'):
            carCtrl.front(0, 0, 0)
            direction = 0 
        if char == ord('w'):
            carCtrl.rear(0, 1, 1)
        if char == ord(' '):
            carCtrl.rear(1, 0, 1)
            sleep(0.1)
            carCtrl.rear(0, 0, 0)

class Collector:

    def __init__(self, fileName='data/steering.csv'):
        file = open(fileName, 'w')
        self.writer = csv.writer(file)

    def write(self, direction):
        self.writer.writerow(direction)

if __name__ == '__main__':
    carCtrl = Controller()
    carCam = Camera()
    carCol = Collector()
    direction = 0
    try:
        thread.start_new_thread(screen.getch,(carCtrl, direction))
        while True:
            #thread.start_new_thread(screen.getch,(carCtrl, direction))
            carCam.capture()
            carCol.write(str(direction))
    except:
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()
        curses.endwin()
        GPIO.cleanup()
        raise
