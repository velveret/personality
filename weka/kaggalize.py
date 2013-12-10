import re
import sys
import csv

if len(sys.argv) < 4:
  print len(sys.argv)
  print """USAGE: python kaggalize.py [userid_file] [in_file] [out_file]"""
  sys.exit()

outFile = open(sys.argv[3], 'w')
out = csv.writer(outFile, delimiter = ",", escapechar='\\', quoting=csv.QUOTE_NONE)
out.writerow(["class", "predictions"])

inFilename = sys.argv[2]
f= open(inFilename, 'r')
fin = csv.reader(f, delimiter = ",")

useridFilename = sys.argv[1]
userf= open(useridFilename, 'r')
userfin = csv.reader(userf, delimiter = ",")

userIds = []
line = 0
for row in userfin:
    if (line ==0):
      line += 1
      continue
    if len(row) == 0:
      continue
    userIds.append(row[0])

neuroUsers = []
line = 0
for row in fin:
    if (line ==0):
      line += 1
      continue
    if len(row) == 0:
      continue
    instanceNum = int(row[0])
    neuro=row[2][len(row[2]) -1]
    if (neuro == "+"):
        neuroUsers.append(userIds[instanceNum-1])

out.writerow(["+", " ".join(neuroUsers)])
f.close()
userf.close()
outFile.close()

