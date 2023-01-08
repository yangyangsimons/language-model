import copy
import nltk
from nltk.util import ngrams
from nltk.corpus import wordnet
from nltk.corpus import brown
import tkinter as tk
import random
import sys

class Blackboard:

    def __init__(self):
        self.window = tk.Tk()
        self.window.resizable(False,False)
        self.canvas = tk.Canvas(self.window,width=1000,height=1000)
        self.canvas.pack()

        self.lines = []
        self.lines.append([random.randint(10,700),random.randint(10,950), \
                           "Once there was a dog and a cat","l0"])
        self.lines.append([random.randint(10,700),random.randint(10,950), \
                           "Who decided to have an extended natter","l1"])
        # self.lines.append([random.randint(10,700),random.randint(10,950), \
        #                    "It's the best part of the day, morning light sliding", \
        #                    "l2"])
        # self.lines.append([random.randint(10,700),random.randint(10,950), \
        #                    "down rooftops, treetops, the birds pulling themselves", \
        #                    "l3"])
        # self.lines.append([random.randint(10,700),random.randint(10,950), \
        #                    "up out of whatever stupor darkened their wings", \
        #                    "l4"])
        # self.lines.append([random.randint(10,700),random.randint(10,950), \
        #                    "night still in their throats", \
        #                    "l5"])

        for ll in self.lines:
            self.canvas.create_text(ll[0],ll[1],text=ll[2],tags=ll[3], anchor=tk.W)
        #self.agentList = [removeAdjective,replaceWithSynonym,replaceWithAntonym,repairAAn,makeTwoLinesRhyme]
        self.agentList = [addSensibleAdjective]
        #self.agentList = [makeTwoLinesRhymeAndMakeSense,correctPositions,removeAdjective,repairAAn,\
        #                  replaceWithSynonym,replaceWithAntonym,addSensibleAdjective,removeMultipleAdjectives]
        
    def run(self):
        print("*** in run")
        print(self.lines)
        print(len(self.lines))
        ag = random.choice(self.agentList)
        print("executing ",ag)
        self.lines = ag(self.lines)
        self.canvas.delete("all")
        for ll in self.lines:
            self.canvas.create_text(ll[0],ll[1],text=ll[2],tags=ll[3],anchor=tk.W)
        self.canvas.after(10,Blackboard.run,self)

    def main(self):
        self.run()
        self.window.mainloop()

def removeAdjective(lines):
    ll = lines.pop(random.randrange(len(lines)))
    tagged = nltk.pos_tag(nltk.word_tokenize(ll[2]))
    adjList = []
    for idx,val in enumerate(tagged):
        if val[1]=="JJ":
            adjList.append(idx)
    print("Adjective List is ",adjList)
    if adjList:
        del tagged[random.choice(adjList)]
    newLine = " ".join([ x[0] for x in tagged ])
    #print(newLine)
    lines.append([ll[0],ll[1],newLine,ll[3]])
    return lines

def makeTwoLinesRhyme(lines):
    ll1 = lines.pop(random.randrange(len(lines)))
    ll2 = lines.pop(random.randrange(len(lines)))
    lastWord1 = nltk.word_tokenize(ll1[2])[-1]
    lastWord2 = nltk.word_tokenize(ll2[2])[-1]
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == lastWord1]
    rhymes = []
    #level = random.randrange(1,3)
    level = 2
    for (word, syllable) in syllables:
        rhymes += [word for word, pronunciation in entries if pronunciation[-level:] == syllable[-level:]]
    print("rhymes with ",lastWord1)
    print(rhymes[0:10])

    if rhymes:
        newTokens = list(nltk.word_tokenize(ll2[2])[:-1])
        newTokens.append(random.choice(rhymes))
        newLine = " ".join(newTokens)
        lines.append([ll1[0],ll1[1],ll1[2],ll1[3]])
        if random.random()<0.5:
            lines.append([ll1[0],ll1[1]+20,newLine,ll2[3]])
        else:
            lines.append([ll1[0],ll1[1]-20,newLine,ll2[3]])
    else:
        lines.append(ll1)
        lines.append(ll2)
    return lines


def makeTwoLinesRhymeAndMakeSense(lines):
    ll1 = lines.pop(random.randrange(len(lines)))
    ll2 = lines.pop(random.randrange(len(lines)))
    lastWord1 = nltk.word_tokenize(ll1[2])[-1]
    lastWord2 = nltk.word_tokenize(ll2[2])[-1]
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == lastWord1]
    rhymes = []
    level = random.randrange(1,3)
    #level = 2
    for (word, syllable) in syllables:
        rhymes += [word for word, pronunciation in entries if pronunciation[-level:] == syllable[-level:]]
    print("rhymes with ",lastWord1)
    print(rhymes[0:10])

    synonyms = []
    for syn in wordnet.synsets(lastWord2):
        for l in syn.lemmas():
            synonyms.append(l.name())
    print("means ",lastWord2)
    print(set(synonyms[0:10]))

    synonymsThatRhyme = list(set(synonyms).intersection(set(rhymes)))
    if synonymsThatRhyme:
        newTokens = list(nltk.word_tokenize(ll2[2])[:-1])
        newTokens.append(random.choice(synonymsThatRhyme))
        newLine = " ".join(newTokens)
        lines.append([ll1[0],ll1[1],ll1[2],ll1[3]])
        if random.random()<0.5:
            lines.append([ll1[0],ll1[1]+20,newLine,ll2[3]])
        else:
            lines.append([ll1[0],ll1[1]-20,newLine,ll2[3]])
    else:
        lines.append(ll1)
        lines.append(ll2)
    return lines

def repairAAn(lines):
    newLines = []
    for ll in lines:
        tokens = nltk.word_tokenize(ll[2])
        for idx,tok in enumerate(tokens[:-1]):
            if tok=="a":
                if (tokens[idx+1])[0] in "aeiou":
                    tokens[idx] = "an"
            if tok=="an":
                if (tokens[idx+1])[0] not in "aeiou":
                    tokens[idx] = "an"
        newLine = " ".join(tokens)
        newLines.append([ll[0],ll[1],newLine,ll[3]])
    return newLines

def replaceWithSynonym(lines):
    ll = lines.pop(random.randrange(len(lines)))
    tokens = nltk.word_tokenize(ll[2])
    wordIdx = random.randrange(len(tokens))
    wordToBeReplaced = tokens[wordIdx]
    synonyms = []
    for syn in wordnet.synsets(wordToBeReplaced):
        for l in syn.lemmas():
            if not "_" in l.name():
                synonyms.append(l.name())
    if synonyms:
        tokens[wordIdx] = random.choice(synonyms)
    else:
        tokens[wordIdx] = wordToBeReplaced
    newLine = " ".join(tokens)
    lines.append([ll[0],ll[1],newLine,ll[3]])
    return lines

def replaceWithAntonym(lines):
    ll = lines.pop(random.randrange(len(lines)))
    tokens = nltk.word_tokenize(ll[2])
    wordIdx = random.randrange(len(tokens))
    wordToBeReplaced = tokens[wordIdx]
    antonyms = []
    for syn in wordnet.synsets(wordToBeReplaced):
        for l in syn.lemmas():
            if l.antonyms() and not "_" in l.name():
                antonyms.append(l.antonyms()[0].name())
    if antonyms:
        tokens[wordIdx] = random.choice(antonyms)
    else:
        tokens[wordIdx] = wordToBeReplaced
    newLine = " ".join(tokens)
    lines.append([ll[0],ll[1],newLine,ll[3]])
    return lines

def addSensibleAdjective(lines):
    originalLines = copy.deepcopy(lines)
    ll = lines.pop(random.randrange(len(lines)))
    tokenized = nltk.word_tokenize(ll[2])
    tagged = nltk.pos_tag(tokenized)
    nounPositions = [idx for idx,val in enumerate(tagged) if val[1]=="NN"]
    if not nounPositions:
        return originalLines
    chosenNounPosition = random.choice(nounPositions)
    chosenNoun = tagged[chosenNounPosition][0]
    print(chosenNoun)
    ##now add the adjective
    bigrams = ngrams(brown.words(), 2)
    preWords = [ bg[0] for bg in bigrams if bg[1]==chosenNoun]
    taggedPreWords = nltk.pos_tag(preWords)
    print(taggedPreWords)
    chosenPreWords = [ pw[0] for pw in taggedPreWords if (pw[1]=="JJ") ] #VBN #NN
    print(chosenPreWords)
    if not chosenPreWords:
        return originalLines
    chosenDescriptor = random.choice(chosenPreWords)
    tokenized.insert(chosenNounPosition, chosenDescriptor)
    newLine = " ".join(tokenized)
    lines.append([ll[0],ll[1],newLine,ll[3]])
    return lines

def removeMultipleAdjectives(lines):
    newLines = []
    for ll in lines:
        tokens = nltk.word_tokenize(ll[2])
        tagged = nltk.pos_tag(tokens)
        markForDeletion = []
        prevType = tagged[1][1]
        for idx,pair in tagged:
            if prevType=="JJ" and pair[1]=="JJ":
                markForDeletion.append(idx)
        for idx in sorted(markForDeletion, reverse=True):
            del tokens[idx]
        newLine = " ".join(tokens)       
        newLines.append([ll[0],ll[1],newLine,ll[3]])
    return newLines

def correctPositions(lines):
    newLines = []
    for ll in lines:
        if ll[1]>900:
            newLines.append([ll[0],random.randrange(10,800),ll[2],ll[3]])
        else:
            newLines.append(ll)
    return newLines

bb = Blackboard()
bb.main()
