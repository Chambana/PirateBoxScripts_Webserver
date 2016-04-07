
from HTMLParser import HTMLParser
import time


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    saved = list()
    def handle_starttag(self, tag, attrs):
        #print "Encountered a start tag:", tag
        pass
    def handle_endtag(self, tag):
        #print "Encountered an end tag :", tag
        print self.saved
    def handle_data(self, data):
        #print "Encountered some data  :", data
        if data!=' ':
            self.saved.append(data)


def check_for_uav_command(line):
    for entry in line:
       if entry.lower() == "turn right":
           print "Found a Turn Right!"
       if entry.lower() == "turn left":
           print "Found a turn left!"

last_parsed_timestamp = None
parser = MyHTMLParser()

# read 1 line (the first line) and check it against the timestamp to see if new
while 1:
    chatfile = open("./data.txt", 'r')
    buf = chatfile.readline()
    print buf

    parser.feed(buf)
    if parser.saved[0]!=last_parsed_timestamp:
        print "saving new timestamp", parser.saved[0]
        last_parsed_timestamp=parser.saved[0]
        check_for_uav_command(parser.saved)
    else:
        print "No New Chat Data"
        time.sleep(1)
    chatfile.close()
    parser.saved=None
    parser.saved=list()


