import json, hashlib

from cryptography.fernet import Fernet
class Dat:
    char_shift = 16
    @staticmethod
    def write(data: dict, src: str):
        json_data = json.dumps(data)
        
        encrypted_data = Dat.encrypt(json_data.encode('utf-8'))

        with open(src,'wb') as f:
            f.write(encrypted_data)
    
    @staticmethod
    def read(src: str):
        with open(src, 'rb') as f:
            encrypted_data = f.read()

        decrypted_data = Dat.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode('utf-8'))
    

    @staticmethod
    def encrypt(data):
        res = ""
        for char in data:
            if char.isalpha():
                if char.isupper():
                    res += chr((ord(char) + Dat.char_shift))  
                else:
                    res += chr((ord(char) + Dat.char_shift))  
            else:
                res += char 
        return res

    @staticmethod
    def decrypt(data):
        return Dat.encrypt(data, -Dat.char_shift)