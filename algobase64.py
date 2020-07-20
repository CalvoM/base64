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


def decoder(data):
    """Decodes the base64 encoding

    Args:
        data (string): The base encoded string

    Returns:
        string: Decoded string
    """
    mapped_data=[]
    for d in data:
        if d!='=':
            bin_c = bin(base64_chars.index(d)).replace('0b','')
            bin_c = '0'*(6-len(bin_c))+bin_c
            mapped_data.append(bin_c)
    
    str_data = ''.join(mapped_data)
    byt = wrap(str_data,8)
    word = ''.join([chr(int(x,2)) for x in byt])
    word = word.rstrip('\x00')
    return word

if __name__ == "__main__":
    encoded_str=''
    with open(sys.argv[1],'rb') as f:
        encoded_str = encoder(f.read())
    with open(sys.argv[2],'w') as f:
        f.write((decoder(encoded_str)),"utf-8")