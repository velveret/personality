import re
import sys
import csv
import numpy

if len(sys.argv) < 4:
  print len(sys.argv)
  print """USAGE: python reformat.py [input_file] [output_file] [is_test]"""
  sys.exit()

if (sys.argv[3] == "true"):
  is_test = True
else:
  is_test = False

inFilename = sys.argv[1]
f= open(inFilename, 'rU')
if is_test:
	fin = csv.reader(f, delimiter = ",")
else:
	fin = csv.reader(f, delimiter = "\t")

outFile = open(sys.argv[2], 'w')
userToSentiment = {}
userToNeuro = {}
out = csv.writer(outFile, delimiter = ",", quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
line = 0
for row in fin:
	
	if len(row) == 0:
		continue
	row.pop(1)
	row.pop(1)
	# aggregate by user
	userId = row[0]
	if not(is_test):
		neuro = row[3]
		senti = float(row[7])
		if not(userId in userToNeuro):
			userToNeuro[userId] = neuro
		if not(userId in userToSentiment):
			userToSentiment[userId] = []
		userToSentiment[userId].append(senti)
	else:
		senti = float(row[3])
		if not(userId in userToSentiment):
			userToSentiment[userId] = []
		userToSentiment[userId].append(senti)
if not(is_test):
	for userid in userToNeuro.keys():
		row = [userid, userToNeuro[userid], numpy.mean(userToSentiment[userid])]
		out.writerow(row)
else:
	for userid in userToSentiment.keys():
		row = [userid,"-",numpy.mean(userToSentiment[userid])]
		out.writerow(row)

f.close()
outFile.close()