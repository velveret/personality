import math
import re
import sys
reload(sys)
from word import WordExtractor
import cPickle as pickle
import nltk
sys.setdefaultencoding('utf-8')
import string
 
# AFINN-111 is as of June 2011 the most recent version of AFINN
filenameAFINN = 'AFINN/AFINN-111.txt'
afinn = dict(map(lambda (w, s): (w, int(s)), [ 
            ws.strip().split('\t') for ws in open(filenameAFINN) ]))
 
# Word splitter pattern
pattern_split = re.compile(r"\W+")

class AfinnScore:
    def __init__(self,pickle_file):
        self.doc = WordExtractor(pickle_file)
        
    def sentiment(self):
        """
        Returns a float for sentiment strength based on the input text.
        Positive values are positive valence, negative value are negative valence. 
        """
        row = 0
        for status in self.doc._statuses[1:]:
            sentiment = 0
            # row: representing row number
            row += 1 
            print row
            #print status
            #print self.doc._statuses[row]
            
            filtered_text = status[1].translate(string.maketrans("",""), string.punctuation)
            
            words = pattern_split.split(filtered_text.lower())
            # get afinn score for each word in the status
            sentiments = map(lambda word: afinn.get(word, 0), words)
            if sentiments:
            
            # Use sqrt(N) to weight each word
                sentiment = float(sum(sentiments))/math.sqrt(len(sentiments))
            else:
                sentiment = 0
            
            self.doc._statuses[row].append(str(sentiment))
            #print the afinn score for the sentence
            print self.doc._statuses[row][6]
        #return a dictionary with all everything in the csv file plus the last column(with afinn scores)
        return self.doc._statuses
            
        
 
 
 
if __name__ == '__main__':
    
    if (len(sys.argv) == 1):
        usage()
        sys.exit()
    
    scorer = AfinnScore(sys.argv[1])
    scorer.sentiment()
   # print scorer.word_score()
 
    