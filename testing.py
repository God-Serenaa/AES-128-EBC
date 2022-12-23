from AES import AES128_EBC

if __name__ == '__main__':
    key = "sajid ekta bolod"
    aes = AES128_EBC(key)
    #print(aes.key)
    message = "susmir biye hobe na"
    cipher_text = aes.encrypt_as_string(message)
    print(cipher_text)
    plain_text = aes.decrypt_as_string(cipher_text)
    print(plain_text)
