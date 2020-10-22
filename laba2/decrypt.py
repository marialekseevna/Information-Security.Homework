from laba2.RC5 import RC5

class Decrypt(RC5):

    # расшифровывание
    def decrypt(self, data):
        A = int.from_bytes(data[:self.w8], byteorder='little')
        B = int.from_bytes(data[self.w8:], byteorder='little')
        for i in range(self.R, 0, -1):
            B = self.__rightshift(B - self.S[2 * i + 1], A) ^ A
            A = self.__rightshift(A - self.S[2 * i], B) ^ B
        B = (B - self.S[1]) % self.mod
        A = (A - self.S[0]) % self.mod
        return (A.to_bytes(self.w8, byteorder='little')
                + B.to_bytes(self.w8, byteorder='little'))

    # передается имя входного файла и выходного
    def decryptFile(self, inpFileName, outFileName):
        with open(inpFileName, 'rb') as inp, open(outFileName, 'wb') as out:
            run = True
            while run:
                text = inp.read(self.w4)
                if not text:
                    break
                if len(text) != self.w4:
                    run = False
                text = self.decrypt(text)
                if not run:
                    # удаляем добавленные на этапе шифрования b'\x00'
                    text = text.rstrip(b'\x00')
                out.write(text)

    def decryptBytes(self, data):
        res, run = b'', True
        while run:
            temp = data[:self.w4]
            if len(temp) != self.w4:
                run = False
            res += self.decrypt(temp)
            data = data[self.w4:]
            if not data:
                break
        return res.rstrip(b'\x00')