#!/usr/bin/env python
# This runs on python 2.7
'''
Usage: python webContent.py [options]\n
Options: -u   <target URL>   | The target to be scanned\n
         -w   <wordlist>     | The wordlist to be used for scanning \n
         -h   <help>         | Print help\n
Example: python webContent.py -u http://10.10.10.10/ -w /usr/share/wordlists/RockYou.txt
'''
import optparse
import urllib2
from threading import *
import Queue
import urllib

info = "Usage: python webContent.py [options]\nOptions: -u   <target URL>   | The target to be scanned\n         -w   <wordlist>     | The wordlist to be used for scanning \n         -h   <help>         | Print help\nExample: python webContent.py -u http://10.10.10.10/ -w /usr/share/wordlists/RockYou.txt"
def create_words(wordlist_file):
    fd = open(wordlist_file,"rb")
    raw_words = fd.readlines()
    fd.close
    found_resume = False
    words = Queue.Queue()
    for word in raw_words:
        word = word.rstrip()
        if resume is not None:
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print("Resuming wordlist from: %s" % resume)
        else:
            words.put(word)
    return words
def dir_bruter(word_queue,extensions=None):
    while not word_queue.empty():
        attempt = word.queue.get()
        attempt_list = []
        # check for file extensions, if there isnt one, its a directory
        if "." not in attempt:
            attempt_list.append("/%s/" % attempt)
        else:
            attempt_list.append("/%s" % attempt)
        if extensions:
            for extension in extensions:
                attempt_list.append("/%s%s" % (attempt, extension))
        for brute in attempt_list:
            url = "%s%s" % (target_url,urllib.quote(brute))
            try:
                headers = {}
                headers["User-Agent"]= user_agent
                r = urllib2.Request(url,headers=headers)
                response = urllib2.urlopen(r)
                if len(response.read()):
                    print("[%d] => %s" % (response.code,url))
            except urllib2.URLError,e:
                if hasattr(e, 'code') and e.code != 404:
                    print('! %d => %s' % (e.code, url))
                pass
def main():
    parser = optparse.OptionParser('usage%prog -u <target url> -w <wordlist file>')
    parser.add_option('-u', dest='tgt', type='string', help='Specify target URL')
    parser.add_option('-w', dest='wlist', type='string', help='Specify wordlist')
    (options, args) = parser.parse_args()
    threads = 50
    target_url = options.tgt
    wordlist_file = options.wordlist
    resume = None
    user_agent = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136"
    word_queue = create_words(wordlist_file)
    extensions = [".php",".bak",".orig",".inc",".html"]
    if(target_url == None) | (wordlist_file == None):
        print(parser.usage)
        sys.exit(0)
    for i in range(threads):
        t = threading.Thread(target=dir_bruter,args=(word_queue,extensions,))
        t.start()
if __name__ == "__main__":
    main()
