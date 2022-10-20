password = "0123456789abcdef"
s_box = [
    ['63', '7C', '77', '7B', 'F2', '6B', '6F', 'C5', '30', '01', '67', '2B', 'FE', 'D7', 'AB', '76'],
    ['CA', '82', 'C9', '7D', 'FA', '59', '47', 'F0', 'AD', 'D4', 'A2', 'AF', '9C', 'A4', '72', 'C0'],
    ['B7', 'FD', '93', '26', '36', '3F', 'F7', 'CC', '34', 'A5', 'E5', 'F1', '71', 'D8', '31', '15'],
    ['04', 'C7', '23', 'C3', '18', '96', '05', '9A', '07', '12', '80', 'E2', 'EB', '27', 'B2', '75'],
    ['09', '83', '2C', '1A', '1B', '6E', '5A', 'A0', '52', '3B', 'D6', 'B3', '29', 'E3', '2F', '84'],
    ['53', 'D1', '00', 'ED', '20', 'FC', 'B1', '5B', '6A', 'CB', 'BE', '39', '4A', '4C', '58', 'CF'],
    ['D0', 'EF', 'AA', 'FB', '43', '4D', '33', '85', '45', 'F9', '02', '7F', '50', '3C', '9F', 'A8'],
    ['51', 'A3', '40', '8F', '92', '9D', '38', 'F5', 'BC', 'B6', 'DA', '21', '10', 'FF', 'F3', 'D2'],
    ['CD', '0C', '13', 'EC', '5F', '97', '44', '17', 'C4', 'A7', '7E', '3D', '64', '5D', '19', '73'],
    ['60', '81', '4F', 'DC', '22', '2A', '90', '88', '46', 'EE', 'B8', '14', 'DE', '5E', '0B', 'DB'],
    ['E0', '32', '3A', '0A', '49', '06', '24', '5C', 'C2', 'D3', 'AC', '62', '91', '95', 'E4', '79'],
    ['E7', 'C8', '37', '6D', '8D', 'D5', '4E', 'A9', '6C', '56', 'F4', 'EA', '65', '7A', 'AE', '08'],
    ['BA', '78', '25', '2E', '1C', 'A6', 'B4', 'C6', 'E8', 'DD', '74', '1F', '4B', 'BD', '8B', '8A'],
    ['70', '3E', 'B5', '66', '48', '03', 'F6', '0E', '61', '35', '57', 'B9', '86', 'C1', '1D', '9E'],
    ['E1', 'F8', '98', '11', '69', 'D9', '8E', '94', '9B', '1E', '87', 'E9', 'CE', '55', '28', 'DF'],
    ['8C', 'A1', '89', '0D', 'BF', 'E6', '42', '68', '41', '99', '2D', '0F', 'B0', '54', 'BB', '16']
]
xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)


def permutation(text):
    l = []
    for index in [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]:
        l.append(text[index])
    return l


def mix_single_column(a):
    # please see Sec 4.1.2 in The Design of Rijndael
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ xtime(a[0] ^ a[1])
    a[1] ^= t ^ xtime(a[1] ^ a[2])
    a[2] ^= t ^ xtime(a[2] ^ a[3])
    a[3] ^= t ^ xtime(a[3] ^ u)
    return a


def mix_columns(text):
    l = []
    for i in range(4):
        for val in mix_single_column(text[:4]):
            l.append(val)
        text = text[4:]
    return l


def key_xor(text, word):
    text_index = 0
    l = []
    w0, w1, w2, w3 = word[0], word[1], word[2], word[3]
    for i in range(4):
        for j in range(4):
            str1 = str(bin(eval("w" + str(i))[j]))[2:]
            str2 = str(bin(text[text_index]))[2:]
            l.append(eval("0b" + xor(str1, str2)))
            text_index += 1
    return l


def xor(a, b):
    ans = ""
    while len(a) < 8:
        a = "0" + a
    while len(b) < 8:
        b = "0" + b
    for i in range(8):
        ans += "1" if a[i] != b[i] else "0"
    return ans


def pad(text):
    if len(text) % 16 != 0:
        text += "{" * (16 - len(text) % 16)
    return text


def convert_to_hex(text):
    l = []
    for value in text:
        l.append(eval("0x" + str(value.encode('utf-8').hex())))
    return l


def onebitleftshift(text):
    l = []
    for i in range(4):
        if i == 3:
            l.append(text[i - 3])
        else:
            l.append(text[i + 1])
    return l


def bytesubstitution(text):
    l = []
    for i in range(len(text)):
        hex_value = str(hex(text[i]))
        if len(hex_value) == 4:
            index1, index2 = eval("0x" + hex_value[-2]), eval("0x" + hex_value[-1])
        else:
            index1, index2 = 0, eval("0x" + hex_value[-1])
        l.append(eval("0x" + s_box[index1][index2]))
    return l


def addroundkey(text, round):
    all_round_key = [
        ["00000001", "00000000", "00000000", "00000000"],
        ["00000010", "00000000", "00000000", "00000000"],
        ["00000100", "00000000", "00000000", "00000000"],
        ["00001000", "00000000", "00000000", "00000000"],
        ["00010000", "00000000", "00000000", "00000000"],
        ["00100000", "00000000", "00000000", "00000000"],
        ["01000000", "00000000", "00000000", "00000000"],
        ["10000000", "00000000", "00000000", "00000000"],
        ["00011011", "00000000", "00000000", "00000000"],
        ["00110110", "00000000", "00000000", "00000000"]
    ]
    current_round_key = all_round_key[round]
    l = []
    for i in range(4):
        str_text = str(bin(text[i]))[2:]
        l.append(eval("0b" + xor(current_round_key[i], str_text)))
    return l


class AES:
    def __init__(self, k):
        self.key = self.__key_expansion(pad(k))

    def __key_expansion(self, k):
        w = []
        for i in range(0, 16, 4):
            w.append(convert_to_hex(k[i:i + 4]))
        for round in range(10):
            for i in range(4):
                if i == 0:
                    w1 = addroundkey(bytesubstitution(onebitleftshift(w[-1])), round)
                else:
                    w1 = w[-1]
                w2 = w[-4]
                l = []
                for j in range(4):
                    str_w1 = str(bin(w1[j]))[2:]
                    str_w2 = str(bin(w2[j]))[2:]
                    l.append(eval("0b" + xor(str_w1, str_w2)))
                w.append(l)
        return w

    def __encrypt_block(self, block):
        hexed = convert_to_hex(block)
        all_round_cipher_text = [hexed]
        text = key_xor(hexed, self.key[:4])
        dupe_key = self.key[4:]
        for _ in range(9):
            text = key_xor(mix_columns(permutation(bytesubstitution(text))), dupe_key[:4])
            all_round_cipher_text.append(text)
            dupe_key = dupe_key[4:]
        all_round_cipher_text.append(key_xor(permutation(bytesubstitution(text)), dupe_key[:4]))
        print(" ".join(str(hex(i)) for i in all_round_cipher_text[-1]))
        return all_round_cipher_text

    def encrypt(self, plain_text):
        padded_plain_text = pad(plain_text)
        cipher_text = []
        while padded_plain_text:
            cipher_text.append(self.__encrypt_block(padded_plain_text[:16]))
            padded_plain_text = padded_plain_text[16:]


aes = AES(password)
# print("\n".join(" ".join(str(hex(i)) for i in keys) for keys in aes.key[:4]))
aes.encrypt("susmir biye hobe")
