from Crypto.PublicKey import RSA

# encrypt
with open('keys/key.pub', 'r') as f:
	public_key = RSA.importKey(f.read())

secret_message = "the cake is a lie"
encrypted_message = public_key.encrypt(secret_message, "")[0]

# decrypt
with open('keys/key', 'r') as f:
	private_key = RSA.importKey(f.read())

print("Decrypted message: {}".format(private_key.decrypt(encrypted_message)))
