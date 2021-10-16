import requests
from bs4 import BeautifulSoup
import re
import random
from time import sleep
URL = "https://www.presseportal.de/text/polizei"
lastKnownID=""
newDifferingIDs={}
freshIDs=[]
knownIDs=[]
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
    idsPage = requests.get(URL)
    print("GOT NEW IDs FROM: \n" + URL + "\n")
    soup = BeautifulSoup(idsPage.content, "html.parser")
    resultsTeaser = soup.find(id="storylist")
    newIDs = resultsTeaser.find_all("div", class_="storylist_title")
    ##  print(newIDs)
    for idx, newID in enumerate(newIDs):
        newIDs[idx] = newID.find("a")['href']
        print(newIDs[idx])
        newID = re.findall('\d+', newIDs[idx])
        newIDs[idx]=newID[0]
    newIDs.reverse()
    return newIDs
#
def initKnownIDs():
    global freshIDs
    global knownIDs
    freshIDs = getFreshIDs()
    knownIDs = freshIDs.copy()
    knownIDs.pop()
    knownIDs.pop()
    knownIDs.pop()
    knownIDs.pop()
    knownIDs.pop()
    lastKnownID = knownIDs[-1]
##    print("freshIDs")
##    print(type(freshIDs))
##    print(freshIDs)
##    print("knownIDs")
##    print(type(knownIDs))
##    print(knownIDs)
#
def updateKnownIDs():
    global freshIDs
    global knownIDs
    newAmount=0
    lastKnownID = knownIDs[-1]
    for freshID in reversed(freshIDs):
        if freshID == lastKnownID:
            break
        newAmount=newAmount+1
    print("newAmount")
    print(newAmount)
    newFilteredIDs=[]
    for i in range(newAmount):
        reverseIndex=i*(-1)-1
        newFilteredIDs.insert(0, freshIDs[reverseIndex])
    knownIDs.extend(newFilteredIDs)   
#
initKnownIDs()
updateKnownIDs()

