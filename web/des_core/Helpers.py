class Helpers:
    @staticmethod
    def isPrime(n) :
        if (n <= 1) :
            return False
        if (n <= 3) :
            return True
        if (n % 2 == 0 or n % 3 == 0) :
            return False
        i = 5
        while(i * i <= n) :
            if (n % i == 0 or n % (i + 2) == 0) :
                return False
            i = i + 6
        return True

    @staticmethod
    def getPrimeGreaterThan(number):
        while(True):
            number = number + 1
            if Helpers.isPrime(number):
                return number

    @staticmethod
    def getPrimeSmallerThan(number):
        while(True):
            number = number - 1
            if number < 2:
                print("<2")
                number = 256
            if Helpers.isPrime(number):
                return number
    # DES Helpers
    @staticmethod
    def textTo64bits(s):
        result = []
        for c in s:
            bits = bin(ord(c))[2:]
            bits = '00000000'[len(bits):] + bits
            result.extend([int(b) for b in bits])

        if(len(result) > 64):
            raise Exception('Text has > 64 bits')

        zeros = [0] * (64 - len(result))
        result = zeros + result
        
        return result

    @staticmethod
    def textTo56bits(s):
        result = []
        for c in s:
            bits = bin(ord(c))[2:]
            bits = '00000000'[len(bits):] + bits
            result.extend([int(b) for b in bits])

        if(len(result) > 56):
            raise Exception('Text has > 56 bits')

        zeros = [0] * (56 - len(result))
        result = zeros + result
        
        return result

    @staticmethod
    def textToBits(plainText):
        table = []
        for x in plainText:
            tableTemp = []
            for bit in list(format(ord(x), 'b')):
                tableTemp = tableTemp + [int(bit)]
                tableTemp = [0] * (8 - len(tableTemp)) + tableTemp
            table = table + tableTemp
        return table            

    @staticmethod
    def textFromBits(bits):
        chars = []
        for b in range(int(len(bits) / 8)):
            byte = bits[b*8:(b+1)*8]
            chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
        return ''.join(chars)

    @staticmethod
    def intToBin56(x):
        if x == 0: return [0]
        bit = []
        while x:
            bit.append(x % 2)
            x >>= 1
        return [0] * (56 - len(bit)) + bit[::-1]

    @staticmethod
    def hexStringToBinaryArray(hexString):
        binString = str(bin(int(hexString, 16)))[2:]
        return [int(bit) for bit in binString]

    @staticmethod
    def binToHex(bitsArr):
        binStr = ''.join([str(bit) for bit in bitsArr])
        hexRepresentation = hex(int(binStr, 2))
        return hexRepresentation

    @staticmethod
    def addBits(x, n):
            return [0] * (n - len(x)) + x

    @staticmethod
    def intToBin(x, bits=32):
        if x == 0: return [0] * bits
        bit = []
        while x:
            bit.append(x % 2)
            x >>= 1
        return [0] * (bits - len(bit)) + bit[::-1]

    @staticmethod
    def binaryArrayToInt(binaryArray):
        result = 0
        for bit in binaryArray:
            result = (result << 1) | bit
        return result


    @staticmethod
    def addParityBits(array):
        newArray = [0] * 8
        array.insert(7, 0)
        array.insert(15, 0)
        array.insert(23, 0)    
        array.insert(31, 0)
        array.insert(39, 0)
        array.insert(47, 0)
        array.insert(55, 0)
        array.insert(63, 0)
        return array

    @staticmethod
    def rotateArrayLeft(array, n):
        array = array[n:] + array[0:n]
        return array

    @staticmethod
    def xor(arrayOfBits1, arrayOfBits2):
        assert(len(arrayOfBits1) == len(arrayOfBits2))
        xoredArray = [0] * len(arrayOfBits1)
        for index in range(0, len(arrayOfBits1)):
            xoredArray[index] = arrayOfBits1[index] ^ arrayOfBits2[index]
        return xoredArray

# print(Helpers.textFromBits(Helpers.intToBin(1457920300136252297)))
