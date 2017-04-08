#!/usr/bin/env python 
import sys, os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random

if len(sys.argv) != 2:
	print('Usage: {} <LOG_FILE>'.format(sys.argv[0]))
	exit(1)

key_file = os.environ.get('PRIVATE_KEY', 'keys/key')
log_file = sys.argv[1]

with open(key_file, 'r') as f:
	private_key = RSA.importKey(f.read())

with open(log_file, 'r') as f:
	log = f.read()

with open('{}_aes'.format(log_file), 'rb') as f:
	encrypted_aes_key = f.read()

# decrypt the AES key with the private key
decrypted_aes_key = private_key.decrypt(encrypted_aes_key)

# parse the initialization vector and use it
# along with decrypted AES key to decrypt the log
iv = log[0:AES.block_size]
aes_cipher = AES.new(decrypted_aes_key, AES.MODE_CFB, iv)
decrypted_log = aes_cipher.decrypt(log[AES.block_size:])
print(decrypted_log)
