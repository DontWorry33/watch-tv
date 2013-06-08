#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import time
import pickle
import glob

from DownloadEpisodes import *
from loadingbar import *

class EpisodeOptions:
	def __init__(self, showDict, show):
		self.showDict = showDict
		self.show = show
		self.pBar = LoadingLabel(("Downloading", "Downloading.", "Downloading..", "Downloading...", "Downloading...."), "Complete!")

		
	def episodePortal(self):
		try:
			for k in self.showDict.keys():
				if os.path.exists('data/'+k+'.txt'):
					'''
					downloadList = raw_input("Episode titles are downloaded. Would you like to update the list (y/n): " )
					if downloadList.lower() == 'y':
						self.gatherEpisodes()
					else:
					'''
					return True
				else:
					break
			downloadList = raw_input("Would you like to download a list of episode titles from the database to improve speed (y/n): ")
			if downloadList.lower() == 'y':
				self.gatherEpisodes()
			else:
				return False
		except Exception as e:
			print e, type(e)
			downloadList = raw_input("This shows episode titles have not been downloaded (must be new), would you like to update it now (y/n): ")
			if downloadList.lower() == 'y':
				self.gatherEpisodesIndividually()
			else:
				return False
			
	def chooseEpisode(self):
		try:
			epList = pickle.load(open('data/'+self.show+'.txt','r'))
			for x in epList:
				print x
			self.season=int(raw_input("Season: "))
			self.episode = int(raw_input("Episode: "))
			return self.season, self.episode
		except EOFError:
			print "Exiting program, please restart"
			raw_input();
			sys.exit()
		except:
			print e
			print "Missing episode list. Downloading now"
			self.gatherEpisodesIndividually()
			sys.exit()


	def gatherEpisodes(self):
		#print "Files are saving in data folder. Do press keys until program closes. Restart when done.\n"                       
		temp = SplitDict(self.showDict)
		dict1, dict2 = temp.split()
		try:
			worker1 = Worker(dict1, self.pBar)
			worker2 = Worker(dict2, self.pBar)
			worker1.start()
			worker2.start()
			while True:
				tmp = len(glob.glob(os.path.abspath('data/*')))
				if tmp == len(self.showDict):
					self.pBar.close()
					print "Done?"
					break
		except Exception as e:
			print '\n\n\n\n\n\n\n'
			print e
			sys.exit(0)
			
	def gatherEpisodesIndividually(self):
		if os.path.exists('data/'+self.show+'.txt'):
			print 'Data corrupt, please update episodes'
		else:
			tempworker=Worker({self.show:self.showDict[self.show]},self.pBar )
			tempworker.start()
			while True:
				tmp = len(glob.glob(os.path.abspath('data/*')))
				if tmp == len(self.showDict):
					time.sleep(1)
					raw_input("Press enter to close program")
					break

if __name__ == "__main__":
	print "ERROR: THIS IS A MODULE. PLEASE RUN tvlinkseu4.py"
