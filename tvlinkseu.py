#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import urllib2
import urllib
import cookielib
import webbrowser
import sys
import thread
import threading
import time

class WatchTV:
	def __init__(self):
		self.listShows = []
		self.episodeStore = []
		self.cj = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		self.loadShows()
		
		
	def loadShows(self):
		self.showCodes = {}
		websiteCodes = urllib2.urlopen('http://legacylogin.zzl.org/codesList.txt')
		for indCode in websiteCodes:
			relink = indCode.split(':')
			self.showCodes[relink[0]]=relink[1].replace('\n','')
		self.chooseShow()
	
	def chooseShow(self):
		self.show = raw_input("Enter a TV show: ").lower()
		self.show = self.show.replace(' ','-')
		self.show = self.show.replace("'",'-')
		try:
			self.showCodes[self.show]
		except:
			try:
				self.showCodes['the-'+self.show]
				self.show = 'the-'+self.show
			except:
				try:
					self.showCodes[self.show+'-']
					self.show = self.show+'-'
				except:
					try:
						self.showCodes['the-'+self.show+'-']
						self.show = 'the-'+self.show+'-'
					except:
						self.addShow()
		
		self.chooseEpisode()
						
	def addShow(self):
		self.show = self.show.replace('-',"+")
		resp = self.opener.open('http://www.tv-links.eu/_search/?s={0}'.format(self.show))
		findShowCode = re.findall(r'(tv\-shows\/)([\w+\-*]+)\_(\d+)',resp.read())
		for findCodes in findShowCode:
			try:
				areYouSure = raw_input("Is {0} the show you want to add (y/n): ".format(findCodes[1].lower()))
				if areYouSure == 'y':
					if self.showCodes[findCodes[1].lower()]:
						print "Show already in database with name: ",findCodes[1].lower().replace('-',' ')
						break
					store_code_data = urllib.urlencode({'show':findCodes[1].lower(),'code':findCodes[2]})
					self.opener.open('http://legacylogin.zzl.org/codes.php')
					resp = self.opener.open('http://legacylogin.zzl.org/codes.php',store_code_data)
					print "{0} has been added successfully! Re-starting Program\n\n".format(findCodes[1].lower())
				else:
					print "Show not added"
					break
				self.chooseShow()
			except:
				store_code_data = urllib.urlencode({'show':findCodes[1].lower(),'code':findCodes[2]})
				self.opener.open('http://legacylogin.zzl.org/codes.php')
				resp = self.opener.open('http://legacylogin.zzl.org/codes.php',store_code_data)
				print "{0} has been added successfully! Re-starting Program\n\n".format(findCodes[1].lower())
				self.loadShows()
		self.chooseShow()
				
	def chooseEpisode(self):
		print '\n\n'
		if len(self.episodeStore) < 1:	
			self.findEpisodes()
		for indEp in self.episodeStore:
			print indEp
		print '\n\n'
		self.season=int(raw_input("Season: "))
		self.episode = int(raw_input("Episode: "))
		resp = self.opener.open('http://www.tv-links.eu/tv-shows/{0}_{1}/season_{2}/episode_{3}/'.format(self.show,self.showCodes[self.show],self.season,self.episode))
		self.showDate()
		self.showSummary()
		newChoice = raw_input("Watch this episode(y/n): ").lower()
		while newChoice!='y':
			print '\n\n'
			for indEp in self.episodeStore:
				print indEp
			print '\n\n'
			self.season=int(raw_input("Season: "))
			self.episode = int(raw_input("Episode: "))
			resp = self.opener.open('http://www.tv-links.eu/tv-shows/{0}_{1}/season_{2}/episode_{3}/'.format(self.show,self.showCodes[self.show],self.season,self.episode))
			self.showDate()
			self.showSummary()
			newChoice = raw_input("Watch this episode(y/n): ").lower()
		self.linksOfShow()
		
	def linksOfShow(self):
		num=0
		dirtyList = self.showLinks()
		host = raw_input("Enter a specific host(leave blank to show all): ")
		print "Num   Code     Pct    Host"
		print "--------------------------------"
		for link in dirtyList:
			if len(host.strip()) < 1:
				num+=1
				print str(num)+")",link[1],link[2],link[3]
				self.listShows.append([str(num)+")",link[1],str(link[2])+"%",link[3]])
			elif host in link[3]:
				num+=1
				print str(num)+")",link[1],str(link[2])+"%",link[3]
				self.listShows.append([str(num)+")",link[1],str(link[2])+"%",link[3]])
		if len(self.listShows) < 1:
			host = "all"
			print "Unable to find shows. Please check hostname or connection to internet.".format(host)
			raw_input()
			self.chooseShow()
		numberShow = raw_input("\nEnter number: ")
		for x in self.listShows:
			if numberShow+")" in x[0]:
				showCode = self.listShows[int(numberShow)-1][1]
		webbrowser.open("http://www.tv-links.eu/gateway.php?data={0}".format(showCode))
		print "Show has been opened in your web browser. Enjoy!"
		anotherEp = raw_input("Watch another episode?: ").lower()
		if anotherEp == 'y':
			self.chooseEpisode()
		else:
			raw_input()
		
	
	def findSeasons(self):
		resp = self.opener.open('http://www.tv-links.eu/tv-shows/{0}_{1}/'.format(self.show,self.showCodes[self.show]))
		seDirty = re.findall(r'(season\_)(\d+)\W(\w+)\/',resp.read())
		for se in seDirty:
			lastSeason = se[1]
			break
		return int(lastSeason)
		
	def findEpisodes(self):
		seasonCount = self.findSeasons()
		badchar = '&#039;'
		badchar2 = '&amp;'
		resp = self.opener.open('http://www.tv-links.eu/tv-shows/{0}_{1}/'.format(self.show,self.showCodes[self.show]))
		restDirty = re.findall(r'c1\"\>(\w+\s)(\d+)\<\/\w+\>\s\<\w+\s\w+\=\"\w+\"\>([\w+\s\-*\.*\:*\,*\&*\#*\0*\3*\;*\(*\)*]+)',resp.read())
		for restC in restDirty:
			if restC[1] == '0':
				continue
			if restC[1] == '1':
				#print "\nSeason",seasonCount,'\n'
				self.episodeStore.append('\nSeason: '+str(seasonCount) + "\n")
				seasonCount-=1
			#print restC[0]+' '+restC[1],restC[2].replace(badchar,"'").replace(badchar2,"&")
			self.episodeStore.append(restC[0]+' '+restC[1]+' '+restC[2].replace(badchar,"'").replace(badchar2,"&"))

	def showDate(self):
		resp = self.opener.open('http://www.tv-links.eu/tv-shows/{0}_{1}/season_{2}/episode_{3}/'.format(self.show,self.showCodes[self.show],self.season,self.episode))
		dates = re.findall(r'(\d+)\W(\d+)\W(\d+)',resp.read())
		for date in dates:
			if date[2] > 2000 and len(date[2]) == 4:
				airDate = date[0]+'/'+date[1]+'/'+date[2]
				break
		print "\nRelease Date: ", airDate, "\n"


	def showSummary(self):
		resp = self.opener.open('http://www.tv-links.eu/tv-shows/{0}_{1}/season_{2}/episode_{3}/'.format(self.show,self.showCodes[self.show],self.season,self.episode))   
		badchar = '&#039;'
		badchar2 = '&quot;'
		sumShow = "None"
		summary = re.findall(r'(font2\W\W\s)([\w+\s\:*\;*\-*\.*\,*\&*\#*0*3*9*;*\(*\)*\é*]+)',resp.read())
		#hiddenSummary = re.findall(r'(hide\"\>)([\w+\s\:*\;*\-*\.*\,*\&*\#*0*3*9*;*\(*\)*\é*]+)',resp.read())
		for x in summary:
			if badchar in x[1] or badchar2 in x[1]:
				sumShow = x[1].replace(badchar, "'").replace(badchar2, '"').replace('é','e')
			elif badchar not in x[1]:
				sumShow = x[1]
		print "\nSummary of Show: ", sumShow , "\n"

		
	def showLinks(self):
		resp = self.opener.open('http://www.tv-links.eu/tv-shows/{0}_{1}/season_{2}/episode_{3}/'.format(self.show,self.showCodes[self.show],self.season,self.episode))
		regFind = re.findall(r'(vers_h\[\d+\])\s\=\s\w+\s\w+\(\W(\w+\W*\W*)\W\W\s\d+\W\s(\d+)\W\s\W(\w+)',resp.read())
		return regFind


if __name__ == "__main__":
	print "Enjoy watching tv shows free!"
	program = WatchTV()
