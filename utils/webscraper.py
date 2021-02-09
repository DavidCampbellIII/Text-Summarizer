import bs4 as bs
import urllib.request
import re
import json
import os

def scrapeURL(url, domainName, savePath):
    mainPage = urllib.request.urlopen(url)
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
        pageText = urllib.request.urlopen(link).read()
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
    addElement(pageData, "Description", h2.text, "description:", "\r\n")

    #find all bolded elements
    boldElements = parsedText.find("div", class_="hilightBold").find_all("b")

    #TODO:
    #go one at a time through each bolded element:
        #use bolded text as entry name (to title case)
        #keep grabbing next sibling until next bolded element is reached
        #stop once we reach KEYWORDS, which seems to always be the last bold element on each page

    startIndex = 3
    for i in range(startIndex, len(boldElements) - 1):
        currentBold = boldElements[i]
        stopBold = boldElements[i + 1]
        #TODO clean title
        title = currentBold.text.title()
        content = findNextValidSibling(currentBold, stopBold)
        print("Title:", title)
        print("Content:", content)
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
    while current and current != stop:
        #if the current sibling is valid (not an <a> or <br>), add to result
        print("Current", current)
        if isValidSibling(current):
            result.append(current.join("\n"))
        current = current.next_sibling
    #joining a list to a string is much faster
    return "".join(result)

def isValidSibling(element):
    element = str(element)
    return element and element != "<br/>" and element != "<hr/>" and not "</" in element

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
    if stopPositionName != None:
        stopIndex = elementLower.find(stopPositionName)
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