import bs4 as bs
import urllib.request
import re

def scrapeURL(url, domainName):
    mainPage = urllib.request.urlopen(url)
    pageText = mainPage.read()
    parsedText = bs.BeautifulSoup(pageText, "lxml")

    dropDownElements = parsedText.find_all("div", class_="dropdown-menu")
    #use set to remove duplicates
    links = set()
    for e in dropDownElements:
        for a in e.find_all("a", href = re.compile("/sample.asp")):
            link = domainName + a["href"].replace(" ", "%20") #must add domain name and replace spaces with %20
            links.add(link)
    goToLinks(links)

#Goes through all found links and starts parsing process
def goToLinks(links):
    for link in links:
        print("Going to... ", link)
        pageText = urllib.request.urlopen(link).read()
        parsePage(pageText)

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

    #chief complaint
    print("Bold elements:", boldElements)
    print("Body", boldElements[3])
    print(boldElements[3].next_sibling)

    #history of present illness

    #past medical history

    #past surgical history

    #allergies

    #social history

    #review of systems

    #physical examination

    #laboratory values

    #dianostic studies

    #impression and plan

    print("\nDict: ", pageData)
    print("\n")

def saveParsedPageToJson(pageData):
    pass

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
    scrapeURL(url, domainName)
    print("Done!")