from Crypto.Cipher import AES
import base64
import re
import codecs

hexlify = codecs.getencoder('hex')
decode_hex = codecs.getdecoder("hex_codec")

class AESCBC:

    def __init__(self, key, iv):
        self.key = key
        self.iv = iv
        self.mode = AES.MODE_CBC
        self.size = AES.block_size
        self.pad = lambda s: s + (self.size - len(s) % self.size) * chr(self.size - len(s) % self.size)

    def encrypt(self, content):
        cryptor = AES.new(self.key, self.mode, self.iv)
        encrypted = cryptor.encrypt(self.pad(content))
        return hexlify(encrypted)[0]

    def decrypt(self, content):
        cryptor = AES.new(self.key, self.mode, self.iv)
        content += (len(content) % 4) * '='
        content = decode_hex(content)[0]
        decrypted = cryptor.decrypt(content)
        try:
            return re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f\n\r\t]').sub('', decrypted.decode())
        except Exception:
            raise ValueError("inputted value can not be decrypted.")


#test = AESCBC("6156ddb7fed8a4c22a1448fd6e834a79", "0000000000000000")
#print(test.encrypt("c"))
#print(test.decrypt("92AE2D631A12B3161E67D332C31A7B96"))