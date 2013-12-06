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

class WordExtractor:

    def __init__(self, pickle_file):
        self._statuses = pickle.load(open(pickle_file, 'rb'))
        self._averages = dict()
        self._gender_stats = dict()
        self.fdistneuro = FreqDist()
        self.fdistnonneuro = FreqDist()
        self.highneuro = defaultdict()
        self.highnonneuro =defaultdict()
        
        self.f = defaultdict(float)
        self.g = defaultdict(float)
        self.wordlist = []
        
        

    """
    Processes statuses. (For information on how the different data structures
    are set up, look at the comments for the getters.)
    """

    
    def wordprocess(self):
        lengths = dict()
        line = 0
        for status in self._statuses[1:]:
            line +=1
            print line
            user = status[0]
            filtered_status = status[1].translate(string.maketrans("",""), string.punctuation)
            
            tokens = pattern_split.split(filtered_status.lower())
            
            
            # filter out stopwords and emoticons
            filtered_tokens = [w for w in tokens if w not in stopwordslist and w not in filterlist]
            
            if status[5] == '+':
                self.fdistneuro.update(filtered_tokens) 
            elif status[5] == '-':
                self.fdistnonneuro.update(filtered_tokens)            
            
     
                

                

       

    
    #returns most frequently used words by neurotic person
    def neuro_word_frequency(self):
        vocneuro= self.fdistneuro.keys()
        highvocneuro = vocneuro [:500]
        return highvocneuro
        
    #returns most frequently used words by non-neurotic person    
    def nonneuro_word_frequency(self):
        
        vocnonneuro = self.fdistnonneuro.keys()
        highvocnonneuro = vocnonneuro [:500]
        return highvocnonneuro

    

    def highneuro_word_frequency(self):
        for w in self.neuro_word_frequency():
            self.highneuro[w] =self.fdistneuro[w]
        return self.highneuro.items()
    
    
    
    def highnonneuro_word_frequency(self):
        for w in self.nonneuro_word_frequency():
            self.highnonneuro[w] =self.fdistnonneuro[w]
        return self.highnonneuro.items()
    
    def select_word(self):
        nntn = float(184563/1780098)
        ntnn = float(1780098/184563)
         
        

        for w in self.highneuro.keys():
            
            if w in self.highnonneuro.keys():
                self.f[w]= int(self.highneuro[w]-self.highnonneuro[w]*nntn)
                
                     
                

        print self.f.items()

        print "Start calculating non-neurotic words"
        for w in self.highnonneuro.keys():
            if w in self.highneuro.keys():
                self.g[w] = int(self.highnonneuro[w]-self.highneuro[w]*ntnn)
        
            else:
                print "False for %s" %(w)
                

        print self.g.items()
        
        for w in self.f.keys():
            if w in self.g.keys():
                if self.f[w]>=2000 and self.g[w]<=500:
                    self.wordlist.append(w)
    
        print "Here is the wordlist"
        print self.wordlist
        # return a list of words used relatively heavily by neurotic persons
        return self.wordlist
        
def usage():
    print """usage: python word.py [picklefile]
    [picklefile]: the name of the file containing the pickled statuses"""

if __name__ == '__main__':
    if (len(sys.argv) == 1):
        usage()
        sys.exit()
    
    extractor = WordExtractor(sys.argv[1])
    extractor.wordprocess()
    
    extractor.neuro_word_frequency()
    extractor.nonneuro_word_frequency()
    extractor.highneuro_word_frequency()
    extractor.highnonneuro_word_frequency()
    extractor.select_word()
    #print extractor.avg_token_length()
   # print extractor.highneuro_word_frequency()
    #print extractor.highnonneuro_word_frequency()