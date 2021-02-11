import bs4 as bs
from urllib.request import urlopen, Request
import re
import json
import os

def scrapeURL(url, domainName, savePath):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    request = Request(url=url, headers=headers)
    mainPage = urlopen(request)
    pageText = mainPage.read()
    parsedText = bs.BeautifulSoup(pageText, "lxml")

    dropDownElements = parsedText.find_all("div", class_="dropdown-menu")
    #use set to remove duplicates (there are two sets of pages we parse through, for some reason)
    links = set()
    for e in dropDownElements:
        #only find anchors that have "/sample.asp" as a part of their url
        for a in e.find_all("a", href = re.compile("/sample.asp")):
            link = domainName + a["href"].replace(" ", "%20") #must add domain name and replace spaces with %20
            links.add(link)

    #goes through all found links and starts parsing process
    for link in links:
        print("Going to... ", link)
        request = Request(url=link, headers=headers)
        pageText = urlopen(request).read()
        pageData = parsePage(pageText)
        saveParsedPageToJson(savePath, pageData)

#Parses data from given page text and puts into dict
def parsePage(pageText):
    pageData = {}
    parsedText = bs.BeautifulSoup(pageText, "lxml")
    #sample name
    h1 = parsedText.find("h1")
    addElement(pageData, "Sample Name", h1.text, "sample name:")

    #description
    h2 = parsedText.find("h2")
    addElement(pageData, "Description", h2.text, "description:", "(Medical Transcription Sample Report)")

    #find all bolded elements
    boldElements = parsedText.find("div", class_="hilightBold").find_all("b")

    #go one at a time through each bolded element:
        #use bolded text as entry name (to title case)
        #keep grabbing next sibling until next bolded element is reached
        #stop once we reach KEYWORDS, which seems to always be the last bold element on each page
    startIndex = 3
    for i in range(startIndex, len(boldElements) - 1):
        #current bold element we are on
        currentBold = boldElements[i]
        #stop at the next bold element, grab all text in between
        stopBold = boldElements[i + 1]
        #clean title of extra spaces and colons
        title = currentBold.text.title().strip().replace(":", "")
        #find all the text content between this bold and the next bold element
        content = findNextValidSibling(currentBold, stopBold)
        pageData[title] = content

    print("\nDict: ", pageData)
    print("\n")

    return pageData

def saveParsedPageToJson(savePath, pageData):
    filename = savePath + pageData["Sample Name"] + ".json"
    f = open(filename, 'w')
    #write formatted json to file
    f.write(json.dumps(pageData, indent=4))
    f.close()

def findNextValidSibling(start, stop):
    #store as list, faster than string concatenation
    result = []
    current = start.next_sibling

    #keep going until we reach the stop bold element
    while current is not None and current != stop:
        currentStr = str(current).strip()
        #if the current sibling is valid (not an <a> or <br>), add to result
        if isValidSibling(currentStr):
            result.append(currentStr)
            #add new line just in case this sibling has multiple line breaks in it
            result.append("\n")
        current = current.next_sibling

    if len(result) > 0:
        #remove last element because we don't want a \n at the end of a line
        result.pop()

    #joining a list to a string is much faster
    return "".join(result)

def isValidSibling(element):
    return element and element != "<br/>" and element != "<hr/>" and not "</" in element and len(element) > 0

#adds an element to the page data with the given entryName
def addElement(pageData, entryName, element, elementName, stopPositionName=None):
    cleanedElement = cleanElement(elementName, element, stopPositionName)
    pageData[entryName] = cleanedElement
    print(entryName + ": ", cleanedElement)

#refactor this to use next_sibling instead of reading in h1 and h2 header entirely
def cleanElement(elementName, element, stopPositionName=None):
    offset = len(elementName) + 1
    elementLower = element.lower()
    startIndex = elementLower.find(elementName) + offset
    if stopPositionName:
        stopIndex = elementLower.find(stopPositionName.lower())
        cleanedElement = element[startIndex:stopIndex]
    else:
        cleanedElement = element[startIndex:]
    return cleanedElement.strip()


if __name__ == "__main__":
    url = "https://www.mtsamples.com/site/pages/browse.asp?type=98-General%20Medicine"
    domainName = "https://www.mtsamples.com"
    savePath = os.path.join(os.getcwd(), "webscraper_data\\")
    scrapeURL(url, domainName, savePath)
    print("Done!")