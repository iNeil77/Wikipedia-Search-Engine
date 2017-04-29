#This function serves as a module to wikiIndexer.py
#It takes as input the text/title given and returns the list of words after
#completing the various parsing operations : casefolding, stop words removal
#tokenisation and stemming
import re                                                           #modules
import collections
from nltk.stem import SnowballStemmer

stopwords={}                                          #Create stopwords list
with open('stopwords.txt','r') as f:
  for line in f:
    line= line.strip()
    stopwords[line]=1
  od = collections.OrderedDict(sorted(stopwords.items()))
  stopwords = od

def tokenise(data):                                                 #Tokenise
  tokenisedWords=re.findall("\d+|[\w]+",data)
  return tokenisedWords
  #tokenisedWords=[key.encode('utf-8') for key in tokenisedWords]
  #return tokenisedWords

def stopWords(listOfWords):                                         #Stop Words Removal
  stopped = []
  for key in listOfWords:
    if key not in stopwords:
      stopped.append(key)
  return stopped

def stemmer(listOfTokens):
  stemmed = []
  for f in listOfTokens:
    stemmed.append(SnowballStemmer('english').stem(f))

  return stemmed

def findExternalLinks(data):
  links=[]
  lines = data.split("==external links==")
  if len(lines)>1:
    lines=lines[1].split("\n")
    for i in range(len(lines)):
      if '* [' in lines[i] or '*[' in lines[i]:
        word=""
        temp=lines[i].split(' ')
        word=[key for key in temp if 'http' not in temp]
        word=' '.join(word)
        links.append(word)
  links=tokenise(' '.join(links))
  links = stopWords(links)
  links= stemmer(links)

  temp=collections.defaultdict(int)
  for key in links:
    temp[key]+=1
  links=temp
  return links

def findInfoBoxTextCategory(data):                                        #find InfoBox, Text and Category
  info=[]
  bodyText=[]
  category=[]
  links=[]
  flagtext=1
  lines = data.split('\n')
  for i in range(len(lines)):
    if '{{infobox' in lines[i]:
      flag=0
      temp=lines[i].split('{{infobox')[1:]
      info.extend(temp)
      while True:
            if '{{' in lines[i]:
                count=lines[i].count('{{')
                flag+=count
            if '}}' in lines[i]:
                count=lines[i].count('}}')
                flag-=count
            if flag<=0:
                break
            i+=1
            info.append(lines[i])

    elif flagtext:
      if '[[category' in lines[i] or '==external links==' in lines[i]:
        flagtext=0
      bodyText.append(lines[i])

    else:
      if "[[category" in lines[i]:
        line = data.split("[[category:")
        if len(line)>1:
            category.extend(line[1:-1])
            temp=line[-1].split(']]')
            category.append(temp[0])

  category=tokenise(' '.join(category))
  category = stopWords(category)
  category= stemmer(category)

  info=tokenise(' '.join(info))
  info = stopWords(info)
  info= stemmer(info)

  bodyText=tokenise(' '.join(bodyText))
  bodyText = stopWords(bodyText)
  bodyText= stemmer(bodyText)

  temp=collections.defaultdict(int)
  for key in info:
    temp[key]+=1
  info=temp

  temp=collections.defaultdict(int)
  for key in bodyText:
    key.encode("utf8")
    temp[key]+=1
  bodyText=temp

  temp=collections.defaultdict(int)
  for key in category:
    temp[key]+=1
  category=temp

  return info, bodyText, category


def processTitle(data):                                             #Parse Title
  data=data.lower()                                                 #Case folding
  tokenisedTitle=tokenise(data)                                     #Tokenisation
  stopWordsRemoved = stopWords(tokenisedTitle)                      #Stop Word Removal
  stemmedWords= stemmer(stopWordsRemoved)                           #Stemming

  temp=collections.defaultdict(int)
  for key in stemmedWords:
    temp[key]+=1
  stemmedWords=temp
  return stemmedWords

def processText(data):                                              #Parse Text
  data = data.lower()                                               #Case Folding
  externalLinks = findExternalLinks(data)
  data = data.replace('_',' ').replace(',','')
  infoBox, bodyText, category = findInfoBoxTextCategory(data)                      #Tokenisation
  return bodyText, infoBox, category, externalLinks
