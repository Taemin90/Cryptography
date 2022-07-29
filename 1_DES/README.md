# Data Encryption Standard, DES

## DES.py
 - This file is core of DES Algotithm. 'DES_Parameters.py' should be imported in it.
 - 'MyDES' is a class for DES.
 - 'des_encrypt', 'des_decrypt' methods in 'MyDES' class are needed for DES.

 |method|Input|Output|Description|
 |-------|-----|-----|---------|
 |des_encrypt|Original 64 BitVector|Encrypted 64 BitVector|Encrypt 1 block(64bits) of original data|
 |des_decrypt|Encrypted 64 BitVector|Decrypted 64 BitVector|Decrypt 1 block(64bits) of encrypted data|
 
 - Simple example
  <img width="925" alt="image" src="https://user-images.githubusercontent.com/57401207/181732422-2292f75b-83f9-4b42-8dd9-c68935bcb942.png">


## DES_parameters.py
 - Permutation lists, S-Box, PC-1, PC-2 are included.
 - This file should be imported in 'DES.py'.

## main_des.py
 - Just for verification of implemented DES Algorithm
