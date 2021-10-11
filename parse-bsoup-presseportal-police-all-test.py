import requests
from bs4 import BeautifulSoup

import random
from time import sleep
URL = "https://www.presseportal.de/text/polizei"
story_titles=""

def randomSleep(minSeconds, maxSeconds):
    sleeptime = round(random.uniform(minSeconds, maxSeconds), 3)
    print("waiting", end="")
    sleep(0.2)
    for x in range(10):
        print(".", end="")
        sleep(0.2)
    print("")
    print("-------------------------------")
    print("sceduling next request in: ", sleeptime, " seconds")
    print("-------------------------------")
    sleep(sleeptime)
        
        
def updateTeaserPage():
    ##load teasers of last stories
    teaserPage = requests.get(URL)
    print("-------------------------------")
    print("teaser story data succesfully loaded from: \n" + URL)
    print("-------------------------------")

    soup = BeautifulSoup(teaserPage.content, "html.parser")
    resultsTeaser = soup.find(id="storylist")

    ##parse teaser story headlines
    story_titles = resultsTeaser.find_all("div", class_="storylist_title")
    for idx, story_title in enumerate(story_titles):
        story_titles[idx] = story_title.find("a").text.strip()
    
    ##parse teaser story links
    story_title_urls = resultsTeaser.find_all("div", class_="storylist_title")
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
        print("\n")
        print(story_teasers[idx], sep = "\n")
        print("\n")
        print(story_title_urls[idx], sep = "\n")
        print("\n")
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
    

##will run forever
##while True:
updateTeaserPage()
##randomSleep(5,10)
