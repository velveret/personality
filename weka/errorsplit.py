import re
import sys
import csv

modelresultFilename = "error_ourmodel.csv"
instancesFilename = "error_test.csv"
sep = ','

correct = open("error_correct.csv", 'w')
incorrect = open("error_incorrect.csv", 'w')

correctout = csv.writer(correct, delimiter = sep, quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
incorrectout = csv.writer(incorrect, delimiter = sep, quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)

instancesf= open(instancesFilename, 'r')
modelresultsf = open(modelresultFilename, 'r')
fin = csv.reader(f, delimiter = sep)
modelresultsin = csv.reader(f, delimiter = sep)

incorrectInstances = []
line = 1
for row in modelresultsin:
  if (line == 1):
    line += 1
    continue
  if len(row) == 0:
    line += 1
    continue
  instanceNum = row[0]
  actual = row[1][2:2]
  predicted = row[2][2:2]
  if actual != predicted:
    incorrectInstances.append(instanceNum)
  line += 1

line = 0
correctCount = 0
incorrectCount = 0
for row in instancesf:
  line += 1
  if (line == 1):
    continue
  if len(row) == 0:
    continue
  instanceNum = (line - 1)/2
  if instanceNum in incorrectInstances:
    incorrectout.writerow(row)
    incorrectCount += 1
  else:
    correctout.writerow(row)
    correctCount += 1
instancesf.close()
modelresultsf.close()
  
incorrect.close()
correct.close()
print "Finished splitting, with " + str(correctCount) + " correct, " + str(incorrectCount) + " incorrect"
print "Should have " + str(len(incorrectInstances)) + " incorrect"