import time
import os.path

for file in os.listdir("."):
    print file
    print "Creation Time (Windows) -> %s" % (time.ctime(os.path.getctime(file)))
    print "Modified -> %s" % (time.ctime(os.path.getmtime(file)))
    print "Accessed -> %s" % (time.ctime(os.path.getatime(file)))
    print "\n"
