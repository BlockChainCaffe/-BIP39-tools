#!/usr/bin/python3

import sys
import keyboard
import re

# inquirer
import inquirer

# rich components
from rich import print
from rich.console import Console
from rich.progress import Progress

## Global configuration dictionary (I'm lazy)
console = Console()



####################################################################################################
###
###    FUNCTIONS
###


''' 
    Ask the type of dice the user has
    Returns int the number of faces = max value of dice
'''
def askDiceType() :
    question = [
        inquirer.List(
            "size",
            message="What type of dice do you have? Count the faces/values",
            choices=["d2/coin", "d4", "d6", "d8", "d10", "d12", "d20", "d100"],
        ),
    ]
    faces = inquirer.prompt(question)
    faces = faces['size'][1:]
    faces = re.sub(r'/.*$','',faces)
    return int(faces)


''' 
    Read Inputs from user
'''
def getRoll(max):
    val = 0
    print('roll dice [red]>[/red] ', end = '')
    if max >= 10:
        val = input()
    else:
        val = keyboard.read_key()

    if val.isnumeric():
        val = int(val)
        if val > 0 and val <= max:
            return val
    return 0

'''
    Return bits (string) acording to number and max
'''
def getBits(n, dice):
    if n<1 or n>dice:
        raise "what the numbers?"

    # turn max to binary and reverse so that position of bit mathes exponent of 2
    _dice = list(str(bin(dice)[2:]))
    _dice.reverse()
    log = len(_dice)-1

    while log>=0:
        bm = 2**log
        if _dice[log] == '1':
            if n <= bm:
                return str(bin(n-1)[2:]).zfill(log)
            else:
                n = n - bm

        log = log-1

    # must never get here
    raise "WTF"


####################################################################################################
###
###    START
###

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")

if __name__ == "__main__": 
    console.clear(True)
    diceType = askDiceType()
    key_size = 256
    key_hexlen = 2*int(key_size/8)
    private_key = ''


    bar_length = console.size[0] - 20

    print("Dice: ", diceType)

    while (len(private_key)<key_size) :
        console.clear(True)
        print('Got ',len(private_key),' of ', key_size, '  ', end=None)
        done = int((bar_length * len(private_key)) / key_size)
        print('[reverse blue]'+(' '*done)+'[/reverse blue]', end=None)
        print('[white]'+('_'*(bar_length-done))+'[/white]', end=None)
        print()

        roll = getRoll(diceType)
        if roll == 0:
            continue
        private_key = private_key + getBits(roll, diceType)

    private_key = private_key[:256]
    # print('binary: ', private_key)
    # print("int : ", int(private_key, 2))
    private_key = hex(int(private_key, 2))[2:]
    print('Your private key is: ', '0x'+str(private_key).zfill(key_hexlen))
