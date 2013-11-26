import re
import sys
import csv

if len(sys.argv) < 2:
  print len(sys.argv)
  print """USAGE: python splittraintest.py [all_input_files]"""
  sys.exit()

posFilename = "positive.csv"
negFilename = "negative.csv"
testFilename = "testdata.csv"
emojiCountFilename = "emojiCount.csv"
sep = ','
sep2 = '\t' # must be one character so add semicolon later

posf = open(posFilename, 'w')
negf = open(negFilename, 'w')
testf = open(testFilename, 'w')
emojiCountf = open(emojiCountFilename, 'w')

posout = csv.writer(posf, delimiter = sep2, quotechar='', escapechar='\\', quoting=csv.QUOTE_NONE)
negout = csv.writer(negf, delimiter = sep2, quotechar='', escapechar='\\', quoting=csv.QUOTE_NONE)
testout = csv.writer(testf, delimiter = sep2, quotechar='', escapechar='\\', quoting=csv.QUOTE_NONE)
emojiCountOut = csv.writer(emojiCountf, delimiter = sep2, quotechar='', escapechar='\\', quoting=csv.QUOTE_NONE)

happy = '[:=]-?\)'
sad = '[:=]-?\('
# happy = "is"
# sad = "to"
posCount = 0
negCount = 0
testCount = 0

for index in range(1, len(sys.argv)):
  inFilename = sys.argv[index]
  f= open(inFilename, 'rb')
  fin = csv.reader(f, delimiter = sep)
  
  line = 1
  for row in fin:
    if (line == 1):
      row.extend(["positive_emoji_count", "negative_emoji_count", "net_emoji_count"])
      emojiCountOut.writerow(row)
      line += 1
      continue
    # print row
    if len(row) == 0:
      line += 1
      continue
    if len(row) != 6:
      print "Malformatted line: %i; skipping." % line
      line += 1
      continue
    text = row[1]
    emojiPosCount = len(re.findall(happy, text))
    emojiNegCount = len(re.findall(sad, text))
    row.extend([emojiPosCount, emojiNegCount, emojiPosCount - emojiNegCount])
    if re.search(happy, text) != None and re.search(sad, text) == None:
      posout.writerow(row)
      posCount += 1
    elif re.search(sad, text) != None and re.search(happy, text) == None:
      negout.writerow(row)
      negCount += 1
    else:
      testout.writerow(row)
      testCount += 1
    emojiCountOut.writerow(row)
    line += 1
  f.close()
  
negf.close()
posf.close()
testf.close()
emojiCountf.close()
print "Finished splitting, with " + str(posCount) + " positive, " + str(negCount) + " negative, " + str(testCount) + " test"