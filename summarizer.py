import bs4 as bs
import urllib.request
import re
import nltk
import spacy
import heapq

class Summarizer:
    _nlp = spacy.load("en_core_web_md")
    #summarizes by way of extraction
    def summarize(self, text, compressionRate=0.75):
        #cannot summarize text if desired compression rate is <= 0% compression (pointless/impossible)
        #or >= 100% (impossible)
        if compressionRate <= 0 or compressionRate >= 1:
            raise Exception("Compression rate must be greater than 0 and less than 1!")

        #clean text, get rid of all numbers/symbols
        cleanedText = self.__cleanWords(text)
        #tokenize lemma of each lowercased word
        tokens = self.__tokenize(cleanedText.lower())

        #tokenize sentences
        sentences = nltk.sent_tokenize(text)
        #generate word frequencies
        wordFrequencies = self.__genWordFrequencies(tokens)
        #score sentences
        sentenceScores = self.__scoreSentences(sentences, wordFrequencies)
        print(sentenceScores)
        
        print("\n\n=========SUMMARY==========")
        #generate summary based on sentence scores and compression rate
        summary = self.__generateSummary(sentences, sentenceScores, compressionRate)
        return ' '.join(summary)

    def __genWordFrequencies(self, tokens):
        word_frequencies = {}
        for word in tokens:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

        maximum_frequncy = max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)

        return word_frequencies

    #TODO simplify this
    def __scoreSentences(self, sentences, wordFrequencies):
        sentenceScores = {}
        #max number of words in a sentence for it to be considered
        maxSentenceLengthAllowed = 30
        for sent in sentences:
            if len(sent.split(" ") < maxSentenceLengthAllowed):
                print("Sentence:", sent)
                #TODO somehow avoid retokenizing words here.  Slightly slower because of scaPy's overhead when
                #tokenizing sentence (due to automatically added attributes, like lemmatization)
                for word in self.__tokenize(sent.lower()):
                    if word in wordFrequencies.keys():
                        print("Valid word:", word)
                        if sent not in sentenceScores.keys():
                            sentenceScores[sent] = wordFrequencies[word]
                        else:
                            sentenceScores[sent] += wordFrequencies[word]
        return sentenceScores

    def __generateSummary(self, sentences, sentenceScores, compressionRate):
        percOfTotal = int(len(sentences) * (1 - compressionRate))
        return heapq.nlargest(percOfTotal, sentenceScores, key=sentenceScores.get)

    #TODO double check these are being cleaned correctly
    def __cleanWords(self, text):
         # Removing Square Brackets and Extra Spaces
        text = re.sub(r'\[[0-9]*\]', ' ', text)
        text = re.sub(r'\s+', ' ', text)

        # Removing special characters and digits
        text = re.sub('[^a-zA-Z]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text

    def __tokenize(self, text):
        tokens = list(token.lemma_ for token in self._nlp(text) if self.__isValidToken(token))
        '''print("TOKENS")
        for token in tokens:
            print(token)'''
        return tokens

    def __isValidToken(self, token):
        return not (not token or not token.string.strip() or token.is_stop or token.is_punct)

    def readArticle(self, url):
        scraped_data = urllib.request.urlopen(url)
        article = scraped_data.read()
        parsed_article = bs.BeautifulSoup(article,'lxml')
        paragraphs = parsed_article.find_all('p')

        article_text = ""
        for p in paragraphs:
            article_text += p.text
        return article_text
    
    def readFileText(self, filename):
        return "".join(open(filename).readlines())


summarizer = Summarizer()
#text = summarizer.readFileText("test_texts/test_text_htmlConvo.txt")
text = summarizer.readArticle("https://en.wikipedia.org/wiki/Medicine")
summary = summarizer.summarize(text, 0.9)
print(summarizer.summarize(summary, 0.75))
