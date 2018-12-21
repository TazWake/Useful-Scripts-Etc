#!/usr/bin/env python3
'''This script takes ASCII input and turns it into
ordinal numbers for use in String.fromCharCode
situations. If your string includes quotes, then
it is advised you use -c """your data"""'''
import argparse

def create_encoded_js(i):
    '''This encodes the incoming text'''
    decstring = ""
    for char in i:
        decstring += str(ord(char)) + ","
    return decstring[:-1]
def main():
    '''Run the program'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', required='true', help="string to convert")
    args = parser.parse_args()
    if args.c is None:
        exit()
    else:
        print(create_encoded_js(args.c))
if __name__ == '__main__':
    main()
