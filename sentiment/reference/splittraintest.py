#!/usr/bin/python

import re
import sys
import csv

if len(sys.argv) < 3:
  print """USAGE: python splittraintest.py [all_input_files]"""
  sys.exit()

posFilename = "positive.csv"
negFilename = "negative.csv"
testFilename = "testdata.csv"
sep = '\t'
sep2 = '\t' # must be one character so add semicolon later

posf = open(posFilename, 'w')
negf = open(negFilename, 'w')
testf = open(testFilename, 'w')

posout = csv.writer(posf, delimiter = sep2, quotechar='', quoting=csv.QUOTE_NONE)
negout = csv.writer(negf, delimiter = sep2, quotechar='', quoting=csv.QUOTE_NONE)
testout = csv.writer(testf, delimiter = sep, quotechar='', quoting=csv.QUOTE_NONE)

happy = '[:|=]-?\)'
sad = '[:|=]-?\('
posCount = 0
negCount = 0
testCount = 0

for index in range(1, len(sys.argv)):
  inFilename = sys.argv[index]
  f= open(inFilename, 'rU')
  fin = csv.reader(f, delimiter = sep, quoting=csv.QUOTE_NONE)
  
  line = 1
  for row in fin:
    if len(row) == 0:
      continue
    if len(row) != 3:
      print "Malformatted line: %i; skipping." % line
      continue
    tweetID = row[0]
    text = row[2]
    if re.search(happy, text) != None and re.search(sad, text) == None:
      posout.writerow([tweetID, ';;'+text])
      posCount += 1
    elif re.search(sad, text) != None and re.search(happy, text) == None:
      negout.writerow([tweetID, ';;'+text])
      negCount += 1
    else:
      testout.writerow([tweetID, text])
      testCount += 1
    line += 1
  f.close()
  
negf.close()
posf.close()
testf.close()
print "Finished splitting, with " + str(posCount) + " positive, " + str(negCount) + " negative, " + str(testCount) + " test"
