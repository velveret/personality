import sys
import cPickle as pickle
import nltk
from nltk import FreqDist
from collections import defaultdict
import string

stopwordslist = nltk.corpus.stopwords.words('english')

class WordExtractor:

    def __init__(self, pickle_file):
        self._statuses = pickle.load(open(pickle_file, 'rb'))
        self._averages = dict()
        self._gender_stats = dict()
        self.fdistneuro = FreqDist()
        self.fdistnonneuro = FreqDist()
        self.highneuro = defaultdict()
        self.highnonneuro =defaultdict()
        # filter the tokens below
        self.checklist=['<x>','?',':3', ':(', '=',  '(', ':D', ')',  "it's", '<propmale>','<propfemale>','<propfirst>'
            '(?', ';', '?)', "'s", '(*^?^*)', '(t', '+',
            ':p', ';o;', '<3', '=(???)=', '>___<;;', 'T)', '^', 'it.',  'x___X', 
            '&', '(-', ')?', '*', '-)', ':)', "<propfemale>'s", '(*>w<*)', '(-__-;;', '(-___-;;)', '(:V)',
            '(;____;)', '(;______;)', '(=____=)', '(>?<)', '(>__<;;)', '(>___<;;)', '(???',
            '(???;)', '(?_?;)', '(t___t)', '(^__~)', '(`',  '(o__o;;)','(of', '(the',
            '(x___X', '(x___X)', '(x____X)', '(x_____X)', '(x___x)', '(x___x;;)',
            ')"', ')/', ')=', "*????*:.?..?.:*?'(*???*)'?*:.?.", '*sigh*', '-->', '-____-;;',
            '.?.:*?', '.?.:*????*', ':("', ':-(', ':-D', '::hugs::', ':d"', ':p"', ':[', ':d', ';____;', ';_____;',
            '<<group', "<propfirst>'", '<propfirst>.', '<propmale>.', 
            '=(>?<', '=(^?^)=', '=^___^=', '=___=;', '=____=;;', '>__<;', '>____<;;"',
            '?(???;)?=3=3=3', '?*:.?.', '??...', '??;?', '???).', '??????...', '???????', '???????!!',
            '????????...', '?????????!', '?????????,', '?????????...', '??????????...', 
            '????????????...?', '??????????????????', 'D:', ':)','(:','(-:',':-)']
        self.filterlist = [w.lower() for w in self.checklist]

    """
    Processes statuses. (For information on how the different data structures
    are set up, look at the comments for the getters.)
    """

    
    def wordprocess(self):
        lengths = dict()
        for status in self._statuses[1:]:
            user = status[0]
            
            
            tokens = status[1].split()
            # filter out stopwords and emoticons
            filtered_tokens = [w.lower() for w in tokens if w.lower() not in stopwordslist and w.lower() not in self.filterlist]
            
            if status[5] == '+':
                self.fdistneuro.update(filtered_tokens) 
            elif status[5] == '-':
                self.fdistnonneuro.update(filtered_tokens)            
            
            
                

                

       

    

   
    #returns most frequently used words by neurotic person
    def neuro_word_frequency(self):
        vocneuro= self.fdistneuro.keys()
        highvocneuro = vocneuro [:150]
        return highvocneuro
        
    #returns most frequently used words by non-neurotic person    
    def nonneuro_word_frequency(self):
        
        vocnonneuro = self.fdistnonneuro.keys()
        highvocnonneuro = vocnonneuro [:150]
        return highvocnonneuro

    

    def highneuro_word_frequency(self):
        for w in self.neuro_word_frequency():
            self.highneuro[w] =self.fdistneuro[w]
        return self.highneuro.items()
    
    
    
    def highnonneuro_word_frequency(self):
        for w in self.nonneuro_word_frequency():
            self.highnonneuro[w] =self.fdistnonneuro[w]
        return self.highnonneuro.items()
    
    

def usage():
    print """usage: python basicfeatures.py [picklefile]
    [picklefile]: the name of the file containing the pickled statuses"""

if __name__ == '__main__':
    if (len(sys.argv) == 1):
        usage()
        sys.exit()
    
    extractor = WordExtractor(sys.argv[1])
    extractor.wordprocess()
    #print extractor.avg_token_length()
    print extractor.highneuro_word_frequency()
    print extractor.highnonneuro_word_frequency()