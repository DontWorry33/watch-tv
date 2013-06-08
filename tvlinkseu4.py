#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import urllib2
import urllib
import cookielib
import webbrowser
import sys
import os
import time
import pickle
from colorama import *
init()

#self made modules
from GetData import *
from DownloadEpisodes import *
from EpisodeOptions import *


class WatchTV:
	def __init__(self):
		self.listShows = []
		self.episodeStore = []
		self.cj = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		self.loadShows()
		
		
	def loadShows(self):
		self.showCodes = {}
		websiteCodes = urllib2.urlopen('http://dontworry.solidwebhost.com/codesList.txt')
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
		while True:
			userChoice = EpisodeOptions(self.showCodes,self.show)
			check = userChoice.episodePortal()
			if check == False:
				self.manualEpisode()
			else:
				self.season, self.episode = userChoice.chooseEpisode()
				self.showDate()
				self.showSummary()
				othChoice = raw_input("Watch this episode (y/n): ").lower()
				if othChoice == 'y':
					self.linksOfShow()
				else:
					continue



	def manualEpisode(self):
		print '\n\n'
		if len(self.episodeStore) < 1:  
			self.findEpisodes()
		for indEp in self.episodeStore:
			print indEp
		print '\n\n'
		self.season=int(raw_input("Season: "))
		self.episode = int(raw_input("Episode: "))
		#resp = self.opener.open('http://www.tv-links.eu/tv-shows/{0}_{1}/season_{2}/episode_{3}/video-results/'.format(self.show,self.showDict[self.show],self.season,self.episode))
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
			resp = self.opener.open('http://www.tv-links.eu/tv-shows/{0}_{1}/season_{2}/episode_{3}/video-results/'.format(self.show,self.showDict[self.show],self.season,self.episode))
			self.showDate()
			self.showSummary()
			newChoice = raw_input("Watch this episode(y/n): ").lower()
		self.linksOfShow()

		
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
					self.opener.open('http://dontworry.solidwebhost.com/codes.php')
					resp = self.opener.open('http://dontworry.solidwebhost.com/codes.php',store_code_data)
					print "{0} has been added successfully! Re-starting Program\n\n".format(findCodes[1].lower())
				else:
					print "Show not added"
					break
				self.chooseShow()
			except:
				store_code_data = urllib.urlencode({'show':findCodes[1].lower(),'code':findCodes[2]})
				self.opener.open('http://dontworry.solidwebhost.com/codes.php')
				resp = self.opener.open('http://dontworry.solidwebhost.com/codes.php',store_code_data)
				print "{0} has been added successfully! Re-starting Program\n\n".format(findCodes[1].lower())
				self.loadShows()
		self.chooseShow()

	def fRemove(self, dirtylist, name):
		if dirtylist[1].count(name) > 0:
			for x in range(dirtylist[1].count(name)):
				dirtylist[1].remove(name)
		return dirtylist
		
	def linksOfShow(self):
		dirtylist = []
		resp = self.opener.open('http://www.tv-links.eu/tv-shows/{0}_{1}/season_{2}/episode_{3}/video-results/'.format(self.show,self.showCodes[self.show],self.season,self.episode)).read() 
		print 'http://www.tv-links.eu/tv-shows/{0}_{1}/season_{2}/episode_{3}/video-results/'.format(self.show,self.showCodes[self.show],self.season,self.episode)   
		url = GrabData(resp)
		dirtylist.append(url.Percent())
		dirtylist.append(url.Host())
		dirtylist.append(url.Link())


		dirtylist = self.fRemove(dirtylist, "Apple")
		dirtylist = self.fRemove(dirtylist, "amazon")
		dirtylist = self.fRemove(dirtylist, "blinkbox")
		dirtylist = self.fRemove(dirtylist, "channel4")
		dirtylist = self.fRemove(dirtylist, "abc")
		dirtylist = self.fRemove(dirtylist, "hulu")
		dirtylist = self.fRemove(dirtylist, "comcast")

		num=1
		host = raw_input("Enter a specific host(leave blank to show all): ")
		print "Num   Code     Pct    Host"
		print "--------------------------------"
		for x,y,z in zip(dirtylist[0],dirtylist[1],dirtylist[2]):
			if len(host.strip()) < 1:
				if int(x[:2]) < 50:
					print '\033[1;31m{0}\033[1;m'.format(str(num)+') '+str(x)+' on '+str(y))+Fore.RESET+Style.NORMAL
				else:
					print '\033[1;32m{0}\033[1;m'.format(str(num)+') '+str(x)+' on '+str(y))+Fore.RESET+Style.NORMAL
			elif host in y:
				if int(x[:2]) < 50:
					print '\033[1;31m{0}\033[1;m'.format(str(num)+') '+str(x)+' on '+str(y))+Fore.RESET+Style.NORMAL
				else:
					print '\033[1;32m{0}\033[1;m'.format(str(num)+') '+str(x)+' on '+str(y))+Fore.RESET+Style.NORMAL
			self.listShows.append([str(num)+')',str(x),str(y),str(z)])      
			num+=1

		if len(self.listShows) < 1:
			host = "all"
			print "Unable to find shows. Please check hostname or connection to internet.".format(host)
			raw_input()
			self.chooseShow()
		numberShow = raw_input("\nEnter number: ")
		for x in self.listShows:
			if numberShow+")" in x[0]:
				showCode = self.listShows[int(numberShow)-1][3]
		webbrowser.open("http://www.tv-links.eu/gateway.php?data={0}".format(showCode))
		print "Show has been opened in your web browser. Enjoy!"
		anotherEp = raw_input("Watch another episode?: ").lower()
		if anotherEp == 'y':
			star7t = WatchTV()
		else:
			raw_input()
			
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

	
	def findSeasons(self):
		resp = self.opener.open('http://www.tv-links.eu/tv-shows/{0}_{1}/'.format(self.show,self.showCodes[self.show]))
		seDirty = re.findall(r'(season\_)(\d+)',resp.read())#\W(\w+)\/',resp.read())
		for se in seDirty:
			lastSeason = se[1]
			print se[0], se[1]
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

		
if __name__ == "__main__":
	print "Enjoy watching tv shows free!"
	program = WatchTV()
