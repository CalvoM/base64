#! /usr/bin/python
import sys
from textwrap import wrap
from math import ceil

base64_chars = [x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="]


def correct_byte(char):
    """Get the binary version of characters and parse into bytes

    Args:
        char (chr/int): byte to change to binary number

    Returns:
        string: the binary number of the <char> argument in 8 bits
    """
    if isinstance(char,int):# if the <char> argument is a number e.g. in images
        char = chr(char)
    byt = bin(ord(char))
    byt=byt.replace('0b','')
    needed_length = 8
    byt_len = len(byt)
    return '0'*(needed_length - byt_len)+byt


def get_bits(text):
    """Get the bits from the <text> in byte form

    Args:
        text (string): text to convert to bit form

    Returns:
        string: the bits for <text> 
    """
    bits = ''.join([correct_byte(t) for t in text])
    return bits


def encoder(text):
    """The entry function to base64 encoding for <text>

    Args:
        text (string): the payload to be encoded

    Returns:
        string: the encoding
    """
    text_bits = get_bits(text)
    sextet = wrap(text_bits,6) # group into bits of 6

    if len(sextet[-1]) != 6 :
        sextet[-1] = sextet[-1]+ '0'*(6-len(sextet[-1]))#each sextet should have 6 bits
    if len(sextet)%4 !=0:#total number of sextents should be multiple of 4
        next_target = ceil(len(sextet)/4) *4
        diff = next_target - len(sextet)
        for i in range(diff):
            sextet.append(correct_byte(chr(64)))#append padding

    word = ''.join([base64_chars[int(s,2)] for s in sextet])
    return word


if __name__ == "__main__":
    with open(sys.argv[1],'rb') as f:
        print(encoder(f.read()))