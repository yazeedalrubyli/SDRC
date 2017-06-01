#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep
import curses

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

MotorFront1 = 36
MotorFront2 = 38
MotorFront = 40

MotorBack1 = 37
MotorBack2 = 35
MotorBack = 33


class Controller:

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(MotorFront1, GPIO.OUT)
        GPIO.setup(MotorFront2, GPIO.OUT)
        GPIO.setup(MotorFront, GPIO.OUT)
        GPIO.output(MotorFront, 0)

        GPIO.setup(MotorBack1, GPIO.OUT)
        GPIO.setup(MotorBack2, GPIO.OUT)
        GPIO.setup(MotorBack, GPIO.OUT)
        GPIO.output(MotorBack, 0)

    def front(self,f1,f2,f):
        GPIO.output(MotorFront1, f1)
        GPIO.output(MotorFront2, f2)
        GPIO.output(MotorFront, f)

    def rear(self,b1,b2,b):
        GPIO.output(MotorBack1, b1)
        GPIO.output(MotorBack2, b2)
        GPIO.output(MotorBack, b)


if __name__ == '__main__':
    carCtrl = Controller()
    try:
        while True:
            char = screen.getch()
            if char == ord('d'):
                carCtrl.front(0, 1, 1)
            elif char == ord('a'):
                carCtrl.front(1, 0, 1)
            if char == ord('w'):
                carCtrl.rear(0, 1, 1)
            elif char == ord('s'):
                carCtrl.rear(1, 0, 1)
                sleep(0.05)
                carCtrl.rear(0, 0, 0)
            if char == ord(' '):
                carCtrl.front(0, 0, 0)
    except:
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()
        curses.endwin()
        GPIO.cleanup()
