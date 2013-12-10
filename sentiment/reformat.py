import re
import sys
import csv
import numpy

if len(sys.argv) < 3:
  print len(sys.argv)
  print """USAGE: python reformat.py [input_file] [output_file]"""
  sys.exit()

inFilename = sys.argv[1]
f= open(inFilename, 'rU')
fin = csv.reader(f, delimiter = "\t")

outFile = open(sys.argv[2], 'w')
userToSentiment = {}
userToNeuro = {}
out = csv.writer(outFile, delimiter = ",", quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
line = 0
for row in fin:
	if (line ==0):
		line += 1
		continue
	if len(row) == 0:
		continue
	row.pop(1)
	row.pop(1)
	# aggregate by user
	userId = row[0]
	neuro = row[3]
	senti = float(row[7])
	if not(userId in userToNeuro):
		userToNeuro[userId] = neuro
	if not(userId in userToSentiment):
		userToSentiment[userId] = []
	userToSentiment[userId].append(senti)
for userid in userToNeuro.keys():
	row = [userid, userToNeuro[userid], numpy.mean(userToSentiment[userid])]
	out.writerow(row)

f.close()
outFile.close()