#!/usr/bin/python3

"""
   Words
   Get a 256bit value and turn it into a BIP39 word list
"""

import sys
import hashlib

word_list = ''

"""
    Gets a hex string representing a 256bit number (aka private key)
    Returns a binary string representing the same number
"""
def toBinary(key):
    scale = 16 ## equals to hexadecimal
    num_of_bits = 256
    binary = bin(int(key, scale))[2:].zfill(num_of_bits)
    return str(binary)


"""
    receive a binary string (len = 256)
    Split the  into 11 bits chunks, turn the chunks into integers
    return an array of integers
"""
def toBinArray(binary):
    array = []
    while(len(binary)>11):
        x = int(binary[0:11], 2)
        array.append(x)
        binary = binary[11:]
    array.append(int(binary, 2))
    return array


"""
    Get an array of integers, each integer is a position in the BIP39 wordlist
    return a list of 23 words whose positions are in the input array 
"""
def toWords(arr):
    global word_list
    # read the wordlist
    english = open("wordlist_eng.txt")
    word_list = english.read().split("\n")
    english.close()
    # return the list of words
    seed_phrase = [word_list[n] for n in arr]
    return seed_phrase

"""
    Get a binary string
    return the checksum of the binary string
    checksum = first 8 bits of the sha256 of the private key
"""
def getChecksum(binary):
    checksum = format(hashlib.sha256(int(binary, 2).to_bytes(32, byteorder="big")).digest()[0],"08b")[:8]
    return checksum



####################################################################################################
###
###    START
###

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")

if __name__ == "__main__": 
    # get key as a hex string from command parameter
    key = sys.argv[1]

    # Key to binary
    bin = toBinary(key)
    # binary to integer array
    arr = toBinArray(bin)
    # integer array to list of 23 words
    phrase = toWords(arr)
    # get the checsum of the binary
    checksum = getChecksum(bin)
    # compute last word position = last 3 bits of binary + 8 of the chechsum
    last = bin[-3:]+checksum
    # get last word from wordlist
    last_word = word_list[int(last, 2)]
    phrase[23] = last_word
    # print result
    print(' '.join(phrase))