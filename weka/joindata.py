import re
import sys
import csv

if len(sys.argv) < 3:
  print len(sys.argv)
  print """USAGE: python joindata.py [out_file] [all_input_files]"""
  sys.exit()

outFile = open(sys.argv[1], 'w')
userToFeatures = {}
processedUsers = []
out = csv.writer(outFile, delimiter = ",", quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)

feats = ["userid"]
for index in range(2, len(sys.argv)):
  inFilename = sys.argv[index]
  f= open(inFilename, 'r')
  fin = csv.reader(f, delimiter = ",")
  
  line = 0
  numfeats = 0
  processedUsers = []
  for row in fin:
  	if (line ==0):
		line += 1
		# process headers
		feats.extend(row[1:])
		numfeats = len(row) - 1
		continue
  	if len(row) == 0:
		continue
  	# aggregate by user
	userId = row[0]
  	if not(userId in userToFeatures):
		userToFeatures[userId] = [userId]
	userToFeatures[userId].extend(row[1:])
	processedUsers.append(userId)
  f.close()
  # empty fields for users with no features
  for userId in set(userToFeatures.keys()) - set(processedUsers):
  	for i in range(0, numfeats):
  		userToFeatures[userId].append("")

out.writerow(feats)
for userid in userToFeatures.keys():
	out.writerow(userToFeatures[userid])

outFile.close()