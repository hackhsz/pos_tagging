import sys
import nltk
import math
import time
import itertools
from collections import Counter
from nltk.tokenize import word_tokenize
START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
RARE_SYMBOL = '_RARE_'
RARE_WORD_MAX_FREQ = 5
LOG_PROB_OF_ZERO = -1000


# TODO: IMPLEMENT THIS FUNCTION
# Receives a list of tagged sentences and processes each sentence to generate a list of words and a list of tags.
# Each sentence is a string of space separated "WORD/TAG" tokens, with a newline character in the end.
# Remember to include start and stop symbols in yout returned lists, as defined by the constants START_SYMBOL and STOP_SYMBOL.
# brown_words (the list of words) should be a list where every element is a list of the tags of a particular sentence.
# brown_tags (the list of tags) should be a list where every element is a list of the tags of a particular sentence.
def split_wordtags(brown_train):
    brown_words = []
    brown_tags = []
    for sentence in brown_train:
        sentence =START_SYMBOL+'/'+START_SYMBOL+" "+START_SYMBOL+'/'+ START_SYMBOL+" "+sentence+ " "+STOP_SYMBOL+'/'+STOP_SYMBOL
    # for sentence in a sentence lists
    for sentences in brown_train:
        tokens = sentences.split()
        #split into words
        tag = [] 
        words = []
        for tok in tokens:
            word = tok.rsplit('/',1)
            words.append(word[0])
            tag.append(word[1])
        brown_words.append(words)
        brown_tags.append(tag)

    return brown_words, brown_tags


# TODO: IMPLEMENT THIS FUNCTION
# This function takes tags from the training data and calculates tag trigram probabilities.
# It returns a python dictionary where the keys are tuples that represent the tag trigram, and the values are the log probability of that trigram
def calc_trigrams(brown_tags):
    q_values = {}
    trigram_c={}
    trigram_p={}
    bigram_c={}
    sent=[]
    for item in brown_tags:
        sent = [START_SYMBOL]+item+[STOP_SYMBOL]
        bigram = (tuple(nltk.bigrams(sent)))
        sent  = [START_SYMBOL]+sent
        trigram =(tuple(nltk.trigrams(sent)))
        for bigram in bigram:
            bigram_c[bigram]=bigram_c.get(bigram,0)+1
        for trigram in trigram:
            trigram_c[trigram]=trigram_c.get(trigram,0)+1
           #  else:
            #     trigram_c[each3]=1.0
        for items in trigram_c:
            if items[0]==START_SYMBOL and items[1]== START_SYMBOL:   
                q_values[items] = math.log(trigram_c[items],2).real-math.log(len(brown_tags),2).real
            else:
                q_values[items] = math.log(trigram_c[items],2).real-math.log(bigram_c[(items[0],items[1])],2).real
   














 # bigram_p={}
    # bigram_c={}
    # trigram_p={}
    # trigram_c={}
    # dict1=[]
    # for item in brown_tags:
    #     item = [START_SYMBOL]+[START_SYMBOL]+item+[STOP_SYMBOL]
    #     dict1.append(item)
    # for item in dict1:
    #     tokens=item.split()
    #     for index in range(2,len(tokens)):
    #         bigram=(tokens[index-1],tokens[index])
    #         if bigram!=("*","*"):
    #             if bigram in bigram_p:
    #                bigram_p[bigram]+=1
    #             else:
    #                bigram_p[bigram]=1
    #         trigram=(tokens[index-2],tokens[index-1],tokens[index])
    #         if trigram in trigram_p:
    #             trigram_p[trigram]+=1
    #         else:
    #             trigram_p[trigram]=1


    # for item in trigram_p:
    #     if item[0] == START_SYMBOL and item[1] == START_SYMBOL:
    #         q_values[item]=math.log(trigram_p[item],2)-math.log(len(brown_tags),2)
    #     else:
    #         q_values[item]=math.log(trigram_p[item],2)-math.log(bigram_p[(key[0],key[1])],2)
    return q_values

# This function takes output from calc_trigrams() and outputs it in the proper format
def q2_output(q_values, filename):
    outfile = open(filename, "w")
    trigrams = q_values.keys()
    trigrams.sort()  
    for trigram in trigrams:
        output = " ".join(['TRIGRAM', trigram[0], trigram[1], trigram[2], str(q_values[trigram])])
        outfile.write(output + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Takes the words from the training data and returns a set of all of the words that occur more than 5 times (use RARE_WORD_MAX_FREQ)
# brown_words is a python list where every element is a python list of the words of a particular sentence.
# Note: words that appear exactly 5 times should be considered rare!
def calc_known(brown_words):
    known_words = set([])
    jaja = {}
    
    for sentence in brown_words:
        
        for words in sentence:
            if words in jaja:
                jaja[words]+=1.0
            else:
                jaja[words]=1.0



    for word in jaja:
        if jaja[word]>5:
            known_words.add(word)
                     
        
    return known_words

# TODO: IMPLEMENT THIS FUNCTION
# Takes the words from the training data and a set of words that should not be replaced for '_RARE_'
# Returns the equivalent to brown_words but replacing the unknown words by '_RARE_' (use RARE_SYMBOL constant)
def replace_rare(brown_words, known_words):
    brown_words_rare = []
    
    for sentences in brown_words:
        sent=[]
        for token in sentences:
            if token not in known_words:
                sent.append('_RARE_')
            else:
                sent.append(token)
        
        brown_words_rare.append(sent)
    return brown_words_rare

# This function takes the ouput from replace_rare and outputs it to a file
def q3_output(rare, filename):
    outfile = open(filename, 'w')
    for sentence in rare:
        outfile.write(' '.join(sentence[2:-1]) + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Calculates emission probabilities and creates a set of all possible tags
# The first return value is a python dictionary where each key is a tuple in which the first element is a word
# and the second is a tag, and the value is the log probability of the emission of the word given the tag
# The second return value is a set of all possible tags for this data set
def calc_emission(brown_words_rare, brown_tags):
    dict1=[]
    e_values={}
    temp2dict={}
    taglist=set([])
    for sentence,item in zip(brown_words_rare,brown_tags):
        for wordsingle,tagsingle in zip(sentence,item):
            item=((wordsingle),(tagsingle))
            e_values[item]=e_values.get(item,0)+1.0
            if tagsingle in taglist:
                temp2dict[tagsingle]+=1.0
            else:
                taglist.add(tagsingle)
                temp2dict[tagsingle]=1.0
           
    for item in e_values:
        haha=math.log(e_values[item]/temp2dict[item[1]],2)
        e_values[item]=haha
    return e_values, taglist

# This function takes the output from calc_emissions() and outputs it
def q4_output(e_values, filename):
    outfile = open(filename, "w")
    emissions = e_values.keys()
    emissions.sort()  
    for item in emissions:
        output = " ".join([item[0], item[1], str(e_values[item])])
        outfile.write(output + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# This function takes data to tag (brown_dev_words), a set of all possible tags (taglist), a set of all known words (known_words),
# trigram probabilities (q_values) and emission probabilities (e_values) and outputs a list where every element is a tagged sentence 
# (in the WORD/TAG format, separated by spaces and with a newline in the end, just like our input tagged data)
# brown_dev_words is a python list where every element is a python list of the words of a particular sentence.
# taglist is a set of all possible tags
# known_words is a set of all known words
# q_values is from the return of calc_trigrams()
# e_values is from the return of calc_emissions()
# The return value is a list of tagged sentences in the format "WORD/TAG", separated by spaces. Each sentence is a string with a 
# terminal newline, not a list of tokens. Remember also that the output should not contain the "_RARE_" symbol, but rather the
# original words of the sentence!
def viterbi(brown_dev_words, taglist, known_words, q_values, e_values):
    appendlist={}
    tracking={}   
    tagged = []
    tracking[(-1,START_SYMBOL,START_SYMBOL)] = START_SYMBOL
    appendlist[(-1,START_SYMBOL,START_SYMBOL)] = 0.0
    for line in brown_dev_words:
        str1=" ";
        str2=" ".join(line)
        tokens_orig =  nltk.word_tokenize(str2)
        tokens=[]
        for words in tokens_orig:
            if words in known_words:
                tokens.append(words)
            else:
                tokens.append('_RARE')
       
        for item in taglist:
            appendlist[(0, START_SYMBOL, item)] = appendlist[(-1,START_SYMBOL,START_SYMBOL)] + q_values.get((START_SYMBOL, START_SYMBOL, item), -1000) + e_values.get((tokens[0], item), -1000)
            tracking[(0, START_SYMBOL, item)] = START_SYMBOL


        for (item, index) in itertools.product(taglist, taglist):
            key = (START_SYMBOL, item, index)
            appendlist[(1, item, index)] = appendlist.get((0,START_SYMBOL, item), -1000) + q_values.get(key, -1000) + e_values.get((tokens[1], index), -1000)
            tracking[(1, item, index)] = START_SYMBOL 

        for i in range (2, len(tokens)):
            for (index, value) in itertools.product(taglist, taglist):
                maxp = -float('Inf')
                maxt = ""
               # maxp = 0.0
                for item in taglist:
                    score = appendlist.get((i-1, item, index), -1000) + q_values.get((item,index,value), -1000) + e_values.get((tokens[i], value), -1000)
                    if(score > maxp):
                        maxp = score
                        maxt = item
                tracking[(i,index,value)] = maxt
                appendlist[(i,index,value)] = maxp

        maxp = -float('Inf')
       # maxp = 0.0

        for (index,value) in itertools.product(taglist,taglist):
            score = appendlist.get((len(tokens_orig)-1, index, value),-1000) + q_values.get((index,value,STOP_SYMBOL),-1000) 
            if score >  maxp:
                maxp = score
                max_index = index
                max_value = value
#append tags in reverse order
        tags = []
        tags.append(max_value)
        tags.append(max_index)
        temp1 = 0
        for j in range(len(tokens_orig) - 3, -1, -1):
            tags.append(tracking[(j + 2, tags[temp1+1], tags[temp1])])
            temp1 +=1
        tag_sent = ""
        tags.reverse()

        for i in range(0, len(tokens_orig)):
            tag_sent = tag_sent + tokens_orig[i] + "/" + str(tags[i]) + " "
        tag_sent += "\n"
        tagged.append(tag_sent)
    return tagged

# This function takes the output of viterbi() and outputs it to file
def q5_output(tagged, filename):
    outfile = open(filename, 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()

# TODO: IMPLEMENT THIS FUNCTION
# This function uses nltk to create the taggers described in question 6
# brown_words and brown_tags is the data to be used in training
# brown_dev_words is the data that should be tagged
# The return value is a list of tagged sentences in the format "WORD/TAG", separated by spaces. Each sentence is a string with a 
# terminal newline, not a list of tokens. 
def nltk_tagger(brown_words, brown_tags, brown_dev_words):
    # # Hint: use the following line to format data to what NLTK expects for training
    training = [ zip(brown_words[i],brown_tags[i]) for i in xrange(len(brown_words)) ]

    # # IMPLEMENT THE REST OF THE FUNCTION HERE
    tagged = []

    default_tag = nltk.DefaultTagger('NOUN')
    





    return tagged

# This function takes the output of nltk_tagger() and outputs it to file
def q6_output(tagged, filename):
    outfile = open(filename, 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()

DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

def main():
    # start timer
    time.clock()

    # open Brown training data
    infile = open(DATA_PATH + "Brown_tagged_train.txt", "r")
    brown_train = infile.readlines()
    infile.close()

    # split words and tags, and add start and stop symbols (question 1)
    brown_words, brown_tags = split_wordtags(brown_train)

    # calculate tag trigram probabilities (question 2)
    q_values = calc_trigrams(brown_tags)

    # question 2 output
    q2_output(q_values, OUTPUT_PATH + 'B2.txt')

    # calculate list of words with count > 5 (question 3)
    known_words = calc_known(brown_words)

    # get a version of brown_words with rare words replace with '_RARE_' (question 3)
    brown_words_rare = replace_rare(brown_words, known_words)

    # question 3 output
    q3_output(brown_words_rare, OUTPUT_PATH + "B3.txt")

    # calculate emission probabilities (question 4)
    e_values, taglist = calc_emission(brown_words_rare, brown_tags)

    # question 4 output
    q4_output(e_values, OUTPUT_PATH + "B4.txt")

    # delete unneceessary data
    del brown_train
    del brown_words_rare

    # open Brown development data (question 5)
    infile = open(DATA_PATH + "Brown_dev.txt", "r")
    brown_dev = infile.readlines()
    infile.close()

    # format Brown development data here
    brown_dev_words = []
    for sentence in brown_dev:
        brown_dev_words.append(sentence.split(" ")[:-1])

    # do viterbi on brown_dev_words (question 5)
    viterbi_tagged = viterbi(brown_dev_words, taglist, known_words, q_values, e_values)

    # question 5 output
    q5_output(viterbi_tagged, OUTPUT_PATH + 'B5.txt')

    # do nltk tagging here
    nltk_tagged = nltk_tagger(brown_words, brown_tags, brown_dev_words)

    # question 6 output
    q6_output(nltk_tagged, OUTPUT_PATH + 'B6.txt')

    # print total time to run Part B
    print "Part B time: " + str(time.clock()) + ' sec'

if __name__ == "__main__": main()
