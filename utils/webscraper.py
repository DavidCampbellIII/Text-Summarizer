import bs4 as bs
import urllib.request

def scrapeURL(url):
    mainPage = urllib.request.urlopen(url)
    pageText = mainPage.read()
    parsedText = bs.BeautifulSoup(pageText, "lxml")
    tableElements = parsedText.find_all("td")
    for td in tableElements:
        print(td.text)


if __name__ == "__main__":
    url = "https://www.mtsamples.com/site/pages/browse.asp?type=98-General%20Medicine"
    scrapeURL(url)