import re
import sys
import csv

if len(sys.argv) < 3:
  print len(sys.argv)
  print """USAGE: python emojicount.py [input_file] [output_file]"""
  sys.exit()

emojiCountFilename = sys.argv[2]
sep = ','
sep2 = '\t' # must be one character so add semicolon later

emojiCountf = open(emojiCountFilename, 'w')

emojiCountOut = csv.writer(emojiCountf, delimiter = sep2, quotechar='', escapechar='\\', quoting=csv.QUOTE_NONE)

happy = '[:=]-?\)'
sad = '[:=]-?\('

inFilename = sys.argv[1]
f= open(inFilename, 'rU')
fin = csv.reader(f, delimiter = sep)

line = 1
for row in fin:
  if (line == 1):
    row.extend(["positive_emoji_count", "negative_emoji_count", "net_emoji_count"])
    emojiCountOut.writerow(row)
    line += 1
    continue
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
  emojiCountOut.writerow(row)
  line += 1
f.close()
  
emojiCountf.close()