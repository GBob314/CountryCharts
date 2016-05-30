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

satList = []
for sat in allSaturdays(1995):
	satList.append(sat)

for sat in satList:
	print sat

response = urllib2.urlopen(make_url("1995-01-28"))
page_source = response.read().split('\n')
weekList = pull_song_data(page_source)
songCount = 0
for song in weekList:
	songCount += 1
	print str(songCount) + ": " + song