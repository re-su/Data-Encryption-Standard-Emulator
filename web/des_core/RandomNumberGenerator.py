import numpy as np
import time
import cv2

from des_core.Helpers import Helpers

class RandomNumberGenerator:
    def __init__(self, m = 256):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        self.cameraWidth = 600
        self.cameraHeight = 600

        self.cap.set(3, self.cameraWidth)
        self.cap.set(4, self.cameraHeight)

        self.primes = [0, 0]
        self.m = m

        self.newSeed()

    def getClockRandom(self):
        self.clockRandom = time.time()
        self.clockRandom = self.clockRandom  - int( self.clockRandom )
        self.clockRandom = int(int(self.clockRandom * 10000000) - int(self.clockRandom * 10000))

    def generateRandomNumberFromImage(self):

        xp = int((self.primes[0] * self.primes[1]) % self.frame.shape[0])
        yp = int((self.primes[0] * self.primes[1]) % self.frame.shape[1])

        R = int(self.frame[xp, yp][0])
        G = int(self.frame[xp, yp][1])
        B = int(self.frame[xp, yp][2])

        self.pixelValue = ((R + G + B) + (R * G * B)) / 1000 / 1.6180339

    def newSeed(self):
        r, self.frame = self.cap.read()
        self.generateRandomNumberFromImage()

        # Generate primes p1 and p2
        self.primes[0] = Helpers.getPrimeSmallerThan(self.pixelValue * 100  + self.pixelValue)
        self.primes[1] = Helpers.getPrimeGreaterThan(self.pixelValue)
        
        # Calculate seed
        self.next = (self.primes[0] * self.primes[1] % self.m )

    def generateNext(self):
        self.generateRandomNumberFromImage()

        self.b = (self.primes[0] * self.primes[1] * self.pixelValue) % self.m 

        self.primes[0] = Helpers.getPrimeGreaterThan(self.primes[0]*self.primes[1] % 255**2)
        self.primes[1] = Helpers.getPrimeGreaterThan(self.primes[0]+self.primes[1] % 255**2) 

        self.next = int((self.next * self.b + (self.primes[0] * self.primes[1])) % self.m)
    
    def getNext(self):
        self.generateNext()
        return self.next
