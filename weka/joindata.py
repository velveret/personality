import re
import sys
import csv

if len(sys.argv) < 4:
  print len(sys.argv)
  print """USAGE: python joindata.py [is_test] [out_file] [all_input_files]"""
  sys.exit()

if (sys.argv[1] == "true"):
  is_test = True
else:
  is_test = False

outFile = open(sys.argv[2], 'w')
if is_test:
  outFile_noid = open(sys.argv[2].replace(".", "_noid."), 'w')
userToFeatures = {}
processedUsers = []
out = csv.writer(outFile, delimiter = ",", quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
if is_test:
  out_noid = csv.writer(outFile_noid, delimiter = ",", quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)

if not(is_test):
  feats = ["userid"]
else:
  feats = ["userid"]
for index in range(3, len(sys.argv)):
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
      if not(is_test):
        userToFeatures[userId] = [userId]
      else:
        userToFeatures[userId] = [userId]
    userToFeatures[userId].extend(row[1:])
    processedUsers.append(userId)
  f.close()
  # empty fields for users with no features
  for userId in set(userToFeatures.keys()) - set(processedUsers):
    for i in range(0, numfeats):
      userToFeatures[userId].append("")

out.writerow(feats)
if is_test:
  out_noid.writerow(feats[1:])
for userid in userToFeatures.keys():
  out.writerow(userToFeatures[userid])
  if is_test:
    out_noid.writerow(userToFeatures[userid][1:])

outFile.close()