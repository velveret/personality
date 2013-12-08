from word import WordExtractor
import sys
import cPickle as pickle
import nltk
import math
import re
reload(sys)
from collections import defaultdict
import csv


sys.setdefaultencoding('utf-8')
import string

wordlist = ['sleep', 'hate', 'tired', 'even', 'ever', 'never', 'tell', 'something', 'want', 'still', 'better', 'always', 'house', 'really', 
'put', 'could', 'think', 'feel', 'miss', 'tomorrow', 'little', 'anyone', 'bed', 
'need', 'nothing', 'away', 'pretty', 'hope', 'watching', 'bad', 'please', 'ill',
'yay', 'much',  'cant', 'someone', 'like', 'right',
 'old', 'people', 'everything', 'oh', 'wish', 'sick','stupid','fucking','really','feeling','felt','shit','fuck','slept','sleepless']

scorelist = defaultdict()


for w in wordlist:
    scorelist[w] = 1
    
print scorelist.items()

# Word splitter pattern
pattern_split = re.compile(r"\W+")

record_score = []

class NeuroScore:

    def __init__(self,pickle_file):
        self.doc = WordExtractor(pickle_file)
        
        

    

    def score_process(self):
        row = 0 
        user_score = 0 
        line = 0
        for status in self.doc._statuses[1:]:
            line +=1
            print line
            
            print int(status[3])
            
            # row: representing row number of a user's status
            if row < int(status[3]):
            
                
                score = 0
                print row
                #print status
                #print self.doc._statuses[row]
            
                filtered_text = status[1].translate(string.maketrans("",""), string.punctuation)
            
                words = pattern_split.split(filtered_text.lower())
                # get afinn score for each word in the status
                scores = map(lambda word: scorelist.get(word, 0), words)
                if scores:
            
                    # Use sqrt(N) to weight each word
                    score = float(sum(scores))/math.sqrt(len(scores))
                else:
                    score = 0
                
                user_score += score
                row +=1
                if row == int(status[3]):
                               
                    record_score.append([status[0], str(float(user_score)/int(status[3]))])
                    print user_score
                    print float(user_score)/int(status[3])
                    row =0
                    user_score = 0
                    print "Clear user_score"
                
                continue
                
            
                
                #print the afinn score for the sentence
                #print self.doc._statuses[row][6]
        #return a dictionary with user id and average neurotic score per user
        return record_score
        
    def write_csv(self):
        with open('neuroscore.csv', 'wb') as csvfile:
            neuroscore = csv.writer(csvfile, delimiter = ',', quotechar='', quoting=csv.QUOTE_NONE)
        
            for row in record_score:
                neuroscore.writerow(row)        
        
        return None
    




if __name__ == '__main__':
    if (len(sys.argv) == 1):
        usage()
        sys.exit()
    
    scorer = NeuroScore(sys.argv[1])
    scorer.score_process()
    scorer.write_csv()
   # print scorer.word_score()
    