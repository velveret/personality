import sys
import cPickle as pickle
import nltk
from nltk import FreqDist
from collections import defaultdict
import string
import re

stopwordslist = nltk.corpus.stopwords.words('english')

# filter the tokens below
filterlist = ['','group','propmale', 'propfemale', 'propfirst','go','find','day',
    'going','around','gonna','got','know','today','went','status','me','come','many','days',
    'keep','things','thing','one','next','would','get','take','u','doesnt','dont','didnt']

# Word splitter pattern
pattern_split = re.compile(r"\W+")


class BiWordExtractor:

    def __init__(self, pickle_file):
        self._statuses = pickle.load(open(pickle_file, 'rb'))
        self._averages = dict()
        self._gender_stats = dict()
        self.fdistneuro = FreqDist()
        self.fdistnonneuro = FreqDist()
        self.highneuro = defaultdict()
        self.highnonneuro =defaultdict()
        

    """
    Processes statuses. (For information on how the different data structures
    are set up, look at the comments for the getters.)
    """

    
    def wordprocess(self):
        lengths = dict()
        row = 0
        for status in self._statuses[1:]:
            row +=1
            print row
            user = status[0]
            
            filtered_status = status[1].translate(string.maketrans("",""), string.punctuation)
            
            tokens = pattern_split.split(filtered_status.lower())
            
            filtered_tokens = [w for w in tokens if w not in stopwordslist and w not in filterlist]
                        
            bitokens = nltk.bigrams(filtered_tokens)
            
            if status[5] == '+':
                self.fdistneuro.update(bitokens) 
            elif status[5] == '-':
                self.fdistnonneuro.update(bitokens)            
            
                
                

                

        

    

    def neuro_word_frequency(self):
        vocneuro= self.fdistneuro.keys()
        highvocneuro = vocneuro [:300]
        return highvocneuro
        
   

   

    def highneuro_word_frequency(self):
        for w in self.neuro_word_frequency():
            if self.fdistneuro[w]>= 5:
                self.highneuro[w] =self.fdistneuro[w]
            
        print self.highneuro.items()
        print self.highneuro.keys()
        return self.highneuro.keys()
    
    
    
   
    
    

def usage():
    print """usage: python basicfeatures.py [picklefile]
    [picklefile]: the name of the file containing the pickled statuses"""

if __name__ == '__main__':
    if (len(sys.argv) == 1):
        usage()
        sys.exit()
    
    extractor = BiWordExtractor(sys.argv[1])
    extractor.wordprocess()
    #print extractor.avg_token_length()
    extractor.neuro_word_frequency()
    extractor.highneuro_word_frequency()
    #print extractor.highnonneuro_word_frequency()