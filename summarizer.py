import bs4 as bs
import urllib.request
import re
import nltk
import heapq

class Summarizer:

    #summarizes by way of extraction
    def summarize(self, text, compressionRate=0.75):
        if compressionRate <= 0 or compressionRate >= 1:
            raise Exception("Compression rate must be greater than 0 and less than 1!")

        # Removing Square Brackets and Extra Spaces
        text = re.sub(r'\[[0-9]*\]', ' ', text)
        text = re.sub(r'\s+', ' ', text)

        # Removing special characters and digits
        formatted_text = re.sub('[^a-zA-Z]', ' ', text )
        formatted_text = re.sub(r'\s+', ' ', formatted_text)

        sentence_list = nltk.sent_tokenize(text)
        word_frequencies = self.__genWordFrequencies(formatted_text)
        

        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]

        percOfTotal = int(len(sentence_list) * (1 - compressionRate))
        summary_sentences = heapq.nlargest(percOfTotal, sentence_scores, key=sentence_scores.get)
        return ' '.join(summary_sentences)

    def __genWordFrequencies(self, formatted_text):
        word_frequencies = {}
        stopwords = nltk.corpus.stopwords.words('english')
        for word in nltk.word_tokenize(formatted_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

        maximum_frequncy = max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)

        return word_frequencies

'''scraped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Artificial_intelligence')
article = scraped_data.read()

parsed_article = bs.BeautifulSoup(article,'lxml')

paragraphs = parsed_article.find_all('p')

article_text = ""
for p in paragraphs:
    article_text += p.text'''

