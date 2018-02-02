import math
import nltk
import time

# Constants to be used by you when you fill the functions
START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
MINUS_INFINITY_SENTENCE_LOG_PROB = -1000

# TODO: IMPLEMENT THIS FUNCTION
# Calculates unigram, bigram, and trigram probabilities given a training corpus
# training_corpus: is a list of the sentences. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function outputs three python dictionaries, where the keys are tuples expressing the ngram and the value is the log probability of that ngram
def calc_probabilities(training_corpus):

     bigram_p = {}
     bigram_c = {}
     trigram_p = {}
     trigram_c = {}
     unigram_p = {}
     unigram_c = {}
     
     total_uni=0
     last_unigram = ""
     last_bigram = ""
     dict1=[]
     dict2=[]
     totale=0
     for item in training_corpus:
           item = START_SYMBOL+" "+START_SYMBOL+ " " + item + " " + STOP_SYMBOL
           dict1.append(item)
     
     for item  in dict1:
          tokens =item.split()
          for index  in range(2,len(tokens)):
               unigram= (tokens[index],)
               if unigram != START_SYMBOL:
                    total_uni+=1 
                    if unigram in unigram_p:
                         unigram_p[unigram]+=1
                         unigram_c[unigram]+=1
                    else:
                         unigram_p[unigram]=1
                         unigram_c[unigram]=1
               bigram=(tokens[index-1],tokens[index])
               if bigram != ("*","*"):
                    if bigram in bigram_p:
                         bigram_p[bigram]+=1
                         bigram_c[bigram]+=1
                    else:
                         bigram_p[bigram]=1
                         bigram_c[bigram]=1
               trigram=(tokens[index-2],tokens[index-1],tokens[index])
               if trigram in trigram_p:
                    trigram_p[trigram]+=1
                    trigram_c[trigram]+=1
               else:
                    trigram_p[trigram]=1
                    trigram_c[trigram]=1
                     
     for item in set(unigram_p):
         unigram_p[item]=math.log((unigram_p[item]),2) - math.log(total_uni,2)
     for keys in bigram_c:
          if keys[0] == START_SYMBOL:
               bigram_p[keys]=math.log(bigram_c[keys],2)- math.log(len(training_corpus),2)
          else:
               bigram_p[keys]=math.log(bigram_c[keys],2)-math.log(unigram_c[(keys[0]),],2)
     for key in trigram_c:
         if key[0] == START_SYMBOL and key[1] == START_SYMBOL:
             trigram_p[key]=math.log(trigram_c[key],2)-math.log(len(training_corpus),2)
         else: 
             trigram_p[key]=math.log(trigram_c[key],2)-math.log(bigram_c[(key[0],key[1])],2)

#     print total_uni
     return unigram_p, bigram_p, trigram_p

# Prints the output for q1
# Each input is a python dictionary where keys are a tuple expressing the ngram, and the value is the log probability of that ngram
def q1_output(unigrams, bigrams, trigrams, filename):
    # output probabilities
    outfile = open(filename, 'w')

    unigrams_keys = unigrams.keys()
    unigrams_keys.sort()
    for unigram in unigrams_keys:
        outfile.write('UNIGRAM ' + unigram[0] + ' ' + str(unigrams[unigram]) + '\n')

    bigrams_keys = bigrams.keys()
    bigrams_keys.sort()
    for bigram in bigrams_keys:
        outfile.write('BIGRAM ' + bigram[0] + ' ' + bigram[1]  + ' ' + str(bigrams[bigram]) + '\n')

    trigrams_keys = trigrams.keys()
    trigrams_keys.sort()     
    for trigram in trigrams_keys:
        outfile.write('TRIGRAM ' + trigram[0] + ' ' + trigram[1] + ' ' + trigram[2] + ' ' + str(trigrams[trigram]) + '\n')

    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Calculates scores (log probabilities) for every sentence
# ngram_p: python dictionary of probabilities of uni-, bi- and trigrams.
# n: size of the ngram you want to use to compute probabilities
# corpus: list of sentences to score. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function must return a python list of scores, where the first element is the score of the first sentence, etc. 
def score(ngram_p, n, corpus):
     score=[]
     
     # if n ==1:
     #      for tokens in corpus:
     #          l_dvp=0.0 
     #          for index in range(len(corpus)-1):
                   
     #               for token in corpus[index].strip().split():
     #                   l_dvp +=ngram_p[(token),]
     #          l_dvp+=ngram_p[(STOP_SYMBOL),]
     #          score.append(l_dvp)
    
     # if n == 7:
     #     for line in corpus:
     #         l_sc=0.0
     #         tokens=[]
     #         tokens=tokens+(nltk.word_tokenize(line))
     #         tokens=tokens+[STOP_SYMBOL]
     #         state =False
     #         for i  in range(0,len(tokens)):
     #             key=(tokens[i],)
     #            # for j in range(i,i+n):
     #             if key in ngram_p:
     #                 l_sc+=ngram_p.get((key),0)
     #                 state = False
     #             else:
     #                  state = True
     #         if state:
     #             score.append(l_sc)
     #         else:
     #             score.append(-1000)
            


    #  count=0
     for line in corpus:
         l_score=0.0
         tokens=[]
         if n == 2:
             tokens+=[START_SYMBOL]
         if n == 3:
             tokens+=[START_SYMBOL]
             tokens+=[START_SYMBOL]
         tokens =tokens+(nltk.word_tokenize(line))+[STOP_SYMBOL]
        # tokens =tokens+[STOP_SYMBOL]
        # state= False
         for i in range(0,len(tokens)-n+1):
               # in this line
             tok=()
             for j in range(i,i+n):
                 tok+=(tokens[j],)
             l_score+=ngram_p.get((tok),0)
   
         score.append(l_score)
   #        else:
   #            score.append(-1000)
     return score

# Outputs a score to a file
# scores: list of scores
# filename: is the output file name
def score_output(scores, filename):
    outfile = open(filename, 'w')
    for score in scores:
        outfile.write(str(score) + '\n')
    outfile.close()

# TODO: IMPLEMENT THIS FUNCTION
# Calculates scores (log probabilities) for every sentence with a linearly interpolated model
# Each ngram argument is a python dictionary where the keys are tuples that express an ngram and the value is the log probability of that ngram
# Like score(), this function returns a python list of scores
def linearscore(unigrams, bigrams, trigrams, corpus):
    mlambda=1/3
    dict3=[]
  
    scores=[]
    for sentence in corpus:
        tokens=nltk.word_tokenize(sentence)
        tokens=['*','*']+tokens+[STOP_SYMBOL]
        tri_p=tuple(nltk.trigrams(tokens))
        
        state= False

        pro=0.0
        for trigra in tri_p:
             unigra = (trigra[2],)
             bigra=(trigra[1],trigra[2])
             
             
            # newtri=(1/3)*(bigra+unigra+trigra)
             
             
             if unigra in unigrams:
                  uni_pob=2**(unigrams[unigra])
             else:
                  uni_pob=0.0
             if trigra in trigrams:
                  tri_pob=2**(trigrams[trigra])
             else:
                  tri_pob=0.0
             if bigra in bigrams:
                  bi_pob=2**bigrams[bigra]
             else:
                  bi_pob= 0.0


             probb=(uni_pob+bi_pob+tri_pob)
             if probb  == 0.0:
                  state = True
             else:
                  
                  pro+=math.log(probb,2)-math.log(3.0,2)
        if state:
            scores.append(-1000)
        else:
            scores.append(pro.real)
    
    return scores

# convert log to probability   
DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

# DO NOT MODIFY THE MAIN FUNCTION
def main():
    # start timer
    time.clock()

    # get data
    infile = open(DATA_PATH + 'Brown_train.txt', 'r')
    corpus = infile.readlines()
    infile.close()

    # calculate ngram probabilities (question 1)
    unigrams, bigrams, trigrams = calc_probabilities(corpus)
    
#    print unigrams[("natural"),]    
 #   print bigrams[("natural","that")]
  #  print trigrams[("natural","that","he")]
   

    # question 1 output
    q1_output(unigrams, bigrams, trigrams, OUTPUT_PATH + 'A1.txt')

    # score sentences (question 2)
    uniscores = score(unigrams, 1, corpus)
    biscores = score(bigrams, 2, corpus)
    triscores = score(trigrams, 3, corpus)

    # question 2 output
    score_output(uniscores, OUTPUT_PATH + 'A2.uni.txt')
    score_output(biscores, OUTPUT_PATH + 'A2.bi.txt')
    score_output(triscores, OUTPUT_PATH + 'A2.tri.txt')

    # linear interpolation (question 3)
    linearscores = linearscore(unigrams, bigrams, trigrams, corpus)

    # question 3 output
    score_output(linearscores, OUTPUT_PATH + 'A3.txt')

    # open Sample1 and Sample2 (question 5)
    infile = open(DATA_PATH + 'Sample1.txt', 'r')
    sample1 = infile.readlines()
    infile.close()
    infile = open(DATA_PATH + 'Sample2.txt', 'r')
    sample2 = infile.readlines()
    infile.close() 

    # score the samples
    sample1scores = linearscore(unigrams, bigrams, trigrams, sample1)
    sample2scores = linearscore(unigrams, bigrams, trigrams, sample2)

    # question 5 output
    score_output(sample1scores, OUTPUT_PATH + 'Sample1_scored.txt')
    score_output(sample2scores, OUTPUT_PATH + 'Sample2_scored.txt')

    # print total time to run Part A
    print "Part A time: " + str(time.clock()) + ' sec'

if __name__ == "__main__": main()
