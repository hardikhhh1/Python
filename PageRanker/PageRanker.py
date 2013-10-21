#Created By: Hardik Arora
#Date : 10/21/2013
#This is page ranker program, which takes inlink pages as an argument
#calculates the page ranks according to the pageranker algorithm


#imports
from __future__ import print_function
import os
import sys
import re
import math
import operator

TotalPages =[]
#Total Pages in the file.

perplexityList = []

inLinks = {}
# inLinks[k] would be the set of pages that link to page k


outLinks = {}
# outLinks(q) is the number of out-links from page q

SinkPages = []
# sinkPages is the list of all the sink pages , that is, the pages which do 
# not have any outlinks.



PageRank = {}
#page ranks of all the pages 
newPageRank = {}

#os.chdir(os.path.dirname(sys.argv[0]))


#file address

TEXTFILENAME = sys.argv[1]
#The text File to read links from

lines = []
# Text of the text file.

DAMPINGFACTOR = 0.85

def textReader():
    textFile = open(TEXTFILENAME,"r")
    x = 0 
    for l in textFile:
        x += 1
        lines.append(l.rstrip('\n'))        
    

# adds the name of the page in the list of the total pages.
def pageToListAdder():
    for line in lines:
        line = line.rstrip()
        link = line.split()
        inlinksAdder(link)
        outlinksAdder(link)
        TotalPages.append(link[0])
    
# add inlinks pointing to the page in the inlinks dictionary    
def inlinksAdder(linkLine):
    
    root = linkLine[0]
    if linkLine[1:]:
        tempList = []
        for each in linkLine[1:]:
            if not (each == '\n'):
                tempList.append(each)
        inLinks[root] = tempList
      
    
# add outlinks pointing to the page in the outlinks dictionary    
def outlinksAdder(linkLine):
    root = linkLine[0]
    if linkLine[1:]:
        for link in linkLine[1:]:
            outlink = outLinks.get(link)
            if not outlink:
                outLinks[link] = [root]
            elif outlink not in SinkPages:
                tempLink = []
                for each in outlink:
                    tempLink.append(each)
                tempLink.append(root)
                outLinks[link] = tempLink
                
                   
def pageRankerAlgo():
    #Applies the page ranker algorithm to the sets.
    global PageRank
    noPages = len(TotalPages)
    if not PageRank:
        for page in TotalPages:
            PageRank[page] = 1/noPages
    while not convergenceChecker():
        sinkPR = 0
        for page in SinkPages:
            sinkPR += PageRank[page]
        for page in TotalPages:
            newPageRank[page] = (1 - DAMPINGFACTOR)/noPages
            newPageRank[page] += (DAMPINGFACTOR * sinkPR)/noPages
            if page in inLinks:
                for p in inLinks[page]:
                    if '\n' in p:
                        p = p.rstrip('\n')
                    newPageRank[page] += (DAMPINGFACTOR * PageRank[p])/ len(outLinks[p])
        for pge in TotalPages:
            PageRank[pge] = newPageRank[pge]
        
                
                 
 
def convergenceChecker():
    #finds the perplexity of the pages
    global perplexityList
    H_x = 0
    temp = 0
    for each in TotalPages:
        temp += (PageRank[each] * 
                 math.log(PageRank[each] ,2))
    h_x = -temp
    perplexity = math.pow(2,h_x)
    print(perplexity)
    perplexityList.append(perplexity)
    return listChecker()
               
def listChecker():
    #checks if the list have converged, where converged can be said if the
    #last four pages have difference of 1 or less than 1
    global perplexityList
    if not perplexityList:
        return False
    else:
        if(len(perplexityList) > 4):
            perplexityList = perplexityList[1:]
            a = perplexityList[0]
            b = perplexityList[1]
            c = perplexityList[2]
            d = perplexityList[3]
            if(((a-b) <= 1) and ((b-c) <= 1) and ((c-d) <= 1)):
#                 print('a : ')
#                 print(a)
#                 print('b : ')
#                 print(b)
#                 print('c : ')
#                 print(c)
#                 print('d : ')
#                 print(d)
                return True
           
        
def subtractDictionaries(dict1,dict2):
    res = []
    for key in dict1:
        if key not in dict2:
            res.append(key)
    
    return res        
    
    
            

textReader()
pageToListAdder()
SinkPages = subtractDictionaries(TotalPages,outLinks)
pageRankerAlgo()

print('total pages : ',len(TotalPages))
print('in links : ',len(inLinks))
print(len(outLinks))
print('Sink pages',len(SinkPages))
sorted_pageRank = sorted(PageRank.items(), key=lambda x: x[1], reverse = True)
sorted_inLinks = sorted(inLinks,key = lambda x : len(inLinks[x]), reverse = True)

print('TOP 50 PAGES ACCORDING TO PAGE RANKS')
x = 1 
while(x < 51):
    print(str(x) + ' : ' + str(sorted_pageRank[(x-1)]))
    x += 1
x = 1
print('TOP 50 PAGES ACCORDING TO PAGE INLINKS')
while(x < 51):
    print(str(x) + ' : ' + str([sorted_inLinks[(x-1)]]) + "   InLinks Count     : " + str(len(inLinks[sorted_inLinks[(x-1)]])))
    x += 1
    
    






     
     
     
     
     
     
     
     
            




