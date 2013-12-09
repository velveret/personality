import math
import re
import sys
reload(sys)
from word import WordExtractor
import cPickle as pickle
import nltk
sys.setdefaultencoding('utf-8')
import string
import csv
 
# AFINN-111 is as of June 2011 the most recent version of AFINN
filenameAFINN = 'AFINN/AFINN-111.txt'
afinn = dict(map(lambda (w, s): (w, int(s)), [ 
            ws.strip().split('\t') for ws in open(filenameAFINN) ]))
 
# Word splitter pattern
pattern_split = re.compile(r"\W+")

record_score = []



class AfinnScore:
    def __init__(self,pickle_file):
        self.doc = WordExtractor(pickle_file)
        
        
    def avg_afinn(self):
        """
        Returns a float for sentiment strength based on the input text.
        Positive values are positive valence, negative value are negative valence. 
        """
        row = 0 
        user_sentiment = 0 
        for status in self.doc._statuses[1:]:
            
            
            print int(status[3])
            
            # row: representing row number of a user's status
            if row < int(status[3]):
            
                
                sentiment = 0
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
                
                user_sentiment += sentiment
                row +=1
                if row == int(status[3]):
                               
                    record_score.append([status[0], str(float(user_sentiment)/int(status[3]))])
                    print user_sentiment
                    print float(user_sentiment)/int(status[3])
                    row =0
                    user_sentiment = 0
                    print "Clear user_sentiment"
                
                continue
                
            
                
                #print the afinn score for the sentence
                #print self.doc._statuses[row][6]
        #return a dictionary with user id and average afinn score per user
        return record_score
        
    def write_csv(self):
        with open('afinnscore.csv', 'wb') as csvfile:
            afinnscore = csv.writer(csvfile, delimiter = ',', quotechar='', quoting=csv.QUOTE_NONE)
        
            for row in record_score:
                afinnscore.writerow(row)        
        
        return None
 
 
if __name__ == '__main__':
    
    if (len(sys.argv) == 1):
        usage()
        sys.exit()
    
    scorer = AfinnScore(sys.argv[1])
    scorer.avg_afinn()
    scorer.write_csv()
   # print scorer.word_score()
 
    