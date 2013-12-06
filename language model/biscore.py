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
from word import WordExtractor
from biword import BiWordExtractor


biwordlist = [('felt', 'like'), ('love', 'guys'), ('im', 'home'), ('want', 'back'), 
('fly', 'black'), ('d', '3'), ('feels', 'like'), ('best', 'friend'), ('getting', 'ready'), 
('think', 'might'), ('anyone', 'wanna'), ('fall', 'asleep'), ('im', 'tired'),('good', 'news'),
('getting', 'better'), ('something', 'like'), ('really', 'good'), ('im', 'already'),
('fell', 'asleep'), ('tomorrow', 'd'), ('im', 'looking'),
 ('pretty', 'good'), ('ill', 'never'), ('gotta', 'love'), ('anyone', 'else'), ('friday', 'night'),
('really', 'tired'), ('make', 'feel'), ('finally', 'done'), ('yet', 'another'), ('well', 'see'), 
('anyone', 'wants'), ('came', 'home'), ('people', 'think'), ('2', 'weeks'), ('act', 'like'), 
('last', 'week'), ('work', 'tonight'), ('im', 'crazy'), ('ice', 'cream'), ('true', 'friend'),
('im', 'sure'), ('holy', 'crap'), ('oh', 'well'), ('wait', 'til'), ('la', 'la'), ('fb', 'friends'),
('guess', 'ill'), ('maybe', 'ill'), ('im', 'starting'), ('thank', 'god'), ('first', 'time'),
('much', 'time'), ('christmas', 'everyone'), ('half', 'hour'), ('ive', 'never'), ('say', 'im'), 
('im', 'bored'), ('look', 'like'), ('good', 'morning'), ('d', 'd'), ('im', 'ready'), ('love', 'like'), 
('still', 'cant'), ('im', 'glad'), ('even', 'though'), ('im', 'getting'), ('want', 'see'),
('4', 'hours'), ('cant', 'see'), ('make', 'sense'), ('every', 'single'), ('never', 'thought'),
 ('black', 'guy'), ('really', 'wants'), ('really', 'really'), ('coming', 'home'), ('year', 'old'),
('video', 'games'), ('people', 'wont'), ('fuck', 'fuck'), ('love', 'much'), ('everyone', 'else'),
('nothing', 'like'), ('far', 'away'), ('two', 'hours'), ('please', 'put'), ('pretty', 'much'),
('good', 'luck'), ('sounds', 'like'), ('happy', 'thanksgiving'), ('everyone', 'birthday'),
('love', 'life'), ('wait', 'till'), ('feeling', 'good'), ('could', 'really'), ('great', 'time'),
('feel', 'good'), ('like', 'ill'), ('wont', 'let'), ('im', 'talking'), ('people', 'need'), 
('text', 'cell'), ('time', 'im'), ('living', 'room'), ('tomorrow', 'night'), ('sweet', 'dreams'),
('hours', 'sleep'), ('years', 'old'), ('3', 'love'), ('ill', 'tell'), ('long', 'time'), 
('cant', 'sleep'), ('im', 'sorry'), ('like', 'crap'), ('love', 'miss'), ('new', 'phone'), ('god', 'damn'), ('love', 'ya'),
('im', 'really'), ('really', 'like'), ('people', 'like'), ('people', 'say'), ('work', 'tomorrow'),
('anyone', 'want'), ('like', 'im'), ('im', 'proud'), ('new','years'), ('need', 'something'), 
('cuz', 'im'), ('looking', 'forward'), ('still', 'feel'), ('ready', 'work'), ('seems', 'like'),
('friends', 'list'), ('cant', 'stop'), ('make', 'sure'), ('tomorrow', 'im'), ('na', 'na'),
('makes', 'feel'), ('super', 'excited'), ('last', 'night'), ('facebook', 'friends'),
('never', 'let'), ('happy', 'new'), ('cant', 'wait'), ('fun', 'fun'), ('life', 'like'),
('havent', 'seen'), ('little', 'bit'), ('someone', 'else'), ('please', 'let'), ('need', 'help'), 
('two', 'weeks'), ('birthday', 'party'), ('least', 'hour'), ('much', 'fun'), ('spring', 'break'),
('nothing', 'else'), ('way', 'back'), ('lets', 'see'), ('im', 'actually'), ('im', 'feeling'), 
('back', 'work'), ('im', 'hungry'), ('lets', 'hope'), ('ive', 'seen'), ('im', 'afraid'), 
('wanna', 'see'), ('hope', 'everyone'), ('back', 'home'), ('cant', 'help'), ('much', 'love'), 
('almost', 'done'), ('last', 'name'), ('really', 'want'), ('3', '3'), ('id', 'like'),
('thats', 'right'), ('finally', 'finished'), ('ha', 'ha'), ('copy', 'paste'), ('nom', 'nom'),
('new', 'year'), ('waste', 'time'), ('home', 'tomorrow'), ('24', 'hours'),('really', 'bad'),
('good', 'times'), ('back', 'bed'), ('baby', 'girl'), ('trying', 'figure'), ('need', 'new'),
('ready', 'bed'), ('im', 'watching'), ('spend','time'), ('really', 'need'), ('think', 'need'), 
('wish', 'luck'), ('12', 'hours'), ('cant', 'seem'), ('put', 'see'), ('really', 'hate'), ('stuck', 'head'),
('school', 'tomorrow'), ('home', 'work'), ('im', 'pretty'), ('love', '3'), ('like','shit'), 
('cannot', 'wait'), ('good', 'friend'), ('thanks', 'everyone'), ('see', 'people'), 
('last', 'time'), ('cause', 'im'), ('well', 'guess'), ('feeling', 'like'), ('cant', 'stand'),
('feel', 'like'), ('im', 'trying'), ('woot', 'woot'),
('cell', 'phone'), ('person', 'like'), ('every', 'time'), ('well', 'im'), ('someone', 'please'), 
('birthday', 'wishes'), ('id', 'rather'), ('lady', 'gaga'), ('im', 'done'), ('marching', 'band'), 
('way', 'much'), ('3', 'hours'), ('hair', 'cut'), ('looks', 'like'), ('ive', 'ever'), ('need', 'sleep'),
('last', 'year'), ('ever', 'seen'), ('im', 'bed'), ('pretty', 'sure'), ('wont', 'copy'),
('back', 'school'), ('family', 'friends'), ('good', 'night'), ('love', 'love'), 
('think', 'ill'), ('high', 'school'), ('friends', 'family'), ('im', 'excited'), ('2', 'hours'),
('right', 'im'), ('love', 'someone'), ('im', 'thinking'), ('im', 'like'), ('new', 'york'),
('back', 'sleep'), ('im', 'love'), ('im', 'still'), ('coming', 'back'), ('im', 'back'), 
('true', 'blood'), ('makes', 'happy'), ('feel', 'free'),
('im', 'good'), ('think', 'im'), ('oh', 'yeah'), ('years', 'ago'), ('people', 'rate'), 
('wish', 'could'), ('think', 'ive'), ('time', 'bed'), ('life', 'good'),
('feel', 'bad'), ('smells', 'like'), ('im', 'finally'), ('hate', 'people'), ('feel', 'better'),
('like', 'crazy'), ('oh', 'god'), ('profile', 'picture'), ('cant', 'even'),
('tomorrow', 'morning'), ('im', 'sick'), ('wait', 'see'), ('much', 'better'), 
('happy', 'birthday'), ('im', 'happy'), ('cant', 'believe'), ('guess', 'im'), 
('blah', 'blah'), ('great', 'night'), ('best', 'friends'), ('put', 'someone'),
('1', 'fly'), ('theres', 'nothing'), ('thank', 'everyone'), ('good', 'time'), ('miss', 'much'), ('good', 'mood')]




scorelist = defaultdict()

for w in biwordlist:
    scorelist[w] = 1
    
print scorelist.items()

# Word splitter pattern
pattern_split = re.compile(r"\W+")

record_score = []

class NeuroBigramScore:

    def __init__(self,pickle_file):
        self.doc = WordExtractor(pickle_file)
        
       

    

    def score_process(self):
        row = 0 
        user_score = 0 
        line = 0
        for status in self.doc._statuses[1:]:
            line +=1
            #print line
            
           # print int(status[3])
            
            # row: representing row number of a user's status
            if row < int(status[3]):
            
                
                score = 0
                #print row
                #print status
                #print self.doc._statuses[row]
            
                filtered_text = status[1].translate(string.maketrans("",""), string.punctuation)
                            
                words = pattern_split.split(filtered_text.lower())
                
                bitokens = nltk.bigrams(words)
                # get neurotic score for each bigram in the status
                scores = map(lambda bitoken: scorelist.get(bitoken, 0), bitokens)
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
        with open('neuroscorebigram.csv', 'wb') as csvfile:
            neuroscorebigram = csv.writer(csvfile, delimiter = ',', quotechar='', quoting=csv.QUOTE_NONE)
        
            for row in record_score:
                neuroscorebigram.writerow(row)        
        
        return None
    

   



if __name__ == '__main__':
    if (len(sys.argv) == 1):
        usage()
        sys.exit()
    
    scorer = NeuroBigramScore(sys.argv[1])
    scorer.score_process()
    scorer.write_csv()
   # print scorer.word_score()
    