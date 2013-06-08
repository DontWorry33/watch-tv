import urllib2
import re


class GrabData:
    def __init__(self, link):
        self.link = link

    def Percent(self):
        percent = re.findall(r'[font2 green red]\"\>(\d+\%\s\w+\s\w+)', self.link)
        return percent

    def Host(self):
        host = re.findall(r'span class="bold"\>(\w+)',self.link)
        return host

    def Link(self):
        link = re.findall(r'return frameLink\(\'([\w+\d+]+\=*\=*)',self.link)
        return link
if __name__ == "__main__":
	print "ERROR: THIS IS A MODULE. PLEASE RUN tvlinkseu4.py"
