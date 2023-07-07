def rsaEncryption(plaintext, key):
    message = []
    for line in plaintext:
        message.extend([ord(char) for char in line])

    n = key['public']['n']
    e = key['public']['e']

    ciphertext = [pow(char, e, n) for char in message]

    return ciphertext

def rsaDecryption(ciphertext, key):
    n = key['public']['n']
    d = key['private']

    plaintext = [pow(char, d, n) for char in ciphertext]
    plaintext = ''.join([chr(int(char)) for char in plaintext])

    return plaintext