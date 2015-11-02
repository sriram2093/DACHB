# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 20:55:33 2015

@author: sriram
"""

#from collections import defaultdict

summary =""
#directoryName = "C:\Users\sriram\Documents\Python Scripts\Data\Articles and Comments\articles\"
directoryName = "C:\Users\sriram\Documents\Python Scripts"
wordMinFrequency = 5
summaryNoOfLines = 3
sentenceDictionary = {};
wordDictionary = {};
backwardStemming = { };#from a stem, getting a word actually in the document
selectedArticles = {};
articleOrComment = 0
# 1 if article, 2 if comment


def initt():
    global summary,sentenceDictionary,wordDictionary,backwardStemming,selectedArticles
    sentenceDictionary ={}
    wordDictionary={}
    backwardStemming={}
    selectedArticles={}
    summary =""
    
    
def mmain(articles,wmf, sumNoOfLines,articleOrCommentVariable):
    
    
    global wordMinFrequency,summaryNoOfLines,sentenceDictionary,wordDictionary,backwardStemming,selectedArticles,summary,articleOrComment
    
    initt();

    wordMinFrequency = wmf
    summaryNoOfLines = sumNoOfLines
    selectedArticles = articles
    articleOrComment = articleOrCommentVariable
    #selectedArticles = articlesReceived
    #sentenceDictionary = defaultdict(list)
    openFiles()
    stemWordsCountFrequency()
    rankingSentences()
    sortingRankedSentences()
    
    return summary


# Opening the list of files which have 
#def openFiles():
#    import os
#    i=0
#    for file in os.listdir(directoryName):
#        if file.endswith(".txt"):#grab the files, not the subfolders
#            fileReadAndSplit(file)
#            i=i+1
#        #if i==10:
#        #    return
#    print "--- ", i, "files processed ---"

def openFiles():
    global selectedArticles
    import os
    for articleNumber in selectedArticles:
        articleNumber = str(int (articleNumber))
        if articleOrComment is 1:
            file = directoryName+"\\Data\\Articles and Comments\\articles\\articles\\" + articleNumber+" [article].txt"
            fileReadAndSplit(file)
        else:
            file = directoryName+"\\Data\\Articles and Comments\\comments\\" + articleNumber+" [comments].txt"
            commentFileReadAndSplit(file)


    
#splitting into sentences and populating the dictionary
#key is the sentence, value is zero by default
#sentence dictionary is populated here
def fileReadAndSplit(file):
    import string
    from xml.dom import minidom                                          

    global sentenceDictionary
    
    try:
        f11 = open(file,"r")
        f11.close()
    except:
        return
    #locale.getpreferredencoding
    f = open(file,"r")
    #f = codecs.open(file, encoding="ascii" , mode='r')
    #lines = f.readlines()
    
    lines = ""    
    
    if articleOrComment is 2:
        lines = "<comments>"    
    lines = lines + f.read()
    
    if articleOrComment is 2:
        lines = lines + "</comments>"
        string.replace(lines,"&"," and ")
    
        
    ##removing all the special characters from the textt    
    include = set(string.punctuation)
    lines = ''.join(e for e in lines if e in include or e.isspace() or e.isalnum())
    

    f.close()
    if articleOrComment is 1: #article
        sentences = lines.split(".")
        
    elif articleOrComment is 2: #comment
        print lines
        lines = lines.replace("<<"," ")
        #lines = lines.replace("<"," less than ")
        #lines = lines.replace(">"," greater than ")
        lines = lines.replace("&","and")
        xmldoc = minidom.parseString(lines)
        comments = xmldoc.getElementsByTagName("comment")
        
        sentences = []
        
        
        for comment in comments:
            content = comment.getElementsByTagName("content")[0]
            #print type(content)
            
            sentences.append(getText(content.childNodes))
            
            
     ######################################### xmldoc.
       
    
    
    for sentence in sentences:
        sentence = sentence + '.'
        sentenceDictionary[sentence] = 0; # Add new entry
        #sentenceDictionary[sentence].append(0)
    #print f.readline().split(".")[0]



#process comments dictionary
def commentFileReadAndSplit(file):
    import string
    from xml.dom import minidom                                          

    global sentenceDictionary
    
    try:
        f11 = open(file,"r")
        f11.close()
    except:
        return
    #locale.getpreferredencoding
    f = open(file,"r")
    #f = codecs.open(file, encoding="ascii" , mode='r')
    #lines = f.readlines()
    
    lines = f.readlines()
    
    comments = ""
    contentFlag = False
    for line in lines:
        if line.startswith("<content>"):
            contentFlag = True
            continue
            
        elif line.startswith("</content>"):
            contentFlag = False
            continue
            

        if contentFlag is True:
            comments = comments+line
        
    string.replace(comments,"&"," and ")
    
        
    ##removing all the special characters from the textt    
    include = set(string.punctuation)
    comments = ''.join(e for e in comments if e in include or e.isspace() or e.isalnum())
    

    f.close()
    
    sentences = comments.split(".")
       
    for sentence in sentences:
        sentence = sentence + '.'
        sentenceDictionary[sentence] = 0; # Add new entry
        #sentenceDictionary[sentence].append(0)
    #print f.readline().split(".")[0]


#Method to stem the words and count the frequency
def stemWordsCountFrequency():
    global sentenceDictionary,backwardStemming,wordDictionary
    
    import nltk
    from nltk import PorterStemmer
    from nltk.corpus import stopwords
    
    for sentence in sentenceDictionary:
        #removes all characters from the content that create problems for tokenization
        sentence = sentence.replace('\n', ' ')
        sentence = sentence.replace('[', ' ')
        sentence = sentence.replace(']', ' ')
        sentence = sentence.replace('\x92', '\'')
        sentence = sentence.replace('\x85', '...')
        sentence = sentence.replace('\x96', '-')
        sentence = sentence.replace('\x93', '\"')
        sentence = sentence.replace('\x94', '\"')
        sentence = sentence.replace('\xa0', ' ')
        sentence = sentence.replace('\x97', ' ')
        sentence = sentence.lower()
        
        try:
            tokens = nltk.word_tokenize(sentence)
        except:
            print " TOKENIZER CRASHED "
            print " [Copy this string in the shell to see unicode characters "
            print sentence
        
        #stems the tokens. For example 'complications' gets to u'Complic'
        stems = [ ]
        stemmer = PorterStemmer()#uses the Porter stemming algorithm
        for token in tokens:
            stem = str( stemmer.stem_word(token) )
            backwardStemming[stem] = token
            stems.append( stem )

        #gets rid of useless English words (or, and, this, that...)
        stop = stopwords.words('english')
        
        tokens = [i for i in stems if i not in stop]
       
        #counts the tokens
        for token in tokens:
            if wordDictionary.has_key(token):#update count
                wordDictionary[token] = wordDictionary[token] + 1
            else:
                wordDictionary[token]=1#if the entry is new, set to 1
    
        
        #print wordDictionary
    
    processWordDictionary()   
    
    
    
#####
def summaryGenerator(sortedDictionary):
    global summary,summaryNoOfLines
    counter = 1
    for sent in sortedDictionary:
        #if sent.startswith("But"):
        sent = sent.replace('But'," ")
        if counter<summaryNoOfLines:
            summary = summary+sent
            counter = counter +1
    
    


#processing the word dictionary based on the ranking of the words.
def processWordDictionary():
    global wordDictionary,wordMinFrequency
    for i in wordDictionary.keys():
        if wordDictionary[i]<wordMinFrequency:
                del wordDictionary[i]
    

def sortingRankedSentences():
    global sentenceDictionary  
    sortedDictionary = sorted(sentenceDictionary, key=sentenceDictionary.get, reverse = True)
    summaryGenerator(sortedDictionary)
    
#function to rank the sentences of the sentence dictionary
def rankingSentences():
       
    import nltk
    from nltk import PorterStemmer
    from nltk.corpus import stopwords
    
    score =0
    
    for originalSentence in sentenceDictionary:
        score =0
        #removes all characters from the content that create problems for tokenization
        sentence = originalSentence        
        sentence = sentence.replace('\n', ' ')
        sentence = sentence.replace('[', ' ')
        sentence = sentence.replace(']', ' ')
        sentence = sentence.replace('\x92', '\'')
        sentence = sentence.replace('\x85', '...')
        sentence = sentence.replace('\x96', '-')
        sentence = sentence.replace('\x93', '\"')
        sentence = sentence.replace('\x94', '\"')
        sentence = sentence.replace('\xa0', ' ')
        sentence = sentence.lower()
        
        try:
            tokens = nltk.word_tokenize(sentence)
        except:
            print " TOKENIZER CRASHED "
            print " [Copy this string in the shell to see unicode characters "
            print sentence
            
        for token in tokens:
            if wordDictionary.get(token) is None:
                score = score + 0
            else:
               score = score + wordDictionary.get(token)
                
            
        sentenceDictionary[originalSentence] = score
        

#mmain(articles)