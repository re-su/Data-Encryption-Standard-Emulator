from des_core.Helpers import Helpers
from des_core.KeyGenerator import KeyGenerator

import numpy as np

class Des:
    IP = [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ]

    IP2 = [
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25,
    ]

    E = [
        32, 1, 2, 3, 4, 5,
        4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1
    ]

    # S boxes
    S = [
        #S1
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],

        #S2
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
        ],

        #S3
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
        ],

        #S4
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
        ],

        #S5
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
        ],

        #S6
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
        ],

        #S7
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
        ],

        #S8
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
        ]
    ]

    P = [
        16, 7, 20, 21,
        29, 12, 28, 17,
        1, 15, 23, 26,
        5, 18, 31, 10,
        2, 8, 24, 14,
        32, 27, 3, 9,
        19, 13, 30, 6,
        22, 11, 4, 25,
    ]

    def __init__(self, keyGenerator = None):
        self.plainTextBits = []
        self.cipher = []

        print('Init DES')

        if(keyGenerator == None):
            self.keyGenerator = KeyGenerator()
        else:
            self.keyGenerator = keyGenerator        

    def encode64(self, plainText):
        table = []
        tableTemp = []
        #table.append(format(ord(x), 'b') for x in plainText)

        for x in plainText:
            tableTemp = []
            for bit in list(format(ord(x), 'b')):
                tableTemp = tableTemp + [int(bit)]
            tableTemp = [0] * (8 - len(tableTemp)) + tableTemp
            table = table + tableTemp
  
        print('Plain Text bits: ', table, len(table))

        self.plainTextBits = table

        self.plainTextBits = Helpers.addBits(table, 64)

        #print('Text in binary: ', self.plainTextBits, len(self.plainTextBits))

        #self.plainTextBits = [0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,1,0,1,0,0,0,1,0,1,0,1,1,0,0,1,1,1,1,0,0,0,1,0,0,1,1,0,1,0,1,0,1,1,1,1,0,0,1,1,0,1,1,1,1,0,1,1,1,1]
        self.cipher = self.plainTextBits

        self.initialPermutation()

        self.generateCipher('encode')

        print('before hex', self.cipher)
        return Helpers.binToHex(self.cipher)

    def decode64(self, hexCipher):
        self.plainTextBits = Helpers.hexStringToBinaryArray(hexCipher)

        print('dec64', self.plainTextBits)

        self.plainTextBits = Helpers.addBits(self.plainTextBits, 64)

        #print('Text in binary: ', self.plainTextBits, len(self.plainTextBits))

        #self.plainTextBits = [0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,1,0,1,0,0,0,1,0,1,0,1,1,0,0,1,1,1,1,0,0,0,1,0,0,1,1,0,1,0,1,0,1,1,1,1,0,0,1,1,0,1,1,1,1,0,1,1,1,1]
        self.cipher = self.plainTextBits

        self.initialPermutation()

        self.generateCipher('decode')

        return self.cipher

    def decode(self, hexCipher):
        table = []
        result = []

        if(hexCipher.startswith('0x')):
            hexCipher = hexCipher[2:]

        print('hex: ', hexCipher)   

        if(len(hexCipher) <= 16):
            print('<=16')
            return Helpers.textFromBits(self.decode64(hexCipher)) 

        #hexCipher =  hexCipher + ('0' * (len(hexCipher) - (int(len(hexCipher)/16) * 16)))
        to16 = (len(hexCipher) - (int(len(hexCipher)/16) * 16))
        print('HEx ', hexCipher)


        for i in range(0, int((len(hexCipher)+to16) / 16)):
            table = table + self.decode64('0x' + hexCipher[i * 16:(i+1)*16])
            print(i, hexCipher[i * 16:(i+1)*16])

        return Helpers.textFromBits(table)



    def encode(self, plainText):
        result = ""
        if(len(plainText) <= 8):
            print('<=8')
            return self.encode64(plainText)
        print('szalo', (len(plainText) - (int(len(plainText)/8) * 8)))
        #plainText = plainText + ('x' * (8-(len(plainText) - (int(len(plainText)/8) * 8))))
        to8 = (8-(len(plainText) - (int(len(plainText)/8) * 8)))
        for i in range(0, int((len(plainText)+to8) / 8)):
            result = result + self.encode64(plainText[i * 8:(i+1)*8])[2:]
            print('e ', self.encode64(plainText[i * 8:(i+1)*8])[2:])
        return '0x' + result       

    def initialPermutation(self):
        index = 0
        cipherCopy = [0] * len(self.cipher)
        for indexFromIP in Des.IP:
            cipherCopy[index] = self.cipher[indexFromIP - 1]
            index = index + 1

        self.cipher = cipherCopy
    
    def finalPermutation(self):
        index = 0
        cipherCopy = [0] * len(self.cipher)
        for indexFromIP2 in Des.IP2:
            cipherCopy[index] = self.cipher[indexFromIP2 - 1]
            index = index + 1

        self.cipher = cipherCopy

    @staticmethod
    def functionF(right, key):
        right = Des.expansion(right)
        rightXorKey = Helpers.xor(right, key)
        sBoxInput = [[0] * 6] * int(len(rightXorKey) / 6)
        sBoxOutput = [[0] * 4] * int(len(rightXorKey) / 6)

        
        output = []
        for index in range(0, int(len(rightXorKey) / 6)):
            sBoxInput = rightXorKey[((index)*6):((index+1)*6)]

            row = Helpers.binaryArrayToInt([sBoxInput[0], sBoxInput[5]])
            column = Helpers.binaryArrayToInt([sBoxInput[1], sBoxInput[2], sBoxInput[3], sBoxInput[4]])

            output = output + Helpers.intToBin(Des.S[index][row][column], 4)
        output = Des.permutationP(output)
        return output

    @staticmethod
    def expansion(right):
        index = 0
        rightCopy = [0] * len(Des.E)
        for indexFromExpansionMatrix in Des.E:
            rightCopy[index] = right[indexFromExpansionMatrix - 1]
            index = index + 1
        # print('Expanssion: ')
        # print(right)
        # print(rightCopy)
        return rightCopy

    @staticmethod
    def permutationP(right):
        index = 0
        rightCopy = [0] * 32
        #print('permP',len(right))
        for indexFromPermutationMatrix in Des.P:
            rightCopy[index] = right[indexFromPermutationMatrix - 1]
            index = index + 1
        return rightCopy

    def round(self, roundIndex, mode):
        right = self.cipher[32:]
        left = self.cipher[0:32]

        if(mode == 'encode'):
            key = self.keyGenerator.getKey(roundIndex)
        else:
            key = self.keyGenerator.getKeyDecode(roundIndex)

        right = Helpers.xor(left, Des.functionF(right, key))

        self.cipher = self.cipher[32:] + right

    def generateCipher(self, mode):

        for roundIndex in range(0, 16): # 0 to 15
            self.round(roundIndex + 1, mode)
            #print(roundIndex, self.cipher)
        
        left = self.cipher[0:32]
        right = self.cipher[32:]

        self.cipher = right + left

        self.finalPermutation()

# coder = Des()
# coder.encode('Hello')
# print('1', coder.plainTextBits)
# print('2', coder.cipher)
# print('3', Helpers.binToHex(coder.cipher))

# coder.decode(Helpers.textFromBits(coder.cipher))
# print('3', coder.plainTextBits)
# print('4', Helpers.textFromBits(coder.cipher))  

# decoder = Des(coder.keyGenerator.reverseKeys())

# decoder.encode(Helpers.textFromBits(coder.cipher))
# print('3', decoder.plainTextBits)
# print('4', Helpers.textFromBits(decoder.cipher))       