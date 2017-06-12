#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep
from PIL import Image
import picamera.array
import numpy as np
import picamera
import thread
import curses
import argparse
import sys
import csv
import os

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
        img = self.stream.array[270:,:,0]
        self.stream.seek(0)
        self.stream.truncate()
        return img
    
    def save_img(self,img):
        im = Image.fromarray(img)
        imgPath = self.imgsPath + str(len(os.listdir(self.imgsPath))) + ".jpeg"
        im.save(imgPath)
    
    def preprocess_img(self,img):
        b_min = 0
        b_max = 135
        b_binary = np.zeros_like(img)
        b_binary[(img >= b_min) & (img <= b_max)] = 1
        
        return b_binary
        

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

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d","--drive",help="Drive Autonomously",action="store_true")
    group.add_argument("-c","--collect", help="Collect Images/Steering Data",action="store_true")
    args = parser.parse_args()

    if args.drive:
        return args
    elif args.collect:
        return args
    else:
        parser.print_help()   
        sys.exit(2)

if __name__ == '__main__':
    args = main()
    try:
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)
        carCtrl = Controller()
        carCam = Camera()
        if args.collect:                
            carCol = Collector()
            thread.start_new_thread(carCtrl.steering,())
            while True:
                carCam.save_img(carCam.capture())
                carCol.write(str(carCtrl.direction))
        elif args.drive:
            carCtrl.rear(0, 1, 70)
            while True:
                img = carCam.preprocess_img(carCam.capture())
                histogram = np.sum(img[img.shape[0]//2:,:], axis=0)
                right = np.sum(histogram[220:], dtype=int)
                left = np.sum(histogram[:100], dtype=int)
                if (right - left) > 200 or left == 0:
                    carCtrl.front(1, 0, 1)
                elif (right - left) < -200 or right == 0:
                    carCtrl.front(0, 1, 1)
                else:
                    carCtrl.front(0, 0, 0)
    except:
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()
        curses.endwin()
        carCtrl.BackPWM.stop()
        GPIO.cleanup()
        raise
