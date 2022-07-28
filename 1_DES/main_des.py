from DES import MyDES
from BitVector import *
import binascii
import random


def random_key_gen(num):
    result = ""
    for _ in range(num):
        result += str(random.randint(0, 1))
    return result


if __name__ == '__main__':
    des = MyDES()

    """ Encryption """
    key = BitVector(bitstring=random_key_gen(64))
    plaintext_file = open('./data/plaintext.txt', 'rb')
    enc_text_file = open('./data/des_encrypt_text.txt', 'wt')
    plaintext = plaintext_file.read()
    plaintext_ascii = bin(int(binascii.hexlify(plaintext), 16))[2:].zfill(len(plaintext)*8)
    enc_text = BitVector(size=0)
    i = 0
    while i < len(plaintext_ascii):
        block_64 = bytes(plaintext_ascii[i:i + 64], "ascii").zfill(64)
        enc_text = enc_text + des.des_encrypt(data=BitVector(bitstring=block_64.decode('ascii')), key=key)
        i = i + 64

    enc_text_str = str(enc_text)
    enc_text_file.write(enc_text_str)

    enc_text_file.close()
    plaintext_file.close()

    """ Decryption """
    enc_text_file = open('./data/des_encrypt_text.txt', 'rt')
    dec_text_file = open('./data/des_decrypt_text.txt', 'wt')
    enc_text = enc_text_file.read()

    dec_text = BitVector(size=0)
    i = 0
    while i < len(enc_text):
        block_64 = bytes(enc_text[i:i + 64], "ascii")
        dec_text = dec_text + des.des_decrypt(data=BitVector(bitstring=block_64.decode('ascii')), key=key)
        i = i + 64

    dec_text_hex = hex(int(str(dec_text), 2))
    dec_text = bytes.fromhex(dec_text_hex[2:]).decode('ascii')
    dec_text_file.write(dec_text)

    dec_text_file.close()
    enc_text_file.close()
