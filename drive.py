import RPi.GPIO as GPIO
import pygame
from pygame.locals import *

pygame.init()

MotorFront1 = 36
MotorFront2 = 38
MotorFront = 40

MotorBack1 = 37
MotorBack2 = 35
MotorBack = 33

class Controller(object):
	def __init__(self):
		pygame.init()

        	GPIO.setmode(GPIO.BOARD)

        	GPIO.setup(MotorFront1,GPIO.OUT)
	        GPIO.setup(MotorFront2,GPIO.OUT)
        	GPIO.setup(MotorFront,GPIO.OUT)

	        GPIO.setup(MotorBack1,GPIO.OUT)
	        GPIO.setup(MotorBack2,GPIO.OUT)
	        GPIO.setup(MotorBack,GPIO.OUT)
 
	def move(f1, f2, f, b1, b2, b):
		GPIO.output(MotorFront1,f1)
	        GPIO.output(MotorFront2,f2)
	        GPIO.output(MotorFront,f)

		GPIO.output(MotorBack1,b1)
	        GPIO.output(MotorBack2,b2)
        	GPIO.output(MotorBack,b)

if __name__ == "__main__":
	carCtrl = Controller()
	GPIO.cleanup()
	while 1:
		events = pygame.event.get()
		for event in events:
		    if event.type == pygame.KEYDOWN:
		        if event.key == pygame.K_LEFT:
		            print(0)
		        if event.key == pygame.K_RIGHT:
		            print(1)
