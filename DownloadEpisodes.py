import urllib2
import re
import pickle
import thread
import threading
import sys
import time
import os

from loadingbar import *

class Worker(threading.Thread):
	def __init__(self, shows,loadBar):
		threading.Thread.__init__(self)
		self.loadBar = loadBar
		self.showCodes = shows
		self.finished=False
		if os.path.isdir("data"):
			pass
		else:
			os.mkdir('data')

	def seasons(self):
		resp = urllib2.urlopen('http://www.tv-links.eu/tv-shows/{0}_{1}/'.format(self.show,self.code)).read()    
		seDirty = re.findall(r'(season\_)(\d+)\W(\w+)\/',resp)
		for se in seDirty:
			lastSeason = se[1]
			break
		return int(lastSeason)
		       

	def episodes(self):
		resp = urllib2.urlopen('http://www.tv-links.eu/tv-shows/{0}_{1}/'.format(self.show,self.code)).read()    
		episodeStore = []
		seasonCount = self.seasons()
		badchar = '&#039;'
		badchar2 = '&amp;'
		restDirty = re.findall(r'c1\"\>(\w+\s)(\d+)\<\/\w+\>\s\<\w+\s\w+\=\"\w+\"\>([\w+\s\-*\.*\:*\,*\&*\#*\0*\3*\;*\(*\)*]+)',resp)
		for restC in restDirty:
			if restC[1] == '0':
				continue
			if restC[1] == '1':
				episodeStore.append('\nSeason: '+str(seasonCount) + "\n")
				seasonCount-=1
			episodeStore.append(restC[0]+' '+restC[1]+' '+restC[2].replace(badchar,"'").replace(badchar2,"&"))
		return episodeStore
	def run(self):
		count = 1
		for k,v in self.showCodes.iteritems():
			self.show = k
			self.code = v
			self.loadBar.update()
			pickle.dump(self.episodes(),open('data/'+k+'.txt','w'))
			#print "Episodes for {0} have been downloaded".format(k)
		self.finished=True


class SplitDict:
	def __init__(self, dic):
		self.dic = dic

	def split(self):
		t1={}
		t2={}
		for x in range(len(self.dic)/2):
			t1[self.dic.keys()[x]]=self.dic.values()[x]
		for y in range(len(self.dic)/2,len(self.dic)):
			t2[self.dic.keys()[y]]=self.dic.values()[y]
		return t1,t2
		
if __name__ == "__main__":
        pass
        '''
	def loadShows():
		codes = {}
		websiteCodes = urllib2.urlopen('http://legacylogin.zzl.org/codesList.txt')
		for indCode in websiteCodes:
			relink = indCode.split(':')
			codes[relink[0]]=relink[1].replace('\n','')
		return codes
	
	rofl = loadShows()
	count=1

	lmao = {}
	haha={}
	for x in range(len(rofl)/2):
		lmao[rofl.keys()[x]]=rofl.values()[x]
	for y in range(len(rofl)/2,len(rofl)):
		haha[rofl.keys()[y]]=rofl.values()[y]
	try:
		worker1 = Worker(lmao)
		worker2 = Worker(haha)
		worker1.start()
		worker2.start()
		progress = ProgressBar("Downloading TV Show Episode Lists",'=')
		updatevalue = 100/len(rofl)
		while worker1.finished is not True and worker2.finished is not True:
			progress.updateBar(count)
			count+=updatevalue
			time.sleep(3)
		progress.close()
	except Exception as e:
		print e,'\n\n\n'
		sys.exit(0)
        '''
