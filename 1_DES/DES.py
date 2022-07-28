from DES_Parameters import *
from BitVector import *


class MyDES:
    def __init__(self):
        pass

    def initial_permutaion(self, data: BitVector):
        """
        :param data: 64 BitVector block
        :return: 64 BitVector block
        """
        result = BitVector(size=64)
        for i in range(64):
            result[i] = data[INITIAL_PERMUTATION[i] - 1]

        return result

    def final_permutation(self, data: BitVector):
        """
        :param data: 64 BitVector block
        :return: 64 BitVector block
        """
        # result = bin(0)[2:].zfill(64)
        result = BitVector(size=64)
        for i in range(64):
            result[i] = data[FINAL_PERMUTATION[i] - 1]

        return result

    def expansion_permutation(self, data: BitVector):
        """
        :param data: 32 BitVector block
        :return: 48 BitVector block
        """
        result = BitVector(size=48)
        for i in range(48):
            result[i] = data[EXPANSION_PERMUTATION[i] - 1]
        return result

    def s_box(self, data: BitVector, sbox_num: int):
        """
        :param data: 6 BitVector
        :param sbox_num: 1 - 8 integer
        :return: 4 BitVector
        """
        row = data[0] + data[5] * 2
        column = int(data[1:5])
        return BitVector(intVal=S_BOX[sbox_num][row][column], size=4)

    def permutation_f(self, data: BitVector):
        """
        :param data: 32 BitVector
        :return: 32 BitVector
        """
        result = BitVector(size=32)
        for i in range(32):
            result[i] = data[PERMUTATION[i] - 1]
        return result

    def f_function(self, data: BitVector, key: BitVector):
        """
        :param data: 32 BitVector
        :param key: 32 ButVector
        :return: 32 ButVector
        """
        ep_result = self.expansion_permutation(data=data)
        xor_result = ep_result ^ key

        sbox_result = BitVector(size=0)
        for i in range(8):
                sbox_result += self.s_box(data=xor_result[i:i + 6], sbox_num=i)
        result = self.permutation_f(data=sbox_result)

        return result

    def round(self, data: BitVector, key: BitVector):
        """
        :param data: 64 BitVector
        :param key: 48 BitVector
        :return: 64 BitVector
        """
        # [left, right] = data.divide_into_two()
        left = data[:32]
        right = data[32:]
        return right + left ^ self.f_function(data=right, key=key)

    def key_schedule_enc(self, key: BitVector):
        """
        :param key: 64 BitVector
        :return: 48 BitVector subkeys for every iteration
        """
        pc_1_result = BitVector(size=56)
        for i in range(32):
            pc_1_result[i] = key[PC_1[i] - 1]

        c = pc_1_result[:28]
        d = pc_1_result[28:]
        for i in range(16):
            subkey = BitVector(size=48)
            if i == 0 or i == 1 or i == 8 or i == 15:
                c = c << 1
                d = d << 1
            else:
                c = c << 2
                d = d << 2
            shift_result = c + d
            for j in range(48):
                subkey[j] = shift_result[PC_2[j] - 1]

            yield subkey

    def key_schedule_dec(self, key: BitVector):
        """
        :param key: 64 BitVector
        :return: 48 BitVector subkeys for every iteration
        """
        pc_1_result = BitVector(size=56)
        for i in range(32):
            pc_1_result[i] = key[PC_1[i] - 1]

        c = pc_1_result[:28]
        d = pc_1_result[28:]
        for i in range(16):
            subkey = BitVector(size=48)
            if i == 0:
                pass
            elif i == 1 or i == 8 or i == 15:
                c = c >> 1
                d = d >> 1
            else:
                c = c >> 2
                d = d >> 2
            shift_result = c + d
            for j in range(48):
                subkey[j] = shift_result[PC_2[j] - 1]

            yield subkey

    def des_encrypt(self, data: BitVector, key: BitVector):
        """
        :param data: 64 BitVector
        :param key: 64 BitVector
        :return: 64 BitVector
        """
        round_result = self.initial_permutaion(data=data)
        for subkey in self.key_schedule_enc(key):
            round_result = self.round(data=round_result, key=subkey)
        return self.final_permutation(data=round_result[32:]+round_result[:32])

    def des_decrypt(self, data: BitVector, key: BitVector):
        """
        :param data: 64 BitVector
        :param key: 64 BitVector
        :return: 64 BitVector
        """
        round_result = self.initial_permutaion(data=data)
        for subkey in self.key_schedule_dec(key):
            round_result = self.round(data=round_result, key=subkey)
        return self.final_permutation(data=round_result[32:]+round_result[:32])
