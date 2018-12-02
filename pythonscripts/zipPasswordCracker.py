# Use to crack passwords on ZipFiles when other tools arent available
import zipfile
import optparse
from threading import Thread

def extractFile(zFile, password):
    try:
        zFile.extractall(pwd=password)
        print('[+] Found password ' + password + '\n'
    except:
        pass

def main():
   parser = optparse.OptionParser("useage%prog " + "-f <zipfile> -d <dictionary>")
   parser.add_option('-f', dest='zname', type='string', help='specify zip file')
   parser.add_option('-d', dest='dname', type='string', help='specify dictionary file')
   (options,args) = parser.parse_args()
