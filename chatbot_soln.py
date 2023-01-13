from pprint import pprint
import random
import nltk

knowledge = { ("person1", "name", "?"), \
             ("person1", "town", "?"),
             ("person1", "street", "?")
             }

active = True
while active:
    unknowns = { (person,fact,value) for (person,fact,value) \
                 in knowledge if value=="?" }
    #print("UNKNOWN:")
    #pprint(unknowns)
    #print("KNOWN:")
    #pprint(knowledge - unknowns)
    if unknowns: #is non-empty
        person, fact, value = random.choice(list(unknowns))
        question = "What is your "+fact+"? "
        knowledge.remove( (person,fact,value) )
        reply = input(question)
        if reply=="bye":
            active = False
            continue
        tokens = nltk.word_tokenize(reply)
        tagged = nltk.pos_tag(tokens)
        properNouns = [ word for (word, pos) in tagged if pos=="NNP" ]
        #print(tagged)
        #print(properNouns)
        if not properNouns:
            properNouns = [ word for (word, pos) in tagged if pos=="NN" ]
        knowledge.add( (person, fact, properNouns[0]) ) 
    else:
        question = "How can I help you? "
        helpRequest = input(question)
        if helpRequest =="bye":
            active = False
            continue
        tokens = nltk.word_tokenize(helpRequest)
        tagged = nltk.pos_tag(tokens)
        #print(tagged)
        verbs = [ word for (word, pos) in tagged if str.startswith(pos,"VB") ]
        #print(verbs)
        if any(item in ["buy", "order", "purchase"] for item in verbs):
            knowledge.add( ("person1", "want to buy", "?") )
        else:
            print("I cannot help you with that")
  
print()
print("Final knowledge base: ")
pprint(knowledge)
    
    
