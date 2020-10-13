from Cipher import Cipher

cip = Cipher()

key = input('Введите ключ: ')
text = input('Введите слово для шифрования: ')
key_text = input('Введите слово для расшифрования: ')

d = cip.cipher(key, text, key_text)


print(d)




