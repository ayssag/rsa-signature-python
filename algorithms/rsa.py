import hashlib
import os
from math import ceil
from hashlib import sha3_256
import base64

def sha1(message):
    """Calculates the SHA-1 hash of the input."""

    hasher = hashlib.sha1()
    hasher.update(message)

    return hasher.digest()

def mgf1(seed, messageLength):
    """Implements the Mask Generation Function 1 (MGF1) used within OAEP."""

    t = b''
    labelHashLength = len(sha1(b''))
    for c in range(ceil(messageLength / labelHashLength)):
        _c = c.to_bytes(4, byteorder='big')
        t += sha1(seed + _c)
    return t[:messageLength]

def bitwise_xor_bytes(a, b):
    """Performs a bitwise XOR operation between two byte strings a and b, returning the result as a new byte string"""
    
    result_int = int.from_bytes(a, byteorder="big") ^ int.from_bytes(b, byteorder="big")
    return result_int.to_bytes(max(len(a), len(b)), byteorder="big")

def int_to_bytes(number):
    """Converts an integer number into a byte string representation."""
    return number.to_bytes(length=(8 + (number + (number < 0)).bit_length()) // 8, byteorder='big', signed=True)

def rsaOaepEncryption(message, publicKey, label=b''):
    """Encrypts a message using RSA combined with OAEP padding."""
    
    e = publicKey['e']
    n = publicKey['n']

    k = publicKey['n'].bit_length() // 8

    messageLength = len(message)
    labelHash = sha1(label)
    labelHashLength = len(labelHash)

    padStringNull = b'\x00' * (k - messageLength - 2 * labelHashLength - 2)
    padConcatMessage = labelHash + padStringNull + b'\x01' + message

    seed = os.urandom(labelHashLength)
    messageMask = mgf1(seed, k - labelHashLength - 1)
    maskedMessage = bitwise_xor_bytes(padConcatMessage, messageMask)
    seedMask = mgf1(maskedMessage, labelHashLength)
    maskedSeed = bitwise_xor_bytes(seed, seedMask)

    ciphertext = b'\x00' + maskedSeed + maskedMessage

    ciphertext = int.from_bytes(ciphertext, byteorder='big')

    encoded_ciphertext = pow(ciphertext, e, n)
    
    return encoded_ciphertext

def rsaOaepDecryption(ciphertext, privateKey, label=b''):
    """Decrypts a message using RSA combined with OAEP padding."""
    
    d = privateKey['d']
    n = privateKey['n']

    ciphertext = int.from_bytes(ciphertext, 'big')
    k = privateKey['n'].bit_length() // 8

    ciphertext = pow(ciphertext, d, n).to_bytes(k, byteorder='big')
    
    #ciphertext = ciphertext.to_bytes(k, byteorder='big') 

    labelHash = sha1(label)
    labelHashLength = len(labelHash)

    _, maskedSeed, maskedMessage = ciphertext[:1], ciphertext[1:1+labelHashLength], ciphertext[1 + labelHashLength:]
    seedMask = mgf1(maskedMessage, labelHashLength)
    seed = bitwise_xor_bytes(maskedSeed, seedMask)
    messageMask = mgf1(seed, k - labelHashLength - 1)
    message = bitwise_xor_bytes(maskedMessage, messageMask)

    i = labelHashLength

    while i < len(message):
        if message[i] == 0:
            i += 1
            continue
        elif message[i] == 1:
            i += 1
            break

    plaintext = message[i:]

    return plaintext

    import base64

def encodeBase64(signature):
    # Convert the signature bytes to Base64
    signature_base64 = base64.b64encode(signature)

    # Convert the Base64 bytes to a string
    signature_base64_string = signature_base64.decode('utf-8')

    return signature_base64_string


def decodeBase64(signature_base64_string):
    # Convert the Base64 string to bytes
    signature_base64 = signature_base64_string.encode('utf-8')

    # Decode the Base64 bytes to signature bytes
    signature = base64.b64decode(signature_base64)

    return signature


def rsaSignature(message, publicKey):
    n = publicKey['n']
    e = publicKey['e']

    hashedMessage = sha3_256(message).digest()
    hashedMessage = int.from_bytes(hashedMessage, 'big')

    signature = pow(hashedMessage, e, n)
    
    signature = int_to_bytes(signature)
    
    return encodeBase64(signature)

def rsaVerifySignature(signature, message, privateKey):
    d = privateKey['d']
    n = privateKey['n']

    signature = decodeBase64(signature)
    signature = int.from_bytes(signature, byteorder='big')

    hashedMessage = sha3_256(message).digest()
    hashedMessage = int.from_bytes(hashedMessage, 'big')

    hashedSignature = pow(signature, d, n)

    verify = True if hashedSignature == hashedMessage else False

    return verify
