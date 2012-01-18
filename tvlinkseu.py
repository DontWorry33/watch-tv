#!/usr/bin/python

import re
import urllib2
import urllib
import cookielib
import webbrowser
import sys


def showEpisodes(showA, showCodesA):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    resp = opener.open('http://www.tv-links.eu/tv-shows/{0}_{1}/'.format(showA,showCodesA[showA]))
    seDirty = re.findall(r'(season\_)(\d+)\W(\w+)\/',resp.read())
    for se in seDirty:
        lastSeason = se[1]
        break
    return int(lastSeason)
        
def findSeasons(showA,showCodesA):
    seasonCount = showEpisodes(showA,showCodesA)
    badchar = '&#039;'
    badchar2 = '&amp;'
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    resp = opener.open('http://www.tv-links.eu/tv-shows/{0}_{1}/'.format(showA,showCodesA[showA]))
    restDirty = re.findall(r'c1\"\>(\w+\s)(\d+)\<\/\w+\>\s\<\w+\s\w+\=\"\w+\"\>([\w+\s\-*\.*\:*\,*\&*\#*\0*\3*\;*]+)',resp.read())
    for restC in restDirty:
        if restC[1] == '0':
            continue
        if restC[1] == '1':
            print "\nSeason",seasonCount,'\n'
            seasonCount-=1
            
        print restC[0]+' '+restC[1],restC[2].replace(badchar,"'").replace(badchar2,"&")

def showDate(showA,showCodesA,season,episode):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    resp = opener.open('http://www.tv-links.eu/tv-shows/{0}_{1}/season_{2}/episode_{3}/'.format(showA,showCodesA[showA],season,episode))
    dates = re.findall(r'(\d+)\W(\d+)\W(\d+)',resp.read())
    for date in dates:
        if date[2] > 2000 and len(date[2]) == 4:
            airDate = date[0]+'/'+date[1]+'/'+date[2]
            break
    print "\nRelease Date: ", airDate


def showSummary(showA,showCodesA,season,episode):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    resp = opener.open('http://www.tv-links.eu/tv-shows/{0}_{1}/season_{2}/episode_{3}/'.format(showA,showCodesA[showA],season,episode))   
    badchar = '&#039;'
    sumShow = "None"
    summary = re.findall(r'(font2\W\W\s)([\w+\s\:*\;*\-*\.*\,*\&*\#*0*3*9*;*]+)',resp.read())
    for x in summary:
        if badchar in x[1]:
            sumShow = x[1].replace(badchar, "'")
        elif badchar not in x[1]:
            sumShow = x[1]
    print "\nSummary of Show: ", sumShow , "\n"

    
def showLinks(showA,showCodesA,season,episode):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    resp = opener.open('http://www.tv-links.eu/tv-shows/{0}_{1}/season_{2}/episode_{3}/'.format(showA,showCodesA[showA],season,episode))
    regFind = re.findall(r'(vers_h\[\d+\])\s\=\s\w+\s\w+\(\W(\w+\W*\W*)\W\W\s\d+\W\s(\d+)\W\s\W(\w+)',resp.read()) #with ==
    return regFind


def addShow(showA,showCodesA):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    showA = showA.replace('-',"+")
    resp = opener.open('http://www.tv-links.eu/_search/?s={0}'.format(showA))
    findShowCode = re.findall(r'(tv\-shows\/)([\w+\-*]+)\_(\d+)',resp.read())
    for findCodes in findShowCode:
        try:
            areYouSure = raw_input("Is {0} the show you want to add (y/n): ".format(findCodes[1].lower()))
            if areYouSure == 'y':
                if showCodesA[findCodes[1].lower()]:
                    print "Show in database with name: ",findCodes[1].lower().replace('-',' ')
                    break
                store_code_data = urllib.urlencode({'show':findCodes[1].lower(),'code':findCodes[2]})
                opener.open('http://legacylogin.zzl.org/codes.php')
                resp = opener.open('http://legacylogin.zzl.org/codes.php',store_code_data)
                print "{0} has been added successfully! Re-starting Program\n\n".format(findCodes[1].lower())
            else:
                print "Show not added"
                break
            main()
        except:
            store_code_data = urllib.urlencode({'show':findCodes[1].lower(),'code':findCodes[2]})
            opener.open('http://legacylogin.zzl.org/codes.php')
            resp = opener.open('http://legacylogin.zzl.org/codes.php',store_code_data)
            print "{0} has been added successfully! Re-starting Program\n\n".format(findCodes[1].lower())
            break
    main()


def main():
    showCodes = {}
    websiteCodes = urllib2.urlopen('http://legacylogin.zzl.org/codesList.txt')
    for indCode in websiteCodes:
        relink = indCode.split(':')
        showCodes[relink[0]]=relink[1].replace('\n','')
    #print showCodes
    show = raw_input("Enter a TV show: ").lower()
    if show == 'delete':
        print showCodes
        deleteShow = raw_input("What show do you want to delete?: ")
        try:
            del(showCodes[deleteShow])
            print "Show deleted"
            main()
        except:
            print "Unable to find show."
            main()
    show = show.replace(' ','-')
    show = show.replace("'",'-')
    try:
        showCodes[show]
    except:
        try:
            showCodes['the-'+show]
            show = 'the-'+show
        except:
            try:
                showCodes[show+'-']
                show = show+'-'
            except:
                try:
                    showCodes['the-'+show+'-']
                    show = 'the-'+show+'-'
                except:
                    addShow(show,showCodes)
                    print "kk"
                    sys.exit(1)
    again(show,showCodes)


def again(showA,showCodesA):
    num=0
    listShows = []
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    print "Watch {0} free!".format(showA)
    print '\n\n'
    findSeasons(showA,showCodesA)
    print '\n\n'
    season=int(raw_input("Season: "))
    episode = int(raw_input("Episode: "))
    resp = opener.open('http://www.tv-links.eu/tv-shows/{0}_{1}/season_{2}/episode_{3}/'.format(showA,showCodesA[showA],season,episode))
    showDate(showA,showCodesA,season,episode)
    showSummary(showA,showCodesA,season,episode)
    dirtyList = showLinks(showA,showCodesA,season,episode)
    host = raw_input("Enter a specific host(leave blank to show all): ")
    print "Num   Code     Pct    Host"
    print "--------------------------------"
    for link in dirtyList:
        if len(host.strip()) < 1:
            num+=1
            print str(num)+")",link[1],link[2],link[3]
            listShows.append([str(num)+")",link[1],str(link[2])+"%",link[3]])
        elif host in link[3]:
            num+=1
            print str(num)+")",link[1],str(link[2])+"%",link[3]
            listShows.append([str(num)+")",link[1],str(link[2])+"%",link[3]])
    if len(listShows) < 1:
        print "Unable to find shows with {0} as the host".format(host)
        raw_input()
        sys.exit(1)
    numberShow = raw_input("Enter number: ")
    
    for x in listShows:
        if numberShow+")" in x[0]:
            showCode = listShows[int(numberShow)-1][1]
            
    webbrowser.open("http://www.tv-links.eu/gateway.php?data={0}".format(showCode))
    print "Show has been opened in your web browser. Enjoy!"
    anotherEp = raw_input("Watch another episode?: ").lower()
    if anotherEp == 'y':
        again(showA,showCodesA)
    else:
        raw_input()

if __name__ == "__main__":
    print "Enjoy watching tv shows free!"
    main()
