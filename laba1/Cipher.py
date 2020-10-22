class Cipher:
    # шифруем
    def encrypt(self, key, text):
        alf = 'abcdefghijklmnopqrstuvwxyz'
        result = []
        space = 0
        for index, ch in enumerate(text):
            if ch != ' ':
                mj = alf.index(ch)
                kj = alf.index(key[(index - space) % len(key)])
                cj = (mj + kj) % len(alf)
                result.append(alf[cj])
            else:
                space += 1
                result.append(' ')
        return ''.join(result)

    # расшифровываем
    def decrypt(self, key, key_text):
        alf = 'abcdefghijklmnopqrstuvwxyz'
        result = []
        space = 0
        for index, ch in enumerate(key_text):
            if ch != ' ':
                cj = alf.index(ch)
                kj = alf.index(key[(index - space) % len(key)])
                mj = (cj - kj) % len(alf)
                result.append(alf[mj])
            else:
                space += 1
                result.append(' ')
        return ''.join(result)


    def cipher(self, key, text=None, key_text=None):
        if not key_text:
            return self.encrypt(key, text)
        else:
            return self.decrypt(key, key_text)