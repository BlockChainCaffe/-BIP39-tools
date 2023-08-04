#!/usr/bin/python3

"""
   NoiseGen
   Get noise from soundcard and turn it into a 256 random key
"""

import sys
import sounddevice as sd
import hashlib

MIC_RND_SEC = 30        # seconds of mic sampling for private key generation
SHA_RND_RND = 2048      # number of sha256 rounds for private key generation
MIC_SLT_SEC = 5         # seconds of mic sampling for salt
SAMPLE_RATE = 44100     # rate of sampling for audio recording 


def getNoise(sec):
    sound = sd.rec(int(SAMPLE_RATE * sec), samplerate=SAMPLE_RATE, channels=2, blocking=True)
    return hashlib.sha256(bytearray(b''.join(sound))).hexdigest()


def generatePrivateKey():
    # create random by reading the mic for rnd_len seconds
    print("Getting entropy from %s secs mic audio recording... Please wait (and make some noise)" % str(MIC_RND_SEC) )
    hash0=getNoise(MIC_RND_SEC)

    # create random for salt
    print("Getting salt from %s secs mic audio recording... Please wait (and make some noise)" % str(MIC_SLT_SEC))
    salt0=getNoise(MIC_SLT_SEC)

    """ sha256 rounds """
    print ("Iterating %s rounds of salted sha256 hashing..." % SHA_RND_RND )
    for i in range(0,SHA_RND_RND):
        hash0=hashlib.sha256((hash0+salt0).encode('utf-8')).hexdigest()

    return hash0

####################################################################################################
###
###    START
###

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")

if __name__ == "__main__": 
    key = generatePrivateKey()
    print(key)

