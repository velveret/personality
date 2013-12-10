import re
import sys
import csv
import numpy

if len(sys.argv) < 4:
  print len(sys.argv)
  print """USAGE: python emojicount.py [input_file] [output_file] [is_test]"""
  sys.exit()

if (sys.argv[3] == "true"):
  is_test = True
else:
  is_test = False

emojiCountFilename = sys.argv[2]
sep = ','

emojiCountf = open(emojiCountFilename, 'w')
emojiCountOut = csv.writer(emojiCountf, delimiter = ",", quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)

happy = '[:=]-?\)'
sad = '[:=]-?\('

inFilename = sys.argv[1]
f= open(inFilename, 'rU')
fin = csv.reader(f, delimiter = sep)

userToPos = {}
userToNeg = {}
userToNet = {}
line = 1
for row in fin:
  if (line == 1):
    line += 1
    continue
  if len(row) == 0:
    line += 1
    continue
  if (not(is_test) and len(row) != 6) or (is_test and len(row) != 5):
    print "Malformatted line: %i; skipping." % line
    line += 1
    continue
  text = row[1]
  userId = row[0]
  if not(userId in userToNet):
    userToNet[userId] = []
    userToPos[userId] = []
    userToNeg[userId] = []
  
  emojiPosCount = len(re.findall(happy, text))
  emojiNegCount = len(re.findall(sad, text))
  userToPos[userId].append(emojiPosCount)
  userToNeg[userId].append(emojiNegCount)
  userToNet[userId].append(emojiPosCount - emojiNegCount)
  line += 1
f.close()

emojiCountOut.writerow(["userid","pos_emoji_count", "neg_emoji_count", "net_emoji_count"])
for userid in userToNet.keys():
  row = [userid,numpy.mean(userToPos[userid]),numpy.mean(userToNeg[userid]),numpy.mean(userToNet[userid])]
  emojiCountOut.writerow(row)
emojiCountf.close()