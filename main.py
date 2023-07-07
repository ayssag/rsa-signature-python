from utils import general as utils
import os
import algorithms.rsa as rsa
import algorithms.keyGenerator as keyGenerator
from texts.rsaCipher import cipher as rsaCipher
import getch
import time

def rsaMenu():
    print('Generating keys.........')
    keys = keyGenerator.generateRsaKeys()
    
    while True:
        screen = utils.readFile('utils/screens/rsa-screen.txt')
        os.system('clear')
        print(f'Keys: {keys}')
        utils.printScreen(screen)
        keyboard = getch.getch()

        if keyboard == 'b':
            break
        if keyboard == 'e':
            plaintext = utils.readFile('plaintext/rumbling-plain.txt')
            ciphertext = rsa.rsaEncryption(plaintext, keys)
            utils.waitKey(ciphertext)
        if keyboard == 'd':
            ciphertext = rsaCipher
            plaintext = rsa.rsaDecryption(ciphertext, keys)
            utils.waitKey(plaintext)

def mainMenu():
    while True:
        os.system('clear')
        screen = utils.readFile('utils/screens/main-screen.txt')
        utils.printScreen(screen)
        keyboard = getch.getch()

        if keyboard == 'q':
            break
        if keyboard == 'r':
            rsaMenu()

if __name__ == '__main__':
    mainMenu()