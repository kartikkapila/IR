import urllib2
import re
import sys
from urlparse import urljoin
from bs4 import BeautifulSoup



###### INITIALIZATION ######
frontier = []
explored_set = []
depth = 0
seed = sys.argv[1]
base_url = seed
if len(sys.argv) > 2 :
	keyPhrase = sys.argv[2]
else :
	keyPhrase = ""

frontier.append((seed,0))
###### END INITIALIZATION #####

def isValidUrl(url) :
	return re.match('^/wiki/(?!Main_Page)(?!.*:)', unicode(url))

def findAbsolutePath(relative_path) :
	return urljoin(base_url,relative_path)

def notInFrontier(absolute_path) :
	for element in frontier :
		if element[0] == absolute_path :
			return False
	return True

def findChildren(soup,depth) :
	for anchor in soup.find_all('a') :
		relative_path = anchor.get('href')	
		if isValidUrl(relative_path) :
			absolute_path = findAbsolutePath(relative_path)
			candidate = (absolute_path,depth)
			if notInFrontier(absolute_path) and absolute_path not in explored_set and depth <= 2 :
				frontier.append(candidate)

while len(frontier) != 0 :
	leaf_node = frontier.pop(0)
	print '**********'
	print leaf_node
	print '**********'
	explored_set.append(leaf_node[0])
	soup = BeautifulSoup(urllib2.urlopen(leaf_node[0]).read())
	findChildren(soup,leaf_node[1] + 1)

print explored_set
