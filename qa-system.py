# -*- coding: utf-8 -*-
#######################################################################################################################################
#######################################################################################################################################
#####
##### Brandon Chin
##### Thursday, April 11, 2019
##### CMSC 416 - Natural Language Processing
##### Programming Assignment 5 - Eliza Chatbot
#####
##### 1. The Problem
##### Implement a Question Answering (QA) system in Python3 called qa-system.py.
##### Your system should be able to answer Who, What, When and Where questions (but not Why or How questions).
##### Your system should handle questions from any domain, and should provide answers in complete sentences that are specific to the question asked.
##### Please do not provide any information beyond what is asked for by the question.
#####
##### 2. Example Input/Output
#####
##### =?> When was George Washington born? (user)
#####
##### => George Washington was born on February 22, 1732. (system)
#####
##### =?> What is a bicycle?
#####
##### => A bicycle has two wheels and is used for transportation.
#####
##### =?> Where is Duluth, Minnesota?
#####
##### =>I am sorry, I don't know the answer.
#####
##### =?> exit
#####
##### Thank you! Goodbye.
#####
##### 3. Algorithm
#####
##### #1. Describe the program, and prompt for question
#####
##### #2. Interpret question being Who, What, When, Where
#####
##### #3. Using a switch case statement, handle each question according to the Who, What, When, Where
#####
##### #4. Reformulating the question as a statement, and looking through the Wikipedia API for the desired answer
#####
##### #5. Strip the sentences of extra information, and only return sentences that are relevant/prove to be most interesting
#####
##### #6. Choose the sentence ranked the highest as the answer, and return it
#####
#######################################################################################################################################
#######################################################################################################################################

import re
import sys
from decimal import Decimal
from random import *
import operator
from string import punctuation
import nltk
import wikipediaapi
from nltk.corpus import brown
from nltk.corpus import stopwords
from nltk import sent_tokenize, word_tokenize
from nltk import PorterStemmer
from nltk.corpus import wordnet
import lxml.html
import string

def main():##main method

    print("[SYSTEM] This is a QA system by Brandon Chin. It will try to answer questions that start with Who, What, When or Where. Enter 'exit' to leave the program.")


    while (1):
        print("[User]", end = ' ')

        questionInput = input("");
        # print ("Your input is: ", questionInput)

        questionInput = ''.join([letter for letter in questionInput if letter not in punctuation])

        # print ("Your input after punc removal is: ", questionInput)

        questionPhraseTokens = []
        queryPhraseTokens = []
        answerTypes = []
        answerPattern = []
        tokenIndex = 0


        if (questionInput == "exit" or questionInput == "Exit"):
            print("[System] Exiting...")
            break
        sentenceTokens = generate_Tokens(questionInput)

        posTokens = nltk.pos_tag(sentenceTokens)

        # print("posTokens: " + str(posTokens))

        # whatToken = ""
        # whenToken = ""
        firstToken = posTokens[tokenIndex][0]

        # if firstToken == "What":
        #     whatToken = firstToken
        #
        # if questionType == "When":
        #     whenToken = firstToken

        def date_when_Rule():
            #When was George Washington born?
            #When is Mardi Gras?
            #When is Christmas?
            #When was the Great War?
            #When did the Great Depression start?

            tokenIndex=1

            if posTokens[tokenIndex][1] == "VBZ":
                tokenIndex += 1

            if posTokens[tokenIndex][1] == "VBD":
                tokenIndex += 1

            if posTokens[tokenIndex][1] == "DT":
                tokenIndex += 1

            if posTokens[tokenIndex][1] == "NNP":
                while(tokenIndex < len(posTokens)):
                    if posTokens[tokenIndex][1] == "NNP":
                        questionPhraseTokens.append(posTokens[tokenIndex][0])
                        # print("questionPhraseTokens: " + str(questionPhraseTokens))
                    if posTokens[tokenIndex][1] == "NN" or posTokens[tokenIndex][1] == "VBD":
                        queryPhraseTokens.append(posTokens[tokenIndex][0])
                        # print("queryPhraseTokens: " + str(queryPhraseTokens))
                    # print("len(posTokens): " + str(len(posTokens)))
                    # print("tokenIndex: " + str(tokenIndex))
                    tokenIndex += 1

            whenAnswerTypes = ["NNP", "CD"]
            whenPattern = ["NNP", "CD", "CD"]

            answerTypes.extend(whenAnswerTypes)
            answerPattern.extend(whenPattern)

            # print("answerTypes: " + str(answerTypes))
            # print("answerPattern: " + str(answerPattern))


        def properN_what_Rule():
            #What is a telescope?
            #What was the Chinese Civil War?
            #What is Twitter?
            #What is love?
            #What is a life sentence?

            tokenIndex=1

            if posTokens[tokenIndex][1] == "VBZ" or posTokens[tokenIndex][1] == "VBD" or posTokens[tokenIndex][1] == "VBP":
                queryPhraseTokens.append(posTokens[tokenIndex][0])
                tokenIndex += 1

            if posTokens[tokenIndex][1] == "DT":
                tokenIndex += 1

            while(tokenIndex < len(posTokens)):
                if posTokens[tokenIndex][1] == "NNP":
                    questionPhraseTokens.append(posTokens[tokenIndex][0])
                    # print("questionPhraseTokens: " + str(questionPhraseTokens))
                if posTokens[tokenIndex][1] == "NN":
                    questionPhraseTokens.append(posTokens[tokenIndex][0])
                    # print("questionPhraseTokens: " + str(questionPhraseTokens))
                if posTokens[tokenIndex][1] == "NNS":
                    questionPhraseTokens.append(posTokens[tokenIndex][0])
                    # print("questionPhraseTokens: " + str(questionPhraseTokens))
                if posTokens[tokenIndex][1] == "JJR":
                    questionPhraseTokens.append(posTokens[tokenIndex][0])
                    # print("questionPhraseTokens: " + str(questionPhraseTokens))
                if posTokens[tokenIndex][1] == "JJ":
                    questionPhraseTokens.append(posTokens[tokenIndex][0])
                    # print("questionPhraseTokens: " + str(questionPhraseTokens))
                # if posTokens[tokenIndex][1] == "NN" or posTokens[tokenIndex][1] == "VBD":
                if posTokens[tokenIndex][1] == "VBD":
                    queryPhraseTokens.append(posTokens[tokenIndex][0])
                #     print("queryPhraseTokens: " + str(queryPhraseTokens))
                # print("len(posTokens): " + str(len(posTokens)))
                # print("tokenIndex: " + str(tokenIndex))
                tokenIndex += 1

            whatAnswerTypes = ["NN"]
            whatPattern = ["NN"]

            answerTypes.extend(whatAnswerTypes)
            answerPattern.extend(whatPattern)

            # print("answerTypes: " + str(answerTypes))
            # print("answerPattern: " + str(answerPattern))

        def where_Rule():
            #Where is Central Park?
            #Where is Bollywood?
            #Where is Houston located?
            #Where is Italy?
            #Where is the White House?

            tokenIndex=1

            if posTokens[tokenIndex][1] == "VBZ" or posTokens[tokenIndex][1] == "VBD":
                queryPhraseTokens.append(posTokens[tokenIndex][0])
                tokenIndex += 1

            if posTokens[tokenIndex][1] == "DT":
                tokenIndex += 1

            while(tokenIndex < len(posTokens)):
                if posTokens[tokenIndex][1] == "NNP":
                    questionPhraseTokens.append(posTokens[tokenIndex][0])
                    # print("questionPhraseTokens: " + str(questionPhraseTokens))
                if posTokens[tokenIndex][1] == "NN":
                    questionPhraseTokens.append(posTokens[tokenIndex][0])
                    # print("questionPhraseTokens: " + str(questionPhraseTokens))
                if posTokens[tokenIndex][1] == "NNS":
                    questionPhraseTokens.append(posTokens[tokenIndex][0])
                    # print("questionPhraseTokens: " + str(questionPhraseTokens))
                if posTokens[tokenIndex][1] == "JJR":
                    questionPhraseTokens.append(posTokens[tokenIndex][0])
                    # print("questionPhraseTokens: " + str(questionPhraseTokens))
                if posTokens[tokenIndex][1] == "JJ":
                    questionPhraseTokens.append(posTokens[tokenIndex][0])
                    # print("questionPhraseTokens: " + str(questionPhraseTokens))
                # if posTokens[tokenIndex][1] == "NN" or posTokens[tokenIndex][1] == "VBD":
                if posTokens[tokenIndex][1] == "VBD":
                    queryPhraseTokens.append(posTokens[tokenIndex][0])
                    # print("queryPhraseTokens: " + str(queryPhraseTokens))
                if posTokens[tokenIndex][1] == "VBZ":
                    queryPhraseTokens.append(posTokens[tokenIndex][0])
                #     print("queryPhraseTokens: " + str(queryPhraseTokens))
                # print("len(posTokens): " + str(len(posTokens)))
                # print("tokenIndex: " + str(tokenIndex))
                tokenIndex += 1

            whereAnswerTypes = ["NNP"]
            wherePattern = ["NNP"]

            answerTypes.extend(whereAnswerTypes)
            answerPattern.extend(wherePattern)

            # print("answerTypes: " + str(answerTypes))
            # print("answerPattern: " + str(answerPattern))

        def who_Rule():
            #Who is Donald Trump?
            #Who is Braden Holtby?
            #Who is Steve Jobs?
            #Who is Narendra Modi?
            #Who is Tom Clancy?

            tokenIndex=1

            if posTokens[tokenIndex][1] == "VBZ" or posTokens[tokenIndex][1] == "VBD":
                queryPhraseTokens.append(posTokens[tokenIndex][0])
                tokenIndex += 1

            if posTokens[tokenIndex][1] == "DT":
                tokenIndex += 1

            while(tokenIndex < len(posTokens)):
                if posTokens[tokenIndex][1] == "NNP":
                    questionPhraseTokens.append(posTokens[tokenIndex][0])
                    # print("questionPhraseTokens: " + str(questionPhraseTokens))
                if posTokens[tokenIndex][1] == "NN":
                    questionPhraseTokens.append(posTokens[tokenIndex][0])
                    # print("questionPhraseTokens: " + str(questionPhraseTokens))
                if posTokens[tokenIndex][1] == "NNS":
                    questionPhraseTokens.append(posTokens[tokenIndex][0])
                    # print("questionPhraseTokens: " + str(questionPhraseTokens))
                if posTokens[tokenIndex][1] == "JJR":
                    questionPhraseTokens.append(posTokens[tokenIndex][0])
                    # print("questionPhraseTokens: " + str(questionPhraseTokens))
                if posTokens[tokenIndex][1] == "JJ":
                    questionPhraseTokens.append(posTokens[tokenIndex][0])
                    # print("questionPhraseTokens: " + str(questionPhraseTokens))
                # if posTokens[tokenIndex][1] == "NN" or posTokens[tokenIndex][1] == "VBD":
                if posTokens[tokenIndex][1] == "VBD":
                    queryPhraseTokens.append(posTokens[tokenIndex][0])
                    # print("queryPhraseTokens: " + str(queryPhraseTokens))
                if posTokens[tokenIndex][1] == "VBZ":
                    queryPhraseTokens.append(posTokens[tokenIndex][0])
                #     print("queryPhraseTokens: " + str(queryPhraseTokens))
                # print("len(posTokens): " + str(len(posTokens)))
                # print("tokenIndex: " + str(tokenIndex))
                tokenIndex += 1

            whoAnswerTypes = ["NNP","VBZ","NN"]
            whoPattern = ["NNP","VBZ","NN"]

            answerTypes.extend(whoAnswerTypes)
            answerPattern.extend(whoPattern)

            # print("answerTypes: " + str(answerTypes))
            # print("answerPattern: " + str(answerPattern))

        def default():

            default_Recognizer()

        switcher = {
            "What" : properN_what_Rule,
            "When" : date_when_Rule,
            "Where" : where_Rule,
            "Who" : who_Rule,
        }

        def switch(firstToken):
            #print "I got here [1] " + currToken
            return switcher.get(firstToken, default)()

        switch(firstToken)


        # wikiReturnDict = wiki_Search(questionPhraseTokens, queryPhraseTokens, answerTypes, answerPattern)

        print("questionPhraseTokens: " + str(questionPhraseTokens))
        questionString = "".join(questionPhraseTokens)
        questionSyns = wordnet.synsets(str(questionString))
        print("questionSyns: " + str(questionSyns))

        print("queryPhraseTokens: " + str(queryPhraseTokens))
        queryString = "".join(queryPhraseTokens)
        querySyns = wordnet.synsets(str(queryString))
        # querySyns.split()
        # print(querySyns[0].lemmas()[0].name())
        print("querySyns list: " + str(querySyns))

        #List of synonyms, run through it, if you get a return, then move on to next question, otherwise go to next synonym and try that
        #List of more specifics like -name, run through that list, if you get a return, then move on to next question, otherwise go to next -topic and try that

        wikiReturnDict = wiki_Search(questionPhraseTokens, queryPhraseTokens, answerTypes, answerPattern)

        if wikiReturnDict == None:
            for i in range(len(querySyns)):
                print("Count is: " + str(i))
                print(querySyns[i].lemmas()[0].name())
                queryPhraseTokens=querySyns[i].lemmas()[0].name()
                queryPhraseTokens=queryPhraseTokens.lower()
                queryPhraseTokens=queryPhraseTokens.split()
                # print(type(queryPhraseTokens))
                # print(type(questionPhraseTokens))
                # questionPhraseTokens.split()
                wikiReturnDict = wiki_Search(questionPhraseTokens, queryPhraseTokens, answerTypes, answerPattern)
                if wikiReturnDict != None:

                    if "answerWords" in wikiReturnDict:
                        answer_Formulation(questionPhraseTokens, queryPhraseTokens, wikiReturnDict)
                        break
                    else:
                        print (wikiReturnDict.get("fullSentence", "none"))
                        break
        else:
            if "answerWords" in wikiReturnDict:
                answer_Formulation(questionPhraseTokens, queryPhraseTokens, wikiReturnDict)
            else:
                print (wikiReturnDict.get("fullSentence", "none"))

            # print("querySyns list: " + str(querySyns))



        # syns = wordnet.synsets("born")
        # print(syns)

        # print (wikiReturnDict.get("answerWords", "none"))


        # if wikiReturnDict != None:
        #
        #     if "answerWords" in wikiReturnDict:
        #         answer_Formulation(questionPhraseTokens, queryPhraseTokens, wikiReturnDict)
        #     else:
        #         print (wikiReturnDict.get("fullSentence", "none"))
        #
        # else:
        #     default_Recognizer()

        # if posTokens[tokenIndex][0] == "What":
        #     answerType = "definition"
        #
        # if posTokens[tokenIndex][0] == "Who":
        #     answerType = "person"
        #
        # if posTokens[tokenIndex][0] == "When":
        #     answerType = "date"
        #
        # if posTokens[tokenIndex][0] == "Where":
        #     answerType == "location"


        # if posTokens[tokenIndex][1] == "NNP":
        #     stillNounPhrase = True
        #     while(stillNounPhrase == True):
        #         if tokenIndex >= len(posTokens):
        #             stillNounPhrase = False
        #         else:
        #             questionPhraseTokens.append(posTokens[tokenIndex][0])
        #
        #         tokenIndex += 1

        # if posTokens[tokenIndex][1] == "NN":
        #     stillNounPhrase = True
        #     while(stillNounPhrase == True):
        #         if tokenIndex >= len(posTokens):
        #             stillNounPhrase = False
        #         else:
        #             questionPhraseTokens.append(posTokens[tokenIndex][0])
        #         tokenIndex += 1


        # print("pos is: " + str(posTokens))

def default_Recognizer():
    print("[SYSTEM] I am not sure, please ask in a different way")

def generate_Tokens(s):

    # Replace new lines with spaces
    s = re.sub(r'\s+', ' ', s)

    # s = re.sub(r')

    # Break sentence into the tokens, remove empty tokens
    tokens = [token for token in s.split(" ") if token != ""]

    # print("tokens: " + str(tokens))

    return tokens

    # for i in range(len(tokens)):
        # print "Tokens {}: {}".format(i+1, tokens[i])
        # currToken = tokens[i]


wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI
)

p_wiki=wiki_wiki.page("Test 1")
# print(p_wiki.text)

wiki_html=wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.HTML
)

def answer_Formulation(questionPhraseTokens, queryPhraseTokens, wikiReturnDict):
    resultList = wikiReturnDict.get("answerWords", "none")
    # print("result list: " + str(resultList) + " type: " + str(type(resultList)))
    # print("questionPhraseTokens: " + str(questionPhraseTokens))
    # print("queryPhraseTokens: " + str(queryPhraseTokens))
    mergedTokens = questionPhraseTokens + queryPhraseTokens
    # print("merged tokens: " + str(mergedTokens))
    beginSentence = " ".join(mergedTokens)
    # print("beginSentence: " + str(beginSentence))
    # mergedList = mergedTokens + resultList
    endSentence = " ".join(resultList)
    # print("endSentence: " + str(endSentence))
    # finalString = str(beginSentence) + str(endSentence)
    print(str(beginSentence) + " " + str(endSentence) + ".")

def wiki_Search(questionPhraseTokens, queryPhraseTokens, answerTypes, answerPattern):

    questionPhrase = " "
    queryPhrase = " "
    # questionPhrase = "George Washington"
    # questionPhraseTokens = word_tokenize(questionPhrase)
    # queryPhrase = "born"
    # queryPhraseTokens = word_tokenize(queryPhrase)
    # answerTypes = ["NNP", "CD"]
    # answerPattern = ["NNP", "CD", "CD"]

    # questionPhrase = "Abraham Lincoln"
    # questionPhraseTokens = word_tokenize(questionPhrase)
    # queryPhrase = "die"
    # queryPhraseTokens = word_tokenize(queryPhrase)
    # answerTypes = ["NNP", "CD"]
    # answerPattern = ["NNP", "CD", "CD"]

    # questionPhrase = "Pennsylvania"
    # questionPhraseTokens = word_tokenize(questionPhrase)
    # queryPhrase = "capital"
    # queryPhraseTokens = word_tokenize(queryPhrase)
    # answerTypes = ["NNP"]
    # answerPattern = ["NNP"]

    # questionPhrase = "Virginia"
    # questionPhraseTokens = word_tokenize(questionPhrase)
    # queryPhrase = "largest city"
    # queryPhraseTokens = word_tokenize(queryPhrase)
    # answerTypes = ["NNP"]
    # answerPattern = ["NNP"]

    # questionPhrase = "Oregon"
    # questionPhraseTokens = word_tokenize(questionPhrase)
    # queryPhrase = "largest city"
    # queryPhraseTokens = word_tokenize(queryPhrase)
    # answerTypes = ["NNP"]
    # answerPattern = ["NNP"]

    # questionPhrase = "Virginia"
    # questionPhraseTokens = word_tokenize(questionPhrase)
    # queryPhrase = "total area"
    # queryPhraseTokens = word_tokenize(queryPhrase)
    # answerTypes = ["CD", "JJ", "NNS"]
    # answerPattern = ["CD", "JJ", "NNS"]
    #

    # print("questionPhraseTokens " + str(questionPhraseTokens))

    questionPhrase = " ".join(questionPhraseTokens)

    queryPhrase = " ".join(queryPhraseTokens)


    # print("Asking about " + questionPhrase + " " + queryPhrase)
    print("question tokens: ")
    print(questionPhraseTokens)
    print("query tokens: ")
    print(queryPhraseTokens)

    if questionPhrase == None or questionPhrase == "":
        default_Recognizer()
        return

    p_html=wiki_html.page(questionPhrase)

    if p_html == None or p_html.text == None or p_html.text == "":
        default_Recognizer()
        return


    #print(p_html.text)

    #print("Categories")
    #print_categories(p_html)

    #print("Sections")
    #print_sections(p_html.sections)

    page = lxml.html.document_fromstring(p_html.text)
    wikitextonly = page.cssselect('body')[0].text_content()

    #print(wikitextonly)

    sentences = sent_tokenize(wikitextonly)
    sentenceIndex = 0
    answerFound = False
    interestingSentences = dict()

    while answerFound == False and sentenceIndex < len(sentences):
        currentSentence = sentences[sentenceIndex]
        #print("Sentence " + str(sentenceIndex))
        #print(sentences[sentenceIndex])

        # break into tokens
        sentenceTokens = word_tokenize(currentSentence)

        # remove punctuation
        table = str.maketrans('', '', string.punctuation)
        stripped = [words.translate(table) for words in sentenceTokens]

        # remove non-alphabetic tokens
        alphabeticTokens = [word for word in stripped if (word.isalpha() or word.isnumeric())]
        #alphabeticTokens = stripped

        # filter out stop words
        stopWords = set(stopwords.words('english'))
        sanitizedWords = [word for word in alphabeticTokens if not word in stopWords]
        stemmer = PorterStemmer()

        # sanitize the sentence
        #print("Sanitized: ")
        #print(sanitizedWords)

        posTaggedWords = (nltk.pos_tag(sanitizedWords))

        #print(posTaggedWords)

        # find something interesting if NNP matches tokens
        interestLevel = 0

        # first look through subject tokens for match in sentence
        for aSubjectToken in questionPhraseTokens:
            for posTaggedWord, pos in posTaggedWords:
                if posTaggedWord == aSubjectToken:
                    #print("SubjectToken " + aSubjectToken + " matches")
                    # look for part of speech match on NNP
                    if pos == "NN" or pos == "NNP":
                        interestLevel += 1
                        if pos == "NNP":
                            # extra bonus for being a proper noun
                            #print("POS tag also matches")
                            interestLevel += 1
                        break # to stop further matching on same subjectToken

        for aQuestionToken in queryPhraseTokens:
            for posTaggedWord, pos in posTaggedWords:
                # stem for the question tokens, we want a meaning match here, while
                # questionPhraseTokens we want to be exact match
                if stemmer.stem(aQuestionToken) == stemmer.stem(posTaggedWord):
                    #print("QuestionToken " + aQuestionToken + " matches")
                    interestLevel += 1
                    if pos == "NN":
                        # question is a NN, more likely to be the right one
                        interestLevel += 1
                    break

        # look the right type of answers
        for posTaggedWord, pos in posTaggedWords:
            if pos in answerTypes:
                interestLevel += 1
                break # to stop further matching on same answerType


        # for currentWord, posTag in posTaggedWords:
        #     if( currentWord in questionPhraseTokens):
        #         print("currentWord: " + currentWord + " matches subjectToken(s)")
        #         if( posTag == "NNP"):
        #             print("posTag also matches")
        #             interestLevel += 1
        #     if( currentWord in queryPhraseTokens):
        #         print("currentWord: " + currentWord + " matches questionToken(s)")
        #         interestLevel += 1


        # if sentence is interesting
        if interestLevel > 1:
            # print("interesting sentence at level " + str(interestLevel))
            # print(currentSentence)
            # print(posTaggedWords)
            interestingSentences[currentSentence] = [interestLevel, posTaggedWords]
            # print("----")

        sentenceIndex += 1


    # print("interesting sentences")
    highestInterestLevel = 0
    mostInterestingSentence = None
    mostInterestingTaggedWords = None

    for sentence, items in interestingSentences.items():
        #print( "sentence: " + str(sentence) )
        #print( "interest level " + str(interestLevel))
        interestLevel = items[0]
        posTaggedWords = items[1]
        if interestLevel > highestInterestLevel:
            highestInterestLevel = interestLevel
            mostInterestingSentence = sentence
            mostInterestingTaggedWords = posTaggedWords

    # if mostInterestingSentence == None:
    #     return
    # else:
        # print("[SYSTEM] " + str(mostInterestingSentence))
        # print("interest level: " + str(highestInterestLevel))
        # print(mostInterestingTaggedWords)

    answerNoQuestionPhraseWords = [word for word in mostInterestingTaggedWords if not word[0] in questionPhraseTokens]
    answerPhraseWords = [word for word in answerNoQuestionPhraseWords if not stemmer.stem(word[0]) in queryPhraseTokens]

    answerTokens = []

    for answerCandidate in answerPhraseWords:
        if answerCandidate[1] in answerTypes:
            answerTokens.append(answerCandidate)
    # print( "answer tokens: ")
    # print( answerTokens)


    # answer pattern match
    answerPatternIndex = 0
    stillMatch = False
    fullMatch = False

    answerWords = []
    answerDict = {}

    if len(answerPattern) == 0:
        answerWords = answerTokens
    else:
        # print("PROGRAM REACHED HERE")
        for aToken in answerTokens:
            # print("answerpattern index " + str(answerPatternIndex))
            if aToken[1] == answerPattern[answerPatternIndex]:
                # print("matched token with pattern " + aToken[0])
                stillMatch = True
                answerWords.append(aToken[0])
                answerPatternIndex += 1
            else:
                stillMatch = False
                answerWords = []
                answerPatternIndex = 0

                # check to see if pattern starts over
                if aToken[1] == answerPattern[answerPatternIndex]:
                    stillMath = True
                    answerWords.append(aToken[0])
                    answerPatternIndex += 1

            if stillMatch == True:
                if answerPatternIndex >= len(answerPattern):
                    # we have a full match
                    fullMatch = True
                    break

        if fullMatch == True:
            # print("full match with ")
            answerDict["answerWords"] = answerWords
            answerDict["fullSentence"] = str(mostInterestingSentence)
            # print("[SYSTEM] ", end = '' + str(answerWords))
            print(answerDict)
            return answerDict


if __name__ == "__main__":
    main()
