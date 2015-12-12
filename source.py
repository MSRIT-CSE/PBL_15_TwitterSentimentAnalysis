# -*- coding: utf-8 -*-

import re
import csv
import nltk.classify
 
def replace(s):   
    p = re.compile(r"(.)\1{1,}", re.DOTALL) 
    return p.sub(r"\1\1", s)

def handleTweetContents(tweetContent):    
    tweetContent = tweetContent.lower()
    tweetContent = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweetContent)
        tweetContent = re.sub('@[^\s]+','AT_USER',tweetContent)    
    tweetContent = re.sub('[\s]+', ' ', tweetContent)
    tweetContent = re.sub(r'#([^\s]+)', r'\1', tweetContent)
    tweetContent = tweetContent.strip('\'"')
    return tweetContent

def stopWords(listOfStopWords):
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    fp = open(listOfStopWords, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords

def getfv(tweetContent, stopWords):
    featureVector = []  
    words = tweetContent.split()
    for w in words:
        w = replace(w) 
                w = w.strip('\'"?,.')
        value = re.search(r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", w)
        if(w in stopWords or value is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector    

def obtain_features(tweetContent):
    tweetContent_words = set(tweetContent)
    features = {}
    for word in listoffeatures:
        features['contains(%s)' % word] = (word in tweetContent_words)
    return features


inpTweetContents = csv.reader(open('C:\Documents/PBL-project/training_neatfile_4.csv', 'rb'), delimiter=',', quotechar='"')
stopWords = stopWords('C:\ Documents/PBL-project/stopwords.txt')
count = 0;
listoffeatures = []
tweetContents = []
for row in inpTweetContents:
    sentiment = row[0]
    tweetContent = row[1]
    processedTweetContent = handleTweetContents(tweetContent)
    featureVector = getfv(processedTweetContent, stopWords)
    listoffeatures.extend(featureVector)
    tweetContents.append((featureVector, sentiment));


listoffeatures = list(set(listoffeatures))

training_set = nltk.classify.util.apply_features(obtain_features, tweetContents)

NBClassifier = nltk.NaiveBayesClassifier.train(training_set)

pos_count=0
neg_count=0
neu_count=0
f=open("C:\sqlite/outputfile.csv","wb")
c=csv.writer(f,delimiter=',')

testTweetContents=csv.reader(open('C:\sqlite/testfinal.csv','rb'),delimiter=',')
for row1 in testTweetContents:
    testTweetContent=row1[0]
    processedTestTweetContent = handleTweetContents(testTweetContent)
    sentiment = NBClassifier.classify(obtain_features(getfv(processedTestTweetContent, stopWords)))
    print "testTweetContent = %s, sentiment = %s\n" % (testTweetContent, sentiment)
    if(sentiment=='positive'):
        pos_count+=1
    elif(sentiment=='negative'):
        neg_count+=1
    else:
        neu_count+=1
    c.writerow([sentiment,row[1]])
print "positive count= %d negative count=%d neutral count=%d" % (pos_count,neg_count,neu_count)
