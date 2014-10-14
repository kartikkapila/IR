import sys
input_file = open("wt2g_inlinks.txt","r")
page_rank_file = open("sortedPageRank.txt","r")
input_page = sys.argv[1]

print "Page" + " " + str(input_page)
print "***********"

for line in page_rank_file :
	newLine = line.split()
	if newLine.pop(0) == input_page :
		print "Page Rank" + " " + str(newLine.pop(0))

page_rank_file.close()
page_rank_file = open("sortedPageRank.txt","r")
inLinkCount = 0
outLinkCount = 0
outLinkPages = []
inLinkPagesInTop50List = []
noOfPagesInTop50Count = 0

def inLinkPagesInTop50(newLine) :
	global noOfPagesInTop50Count
	count = 0
	for line in page_rank_file :
		if count == 50000 :
			break
		page = line.split().pop(0)
		if page in newLine :
			noOfPagesInTop50Count += 1
			inLinkPagesInTop50List.append(page)
		count += 1

for line in input_file : 
	newLine = line.split()
	page = newLine.pop(0)
	if page == input_page :
		inLinkCount = len(newLine)
		inLinkPagesInTop50(newLine)
	elif input_page in newLine:
		outLinkCount += newLine.count(input_page)		
		outLinkPages.append(page)

print "***********"
print "In link count:" + str(inLinkCount)
print "In Link Pages in top 50:" + str(noOfPagesInTop50Count)
print "Out link count:" + str(outLinkCount)
print "Out link Pages:"
for page in outLinkPages :
	print page
print "In Link Pages in top 50"
for page in inLinkPagesInTop50List :
	print page
