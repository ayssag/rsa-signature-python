from utils import general as utils
import os
import algorithms.rsa as rsa
import algorithms.keyGenerator as keyGenerator
import getch
import time

def rsaMenu():
    """Implements the RSA Menu."""

    print('\n\nGenerating keys.........')
    keys = keyGenerator.generateRsaKeys()
    signature = None
    plaintext = None
    ciphertext = None
    
    while True:
        screen = utils.readFile('utils/screens/rsa-screen.txt')
        os.system('clear')
        utils.printScreen(screen)
        keyboard = getch.getch()

        if keyboard == 'b':
            break

        if keyboard == 'k':
            os.system('clear')
            utils.waitKey(keys)

        if keyboard == 'e':
            with open('texts/rumbling-plain.txt', 'rb') as file:
                plaintext = file.read()
            
            ciphertext = rsa.rsaOaepEncryption(plaintext, keys['public'])

            with open('texts/rsa-cipher.txt', 'wb') as file:
                file.write(rsa.int2Bytes(ciphertext))

            utils.waitKey(rsa.int2Bytes(ciphertext))

        if keyboard == 'd':
            with open('texts/rsa-cipher.txt', 'rb') as file:
                ciphertext = file.read()
            
            plaintext = rsa.rsaOaepDecryption(ciphertext, keys['private'])

            utils.waitKey(plaintext)

        if keyboard == 's':
            with open('texts/rumbling-plain.txt', 'rb') as file:
                plaintext = file.read()

            signature = rsa.rsaSignature(plaintext, keys['public'])

            utils.waitKey(signature)
        
        if keyboard == 'v':
            verify = rsa.rsaVerifySignature(signature, plaintext, keys['private'])

            utils.waitKey(verify)

def mainMenu():
    """Implements the Main Menu"""

    while True:
        os.system('clear')
        screen = utils.readFile('utils/screens/main-screen.txt')
        utils.printScreen(screen)
        keyboard = getch.getch()

        if keyboard == 'q':
            break
        if keyboard == 'r':
            rsaMenu()
        if keyboard == 'a':
            print('\nNão foi implementado...')
            time.sleep(2)

if __name__ == '__main__':
    mainMenu()