import urllib2
import re
import sys
from urlparse import urljoin
from bs4 import BeautifulSoup
from sets import Set
import time

###### INITIALIZATION ######
frontier = []
explored_set = []
common_set = Set()
answer = []
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

def urlQuery(absolute_path) :
	retry_attempt = 1.0
	while retry_attempt != 5 :
       		try :
			time.sleep(retry_attempt)
			candidate = urllib2.urlopen(absolute_path)
			if candidate is not None :
				return candidate
		except IOError as e:
			print "Something went wrong. lets try fetching  again."
			retry_attempt += 1	
	print "Request cannot be completed"

def readUrl(candidate) :
	handler  = candidate.read()
	return handler
	
def isValidUrl(url) :
        return re.match('^/wiki/(?!Main_Page)(?!.*:)', unicode(url))

def findAbsolutePath(relative_path) :
        return str(urljoin(base_url,relative_path))

def getCanonicalUrl(candidate, absolute_path) :
        soup = BeautifulSoup(readUrl(candidate))
        links = soup.find_all('link')
        for link in links:
                if "canonical" in link.get('rel') :
                        return str(link.get('href'))
	
        return absolute_path


def isKeyPhrasePresent(soup, absolute_path) :
        if keyPhrase == "" :
                return True
        candidate = urlQuery(absolute_path)
        soup = BeautifulSoup(readUrl(candidate))
        text = soup.get_text().lower()
        if keyPhrase in text :
                return True
        explored_set.append(absolute_path)
        common_set.add(absolute_path)
        return False

def removeHash(relative_path) :
        if relative_path.find('#') != -1 :
                index = relative_path.index('#')
                return relative_path[0 : index]
        return relative_path

def validateNewUrl(absolute_path) :
        if absolute_path not in common_set :
                return True
        return False

def addToFrontier(absolute_path, depth) :
        candidate = (absolute_path, depth)
        frontier.append(candidate)
        common_set.add(absolute_path)

def checkPathsAndAddToFrontier(maybe_new_absolute_path, absolute_path, depth) :
	if maybe_new_absolute_path != absolute_path :
		absolute_path = maybe_new_absolute_path	
                if validateNewUrl(absolute_path) :
 	               addToFrontier(absolute_path, depth)
        elif maybe_new_absolute_path not in common_set :
        	 addToFrontier(absolute_path, depth)

def getRedirectedUrlifRedirected(candidate, absolute_path) :
	if str(candidate.getcode()) == "302" or str(candidate.getcode() == '301'):
		return str(candidate.geturl())
	else :
		return absolute_path	

def findChildren(soup,depth) :
        for anchor in soup.find_all('a') :
                relative_path = anchor.get('href')
                if isValidUrl(relative_path) :
                        relative_path = removeHash(str(relative_path))
                        absolute_path = findAbsolutePath(relative_path)
                        if depth <= 2 and absolute_path not in common_set and isKeyPhrasePresent(soup, absolute_path) :
				candidate = urlQuery(absolute_path)
				redirectedUrl = getRedirectedUrlifRedirected(candidate, absolute_path)
				if redirectedUrl != absolute_path:
                                	maybe_new_absolute_path = getCanonicalUrl(candidate, redirectedUrl)
					checkPathsAndAddToFrontier(maybe_new_absolute_path, redirectedUrl, depth)
				else :
                                	maybe_new_absolute_path = getCanonicalUrl(candidate, absolute_path)
					checkPathsAndAddToFrontier(maybe_new_absolute_path, absolute_path, depth)
					
def main() :
	while len(frontier) != 0 :
        	leaf_node = frontier.pop(0)
        	answer.append(leaf_node[0])
        	if leaf_node[1] + 1 > 2:
               		explored_set.append(leaf_node[0])
                	break
        	explored_set.append(leaf_node[0])
        	common_set.add(leaf_node[0])
        	candidate = urlQuery(leaf_node[0])
        	soup = BeautifulSoup(readUrl(candidate))
        	findChildren(soup,leaf_node[1] + 1)

	for f in frontier :
		candidate = urlQuery(f[0])
        	maybe_new_absolute_path = getCanonicalUrl(candidate, f[0])
                if maybe_new_absolute_path != f[0] :
			answer.append(maybe_new_absolute_path)
		else :
       			answer.append(f[0])
	
	if keyPhrase != "" :
		output = open('focusedCrawl.txt','w')
	else :
		output = open('unfocusedCrawl.txt','w')
	count = 0
	for item in answer:
		count += 1
        	output.write(item)
        	output.write('\n')
	if keyPhrase != "" :
		output.write("Proportion:" + str(count/float(len(common_set))))
	output.close()

soup = BeautifulSoup(urllib2.urlopen(seed).read())
text = soup.get_text().lower()
if keyPhrase != "" :
	if keyPhrase in text :
		main()
	else :
		output = open('focusedCrawlWithNoOutput.txt','w')
		output.write("")
		output.close()
else :
	main()
