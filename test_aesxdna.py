from aes_dna import AESxDNA

if __name__ == '__main__':
    key = "sajid ekta bolod"
    aes = AESxDNA(key)
    message = "susmir biye hobe na"
    cipher_text = aes.encrypt(message)
    print(cipher_text)
    plain_text = aes.decrypt(cipher_text)
    print(plain_text)