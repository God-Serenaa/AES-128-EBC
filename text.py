from AES import AES128_EBC

if __name__ == '__main__':
    password = "sajid ekta bolod"
    aes = AES128_EBC(password)
    message = "susmir biye hobe na"
    cipher_text = aes.encrypt(message)
    print(cipher_text)
    plain_text = aes.decrypt(cipher_text)
    print(plain_text)
