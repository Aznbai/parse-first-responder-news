import os
import sys
import requests
from bs4 import BeautifulSoup
import re
import random
from time import sleep
sys.path.append( '../' )
from PyRTF import *
from PyRTF.Elements import Document, Renderer, Section
from PyRTF.document.paragraph import Paragraph
from PyRTF.document.character import TEXT
#
URL = "https://www.presseportal.de/text/polizei"
freshIDs=[] #all ids recieved from last request
knownIDs=[] #known since start / first request
newFilteredIDs=[] #new, unprinted ids from last request

#
def randomSleep(minSeconds, maxSeconds):
    sleeptime = round(random.uniform(minSeconds, maxSeconds), 3)
    progressDots=50
    print("RANDOM TIMEOUT. \nNEXT STEP IN: ", sleeptime, " seconds")
    for x in range(progressDots):
        print("_", end="")
    print("")
    sleeptime=sleeptime/progressDots
    for x in range(progressDots):
        print(".", end="")
        sleep(sleeptime)
    print("\n")
#
def getFreshIDs():
    global freshIDs
    idsPage = requests.get(URL)
    print("GOT NEW IDs FROM: \n" + URL + "\n")
    soup = BeautifulSoup(idsPage.content, "html.parser")
    resultsTeaser = soup.find(id="storylist")
    newIDs = resultsTeaser.find_all("div", class_="storylist_title")
    ##  print(newIDs)
    for idx, newID in enumerate(newIDs):
        newIDs[idx] = newID.find("a")['href']
##        print(newIDs[idx])
        newID = re.findall('\d+', newIDs[idx])
        newIDs[idx]=newID[0]
    newIDs.reverse()
    print(newIDs)
    freshIDs = newIDs.copy()
    print(freshIDs)

#
def initKnownIDs():
    global freshIDs
    global knownIDs
    knownIDs = freshIDs.copy()
    knownIDs.pop()
    knownIDs.pop()
##    print("freshIDs")
##    print(type(freshIDs))
##    print(freshIDs)
##    print("knownIDs")
##    print(type(knownIDs))
##    print(knownIDs)
#
def filterKnownUnknownIDs():
    global freshIDs
    global knownIDs
    global newFilteredIDs
    newAmount = 0
    lastKnownID = knownIDs[-1]
    for freshID in reversed(freshIDs):
        if freshID == lastKnownID:
            break
        newAmount=newAmount+1
    print("FOUND " + str(newAmount) + " NEW STORY IDs SINCE LAST UPDATE")
    for i in range(newAmount):
        reverseIndex=i * ( -1 ) -1
        newFilteredIDs.insert(0, freshIDs[reverseIndex])
    knownIDs.extend(newFilteredIDs)
#
def makeRtfNote(headingString, fullStoryParagraphs):
    doc = Document()
    ss = doc.StyleSheet
    section = Section()
    doc.Sections.append(section)
    #
    p = Paragraph( ss.ParagraphStyles.Heading1 )
    p.append( headingString )
    section.append( p )
    #
    fullStoryText = ""
    for idx, fullStoryParagraph in enumerate(fullStoryParagraphs):
        p = Paragraph( ss.ParagraphStyles.Normal )
        p.append(TEXT(fullStoryParagraph.text.strip(), size=18) )
        section.append( p )
        p.append(TEXT(' ', size=18) )
    p.append(TEXT(' ', size=18))
    return doc
#
def printConsoleFullStoryParagraphs(fullStoryTitle, fullStoryParagraphs):
    fullStoryText=""
    for idx, fullStoryParagraph in enumerate(fullStoryParagraphs):
        fullStoryText = fullStoryText+fullStoryParagraph.text.strip()+ "\n \n"
    ##print full text of the last story
    print("-------------------------------")
    print(fullStoryTitle, sep = "\n \n")
    print(fullStoryText, sep = "\n")
    print("-------------------------------")
#
def OpenFile(fileName):
    return open('%s.rtf' % fileName, 'w')
#
def printPosFullStoryPagagraphs(fullStoryTitle, fullStoryParagraphs, fullStoryFileName):
    DR = Renderer()
    doc1 = makeRtfNote(fullStoryTitle,fullStoryParagraphs)
    DR.Write(doc1, OpenFile(fullStoryFileName))
    print("RTF Finished")
    cmdString='cmd /c "write /p '+ str(fullStoryFileName)+'.rtf"'
    os.system(cmdString)
#
def loadOneFullStory(storyID):
    ##load full text of the last story
    fullStoryPageURL = "https://www.presseportal.de/text/p_story.htx?nr="+storyID
    fullStoryPage = requests.get(fullStoryPageURL)
    soupFullStory = BeautifulSoup(fullStoryPage.content, "html.parser")
    for e in soupFullStory.findAll('br'):
        e.replace_with(' ')
    resultsFullStory = soupFullStory.find(id="story")
    fullStoryTitle = resultsFullStory.find("h1").text.strip()
    fullStoryParagraphs = resultsFullStory.find_all("p")
    printConsoleFullStoryParagraphs(fullStoryTitle,fullStoryParagraphs)    
    printPosFullStoryPagagraphs(fullStoryTitle,fullStoryParagraphs,storyID)
def printReduceNewFilteredIDs():
    global newFilteredIDs
    for newFilteredID in newFilteredIDs:
        randomSleep(3,8)
        loadOneFullStory(newFilteredID)
    newFilteredIDs=[]
 
#
getFreshIDs()
initKnownIDs()
filterKnownUnknownIDs()
printReduceNewFilteredIDs()
while True:
    randomSleep(300,600)
    getFreshIDs()
    filterKnownUnknownIDs()
    printReduceNewFilteredIDs()

    

