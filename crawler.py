import urllib2
import re
import sys
from urlparse import urljoin
from bs4 import BeautifulSoup
from sets import Set
import time

start_time = time.time()
###### INITIALIZATION ######
frontier = []
explored_set = []
common_set = Set()
depth = 0
seed = sys.argv[1]
base_url = seed
if len(sys.argv) > 2 :
	keyPhrase = sys.argv[2]
	keyPhrase = keyPhrase.lower()
else :
	keyPhrase = ""

frontier.append((seed,0))
###### END INITIALIZATION #####

def isValidUrl(url) :
	return re.match('^/wiki/(?!Main_Page)(?!.*:)', unicode(url))

def findAbsolutePath(relative_path) :
	return urljoin(base_url,relative_path)

def checkRedirect(candidate) :
	print candidate.getcode()
	soup = BeautifulSoup(candidate.read())
	links = soup.find_all('link')
	for link in links:
		if "canonical" == link.get('rel'):
			print "canonical"
		else :
			print "nope"
	return
	
def isKeyPhrasePresent(soup, absolute_path) :
	if keyPhrase == "" :
		return True
	candidate = urllib2.urlopen(absolute_path)
	if absolute_path == "http://en.wikipedia.org/wiki/Computer_Science" : 
		checkRedirect(candidate)
#	checkRedirect(candidate)
	soup = BeautifulSoup(candidate.read())
	text = soup.get_text().lower()
	if keyPhrase in text :
		return True
	return False

def removeHash(relative_path) :
	if relative_path.find('#') != -1 :
		index = relative_path.index('#')
		return relative_path[0 : index]
	return relative_path

def findChildren(soup,depth) :
	for anchor in soup.find_all('a') :
		relative_path = anchor.get('href')	
		if isValidUrl(relative_path) :
			relative_path = removeHash(str(relative_path))
			absolute_path = findAbsolutePath(relative_path)
			candidate = (absolute_path,depth)
			if depth <= 2 and absolute_path not in common_set and isKeyPhrasePresent(soup, absolute_path) :
				frontier.append(candidate)
				common_set.add(absolute_path)

while len(frontier) != 0 :
	leaf_node = frontier.pop(0)	
	print leaf_node[0]
	if leaf_node[1] + 1 > 2:
		explored_set.append(leaf_node[0])
		break
	explored_set.append(leaf_node[0])
	common_set.add(leaf_node[0])
	soup = BeautifulSoup(urllib2.urlopen(leaf_node[0]).read())
	findChildren(soup,leaf_node[1] + 1)

for f in frontier :
	explored_set.append(f[0])

output = open('output.txt','w')
count = 0
for item in explored_set: 
	count += 1
	output.write(item)
	output.write('\n')

output.write('Some Additional Information \n')
output.write("Time Taken:" + str(time.time() - start_time) + "\n")
output.write("No of Links:" + str(count))
output.close()
