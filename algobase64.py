#! /usr/bin/python
import sys
from textwrap import wrap
from math import ceil
base64_chars = [x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="]
def correct_byte(char):
    if isinstance(char,int):
        char = chr(char)
    byt = bin(ord(char))
    byt=byt.replace('0b','')
    needed_length = 8
    byt_len = len(byt)
    return '0'*(needed_length - byt_len)+byt


def get_bytes(text):
    bits = ''.join([correct_byte(t) for t in text])
    return bits


def encoder(text):
    text_bits = get_bytes(text)
    sextet = wrap(text_bits,6)
    if len(sextet[-1]) != 6 :
        sextet[-1] = sextet[-1]+ '0'*(6-len(sextet[-1]))
    if len(sextet)%4 !=0:
        next_target = ceil(len(sextet)/4) *4
        diff = next_target - len(sextet)
        for i in range(diff):
            sextet.append(correct_byte(chr(64)))
    word = ''.join([base64_chars[int(s,2)] for s in sextet])
    return word


if __name__ == "__main__":
    with open(sys.argv[1],'rb') as f:
        print(encoder(f.read()))