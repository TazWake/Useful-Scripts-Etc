#!/usr/bin/env python3
import argparse
``` This script takes ASCII input and turns it into ordinal numbers for use in String.fromCharCode situations. If your string includes quotes, then it is advised you use -c """your data"""```
def createEncodedJS(ascii):
    decstring = ""
    for char in ascii:
        decstring += str(ord(char)) + ","
    return decstring[:-1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-c', required='true', metavar='ASCII Code to convert', help='Provide the ASCII code to convert')
    args = parser.parse_args()
    if args.c == None:
        exit()
    else:
        print(createEncodedJS(args.c))        

if __name__ == '__main__':
    main() 
