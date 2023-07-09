import getch
import os

def readFile(filename):
    file = open(filename, 'r')
    message = [line for line in file]
    file.close()
    return message

def writeFile(filename, content):
    file = open(filename, 'w')
    file.write(content)
    file.close()

def printScreen(screen, key=None):
    for line in screen:
        if '_' in line and key:
            print('Current key:\n', key)
        print(line)

def waitKey(results):
    os.system('clear')
    print('____________________________')
    print(results)
    print('b -> back')
    while True:
        keyboard = getch.getch()
        if keyboard == 'b':
            break