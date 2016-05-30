import re
import urllib2
from datetime import date, timedelta

base_url = "http://www.billboard.com/charts/country-songs/"

def make_url(URLDate):
    return base_url + URLDate
	
#gives all saturdays for a year
def allSaturdays(year):
	d = date(year, 1, 1)
	d += timedelta(days = (5 - d.weekday() + 7) % 7)
	while d.year == year:
		yield d
		d += timedelta(days = 7)
	
#SONG NAME <h2 class="chart-row__song">Change Of Heart</h2>
#ARTIST NAME <a class="chart-row__artist" href="http://www.billboard.com/artist/418089/judds" data-tracklabel="Artist Name">
#                               The Judds
def pull_song_data(page_source):
	lineNumber = 0
	songList = []
	for line in page_source:
		try:
			regSearch1 = re.search('(<h2 class="chart-row__song">)(.+)(</h2>)',line)
			song = regSearch1.group(2) + " - " + page_source[lineNumber + 2].lstrip()
			songList.append(song)
		except AttributeError:
			pass
		lineNumber += 1
	return songList

#Gets the year for user input and returns a list of every Saturday for that year.	
def getYear():
	year = 0
	year = input("Please enter a year: ")
	satList = []
	for sat in allSaturdays(year):
		satList.append(sat)
	return satList

#gets the chart for the specified week	
def getWeekChart(date):
	response = urllib2.urlopen(make_url(str(date)))
	page_source = response.read().split('\n')
	weekList = pull_song_data(page_source)
	return weekList

#prints the chart for the specified week
def printChart(chartList):
	songPosition = 1
	print "Position #\tSong"
	for song in chartList:
		print str(songPosition) + "\t" + song
		songPosition += 1

yearList = getYear()

printChart(getWeekChart(yearList[0]))
print "\n" + str(yearList[0])