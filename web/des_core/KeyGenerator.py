from des_core.RandomNumberGenerator import RandomNumberGenerator
from des_core.Helpers import Helpers

class KeyGenerator:
    PC_1 = [
        57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4
    ]
    PC_2 = [
        14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32
    ]
    def __init__(self):
        self.randomNumberGenerator = RandomNumberGenerator(2**56)
        
        self.initialKey = self.randomNumberGenerator.getNext()

        self.keyBits = Helpers.intToBin56(self.initialKey)
        self.keyBits = Helpers.addParityBits(self.keyBits)

        #self.keyBits = [0,0,0,1,0,0,1,1,0,0,1,1,0,1,0,0,0,1,0,1,0,1,1,1,0,1,1,1,1,0,0,1,1,0,0,1,1,0,1,1,1,0,1,1,1,1,0,0,1,1,0,1,1,1,1,1,1,1,1,1,0,0,0,1]

        self.keys = [[0] * 64] * 16

        self.generateKeys()

    def newKey(self):
        self.initialKey = self.randomNumberGenerator.getNext()

        self.keyBits = Helpers.intToBin56(self.initialKey)
        self.keyBits = Helpers.addParityBits(self.keyBits)

        #self.keyBits = [0,0,0,1,0,0,1,1,0,0,1,1,0,1,0,0,0,1,0,1,0,1,1,1,0,1,1,1,1,0,0,1,1,0,0,1,1,0,1,1,1,0,1,1,1,1,0,0,1,1,0,1,1,1,1,1,1,1,1,1,0,0,0,1]

        self.keys = [[0] * 64] * 16

        self.generateKeys()

        return self.initialKey
    

    def keyInitialPermutation(self):
        keyBitsCopy = [0] * 56
        index = 0
        for permutationMatrixIndex in KeyGenerator.PC_1:
            keyBitsCopy[index] = self.keyBits[permutationMatrixIndex - 1]
            index = index + 1
        self.keyBits = keyBitsCopy
    
    def rotateHalvesLeftOnce(self):
        left = [0] * 28
        right = [0] * 28

        left = self.keyBits[0:28]
        right = self.keyBits[28:]

        left = Helpers.rotateArrayLeft(left, 1)
        right =  Helpers.rotateArrayLeft(right, 1)

        self.keyBits = left + right

        return self.keyBits

    def rotateHalvesLeftTwice(self):
        self.rotateHalvesLeftOnce()
        self.rotateHalvesLeftOnce()

        return self.keyBits

    def generateKeys(self):
        oneRotationIndexes = [0, 1, 8, 15]

        self.keyInitialPermutation()

        for rotationIndex in range(0, 16):
            if rotationIndex in oneRotationIndexes:
                self.keys[rotationIndex] = self.rotateHalvesLeftOnce()
            else:
                self.keys[rotationIndex] = self.rotateHalvesLeftTwice()

    @staticmethod
    def secondKeyPermutation(key):
        keyCopy = [0] * len(KeyGenerator.PC_2)
        index = 0
        for permutationMatrix2Index in KeyGenerator.PC_2:
            keyCopy[index] = key[permutationMatrix2Index - 1]
            index = index + 1
        return keyCopy


    def getKey(self, roundIndex):
        # print(self.keys[roundIndex - 1], roundIndex - 1)
        return KeyGenerator.secondKeyPermutation(self.keys[roundIndex - 1])

    def getKeyDecode(self, roundIndex):
        tempKeysSet = list(reversed(self.keys))
        return KeyGenerator.secondKeyPermutation(tempKeysSet[roundIndex - 1])
    
    def reverseKeys(self):
        self.keys = list(reversed(self.keys))
        return self