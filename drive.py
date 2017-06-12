#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep
from PIL import Image
import picamera.array
import picamera
import thread
import curses
import argparse
import sys
import csv
import os
'''
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
'''
class Camera:
    imgsPath = "data/imgs/"

    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.vflip = True
        self.camera.hflip = True
        #self.camera.resolution = (320, 160)
        self.camera.start_preview()
        sleep(5)
        self.stream = picamera.array.PiYUVArray(self.camera)

    def capture(self):
        self.camera.capture(self.stream, format='yuv')
        image = self.stream.array[270:,:,0]
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
        GPIO.setwarnings(False)

        GPIO.setup(self.MotorFront1, GPIO.OUT)
        GPIO.setup(self.MotorFront2, GPIO.OUT)
        GPIO.setup(self.MotorFront, GPIO.OUT)
        GPIO.output(self.MotorFront, 0)

        GPIO.setup(self.MotorBack1, GPIO.OUT)
        GPIO.setup(self.MotorBack2, GPIO.OUT)
        GPIO.setup(self.MotorBack, GPIO.OUT)
        GPIO.output(self.MotorBack, 0)
        self.BackPWM = GPIO.PWM(self.MotorBack,100)
        self.BackPWM.start(0)
        self.BackPWM.ChangeDutyCycle(0)
        
        self.direction = 0
    
    def front(self,f1,f2,f):
        GPIO.output(self.MotorFront1, f1)
        GPIO.output(self.MotorFront2, f2)
        GPIO.output(self.MotorFront, f)

    def rear(self,b1,b2,b):
        GPIO.output(self.MotorBack1, b1)
        GPIO.output(self.MotorBack2, b2)
        self.BackPWM.ChangeDutyCycle(b)
    
    def steering(self):
        while True:
            char = screen.getch()
            if char == ord('d'):
                self.front(0, 1, 1)
                self.direction = 1
            elif char == ord('a'):
                self.front(1, 0, 1)
                self.direction = 2
            elif char == ord('s'):
                self.front(0, 0, 0)
                self.direction = 0 
            if char == ord('w'):
                self.rear(0, 1, 70)
            if char == ord(' '):
                self.rear(1, 0, 1)
                sleep(0.1)
                self.rear(0, 0, 0)

class Collector:

    def __init__(self, fileName='data/steering.csv'):
        file = open(fileName, 'a')
        self.writer = csv.writer(file)

    def write(self, direction):
        self.writer.writerow(direction)

if __name__ == '__main__':
    try:
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)
            if opt in ("-c", "--collect"):
                try:
                    carCtrl = Controller()
                    carCam = Camera()
                    carCol = Collector()
                    thread.start_new_thread(carCtrl.steering,())
                    while True:
                        carCam.capture()
                        carCol.write(str(carCtrl.direction))
                except:
                    carCtrl.BackPWM.stop()
                    GPIO.cleanup()
            elif opt in ("-a","--autonomous"):
                import tensorflow
    except:
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()
        curses.endwin()
        raise
