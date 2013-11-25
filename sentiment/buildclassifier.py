#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import re
import sys
import time
import random
from time_limit import *
import traceback
from nltk.corpus import stopwords
from nltk import NaiveBayesClassifier
import nltk
import csv

##### GLOBALS FOR THE MODULE #####

classifier = None
masterfeats = None

##### CODE FOR FEATURE EXTRACTION FROM TWEET TEXT

punc_reducer = re.compile(r'(\W)\1+')
repeat_reducer = re.compile(r'(\w)\1{2,}')
punc_breaker_1 = re.compile(r'(\w{2,})(\W\s)')
punc_breaker_2 = re.compile(r'(\s\W)(\w{2,})')
punc_breaker_3 = re.compile(r'(\w{3,})(\W{2}\s)')
punc_breaker_4 = re.compile(r'(\s\W{2})(\w{3,})')
quote_replacer = re.compile(r'&quot;')
amp_replacer = re.compile(r'&amp;')
gt_replacer = re.compile(r'&gt;')
lt_replacer = re.compile(r'&lt;')
mention_replacer = re.compile(r'@\w+')
link_replacer = re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))')
#link_replacer = re2.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))')
caps_finder = re.compile(r'(\b[A-Z]{4,})\b')
lol_reducer = re.compile(r'\b[aeo]*h[aeo]+(h+[aeo]*)*\b|\bl(o+l+)+s*z*(e?d)?\b|\brofls*z*(e?d)?\b|\blu+l+s*z*(e?d)?\b|\blmf+a+o+\b')
stopwords_dict = [(x, True) for x in stopwords.words()]

def featurify(text, master = None):
  ext_tokens = []

  # replace "&quot;" with a double quote
  text = quote_replacer.sub(r'"', text)
  text = amp_replacer.sub(r'&', text)
  text = gt_replacer.sub(r'>', text)
  text = lt_replacer.sub(r'<', text)

  #print text

  # replace mentions with a dummy string
  (text, num) = mention_replacer.subn(r'', text)
  if num > 0:
    ext_tokens.append("<MENTION>")
  # replace links with a dummy string
  (text, num) = link_replacer.subn(r'', text)
  if num > 0:
    ext_tokens.append("<LINK>")
  # find words in all caps and add a dummy string to note that
  (text, num) = caps_finder.subn(r'\1', text)
  if num > 0:
    ext_tokens.append("<CAPS>")
  # find laughter and replace with a dummy string
  (text, num) = lol_reducer.subn(r'', text)
  if num > 0:
    ext_tokens.append("<LULZ>")

  # lowercase everything
  text = text.lower()

  # isolates and reduces long spans of repeated punctuation to a single item (like "...." / " !!!! " / "????")
  text = punc_reducer.sub(r' \1 ', text)
  # shorten long spans of repeated word chars to three ("soooooooo" ==> "sooo")
  text = repeat_reducer.sub(r'\1\1\1', text)
  # break single-character punctuation off of words of size 2 or more (quotes, exclaims, periods)
  text = punc_breaker_1.sub(r' \1 \2 ', text)
  text = punc_breaker_2.sub(r' \1 \2 ', text)
  # break double-character punctuation off of words of size 3 or more (quote-period, question-exclaim)
  text = punc_breaker_3.sub(r' \1 \2 ', text)
  text = punc_breaker_4.sub(r' \1 \2 ', text)

  # split on all whitespace
  tokens = re.split(r'\s+', text)
  # remove stopwords and blanks
  tokens = [x for x in tokens if len(x) > 0 and x not in stopwords_dict]
  # add in manual extra tokens
  tokens += ext_tokens

  #print tokens
  #print

  if master == None:
    feats = dict([(word, True) for word in tokens])
  else:
    feats = dict([(word, True) for word in tokens if word in master])

  # make the feature data structure
  return feats

##### IMPORT THE SENTIMENT CLASSIFIER #####

def load(classifierFile="classifier.pickle", featureFile="features.pickle"):
  global classifier
  global masterfeats
  try:
    print "Importing classifier (this takes a couple minutes)..."
    sys.stdout.flush()
    f = open(classifierFile, 'r')
    classifier = pickle.load(f)
    f.close()
    f = open(featureFile, 'r')
    masterfeats = pickle.load(f)
    f.close()
    print "Finished importing classifier!"
    sys.stdout.flush()
  except Exception:
    print "Failed!"
    print traceback.format_exc()
    sys.exit(1)
    
##### TRAIN AND SAVE A NEW SENTIMENT CLASSIFIER #####

def train(positiveFile='positive.csv', negativeFile='negative.csv', nOccurrences=25, trainProportion=0.9):
  files = [positiveFile, negativeFile]
  tweetfeats = []
  masterfeats = {}
  for fn in files:
    f = open(fn, 'r')
    theclass = "pos"
    if fn == negativeFile:
      theclass = "neg"
    sep = '\t'
    fin = csv.reader(f, delimiter = sep)
    for line in fin:
      text = line[1]
      # break up into tokens removing all non-word chars
      feat = featurify(text)
      for f in feat:
        if f in masterfeats:
          masterfeats[f] += 1
        else:
          masterfeats[f] = 0
      if len(feat) > 0:
        tweetfeats.append((feat, theclass))

  mfn = masterfeats.copy()
  for f in masterfeats:
    if masterfeats[f] < nOccurrences:
      del mfn[f]
  masterfeats = mfn
  f = open("features.lst", "w")
  f.write('\n'.join(list(masterfeats.keys())))
  f.close()
  print "Number of Features = %i" % len(masterfeats)

  train_cut = int(len(tweetfeats) * trainProportion)
  random.shuffle(tweetfeats)
  trainfeats = tweetfeats[:train_cut]
  testfeats = tweetfeats[train_cut:]

  print "Training sentiment classifier..."
  sys.stdout.flush()
  classifier = NaiveBayesClassifier.train(trainfeats)
  print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
  classifier.show_most_informative_features()
  sys.stdout.flush()

  # SAVE the classifier & features
  f = open("classifier.pickle", 'w')
  pickle.dump(classifier, f)
  f.close()
  f = open("features.pickle", 'w')
  pickle.dump(masterfeats, f)
  f.close()
  
##### FUNCTION TO CLASSIFY TWEET TEXT #####

def classify(text):
  try:
    # note: time limit/SIGALRM doesn't work on Windows
    # with time_limit(2):
      feat = featurify(text, masterfeats)
      result = classifier.prob_classify(feat)
      probs = dict([(x, result.prob(x)) for x in result.samples()])
      score = probs['pos'] * 2.0 - 1.0
      return score
  except TimeoutException:
    print "Featurify timed out for text %s" % text
    return 0.0

train()
