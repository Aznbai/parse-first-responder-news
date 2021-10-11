import requests
from bs4 import BeautifulSoup
import random
import time
from time import sleep 
import datetime
import keyboard


URL = "https://www.presseportal.de/text/polizei"
requestIntervalMain=300
requestIntervalMin=1
requestIntervalMax=3
storyBufferSize=10
storyNumber=10 # numberof stories to load per scrap
selected = 1
now= datetime.datetime.now()
requestNextTime= now+ + datetime.timedelta(0,requestIntervalMain)



def randomSleep(minSeconds, maxSeconds):
    sleeptime = round(random.uniform(minSeconds, maxSeconds), 3)
    print("waiting", end="")
    sleep(0.05)
    for x in range(30):
        print(".", end="")
        sleep(0.2)
    print("")
    print("-------------------------------")
    print("sceduling next request in: ", sleeptime, " seconds")
    print("-------------------------------")
    sleep(sleeptime)
def updateTeaserPage():
    global story_titles
    global story_title_urls
    global story_teasers
    teaserPage = requests.get(URL)    ##load teasers of last stories
    soup = BeautifulSoup(teaserPage.content, "html.parser")
    resultsTeaser = soup.find(id="storylist")
    ##parse teaser story headlines
    story_titles= resultsTeaser.find_all("div", class_="storylist_title")
    for idx, story_title in enumerate(story_titles):
        story_titles[idx] = story_title.find("a").text.strip()
    ##parse teaser story links
    story_title_urls= resultsTeaser.find_all("div", class_="storylist_title")
    for idx, story_title_url in enumerate(story_title_urls):
        story_title_urls[idx] = "https://www.presseportal.de"+story_title_url.find("a")['href']
    ##parse teaser story teasers
    story_teasers = resultsTeaser.find_all("div", class_="storylist_teaser")
    for idx, story_teaser in enumerate(story_teasers):
        story_teasers[idx] = story_teaser.text.strip()
    ##print all teasers
    for idx, story_title in enumerate(story_titles):
        print("-------------------------------")
        print(story_titles[idx], sep = "\n")
        print(story_teasers[idx], sep = "\n")
        print(story_title_urls[idx], sep = "\n")
    ##load full text of the last story
    print("-------------------------------")
    print("loading after full version of the most recent story after timeout")
    print("-------------------------------")
    randomSleep(2,5)
    fullStoryPageURL = story_title_urls[0]
    fullStoryPage = requests.get(fullStoryPageURL)
    soupFullStory = BeautifulSoup(fullStoryPage.content, "html.parser")
    resultsFullStory = soupFullStory.find(id="story")
    
    fullStoryTitle = resultsFullStory.find("h1").text.strip()
    fullStoryParagraphs = resultsFullStory.find_all("p")
    fullStoryParagraphs.pop()
    fullStoryParagraphs.pop()
    fullStoryText=""
    for idx, fullStoryParagraph in enumerate(fullStoryParagraphs):
        fullStoryText = fullStoryText+fullStoryParagraph.text.strip()+ "\n"
    ##print full text of the last story
    print("-------------------------------")
    print(fullStoryTitle, sep = "\n \n")
    print(fullStoryText, sep = "\n")
    print("-------------------------------")
    show_menu()
def printStatus():
    print("________________________________________________________")
    print("STATUS REPORT")
    print("SOURCE URL:               " + URL)
    print("BUFFER SIZE:               " + str(storyBufferSize)+" STORIES")
    print("MAIN REQUEST INTERVAL:    " + str(requestIntervalMain) +" SECONDS")
    print("MAX REQUEST FREQUENCY:    " + str(requestIntervalMin)+" SECONDS")
    print("MIN REQUEST FREQUENCY:    " + str(requestIntervalMax) + " SECONDS")
    print("CURRENT TIME:             " + str(now.time()))
    print("NEXT SCHEDULED REQUEST:   " + str(requestNextTime.time()))
    print("________________________________________________________")
    show_menu()
def printTeaserLinks():
    print("-------------------------------")
    for idx, story_title in enumerate(story_titles):
        print(story_title_urls[idx], sep = "\n")
    print("-------------------------------")
    show_menu()
def printTeasers():
    for idx, story_title in enumerate(story_titles):
        print("-------------------------------")
        print(story_titles[idx], sep = "\n")
        print("\n")
        print(story_teasers[idx], sep = "\n")
        print("\n")
    show_menu()
def up():
    global selected
    if selected == 1:
        return
    selected -= 1
    show_menu()

def down():
    global selected
    if selected == 4:
        return
    selected += 1
    show_menu()
##will run forever
##while True:
##updateTeaserPage()
##randomSleep(5,10)    
def show_menu():
    global selected
    print("________________________________________________________")
    print("Choose an option:")
    print("1. REPRINT STATUS")
    print("2. RELOAD FULL STORIES")
    print("3. PRINT CURRENT TEASERS")
    print("4. PRINT CURRENT TEASER LINKS")    
    print("5. DECREASE MAIN REQUEST INTERVAL")
    print("6. INCREASE MAIN REQUEST INTERVAL")
    print("6. INCREASE MAIN REQUEST INTERVAL")
    print("0. RELOAD EVERYTHING AND START")
    print("________________________________________________________")
    
while True:  # infinite execution loop
    show_menu()
    keyboard.add_hotkey('0', updateTeaserPage)
    keyboard.add_hotkey('1', printStatus)
##    keyboard.add_hotkey('2', two)
    keyboard.add_hotkey('3', printTeasers)
    keyboard.add_hotkey('4', printTeaserLinks)
    keyboard.add_hotkey('up', up)
    keyboard.add_hotkey('down', down)
    keyboard.wait()
