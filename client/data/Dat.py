import os, json

class Dat:
    CHAR_SHIFT = 7
    
    @staticmethod
    def encrypt(data) -> str:
        res = ""
        data = str(data)
        for char in data:
                res += chr((ord(char) + Dat.CHAR_SHIFT) % 256)  
        return res.encode('utf-8')

    @staticmethod
    def decrypt(data) -> str:
        res = ""
        data = data.decode('utf-8')
        for char in data:
                res += chr((ord(char) -Dat.CHAR_SHIFT) % 256)  
        return res.replace("'",'"')


    @staticmethod
    def write(data: str | dict | list, src: str):
        if not os.path.exists(src):
            os.makedirs(os.path.dirname(src), exist_ok=True)
        encrypted_data = Dat.encrypt(data)        
        with open(src, 'wb') as f:
            f.write(encrypted_data)

    @staticmethod
    def read(src: str) -> dict:
        with open(src, 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = Dat.decrypt(encrypted_data)
        return json.loads(decrypted_data) 
