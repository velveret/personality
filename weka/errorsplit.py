import re
import sys
import csv

modelresultFilename = "error_ourmodel.csv"
instancesFilename = "error_test.csv"
sep = ','

# correct = open("error_correct.csv", 'w')
# incorrect = open("error_incorrect.csv", 'w')
# correct_and_incorrect = open("error_correctness_test.csv", 'w')
falsePos_Neg = open("error_falseness_test.csv", "w")

instancesf= open(instancesFilename, 'rU')
modelresultsf = open(modelresultFilename, 'rU')
modelresultsin = csv.reader(modelresultsf, delimiter = sep)

incorrectInstances = []
falsePositives = []
falseNegatives = []
line = 1
for row in modelresultsin:
  if (line == 1):
    line += 1
    continue
  if len(row) == 0:
    line += 1
    continue
  instanceNum = int(row[0])
  actual = row[1][2]
  predicted = row[2][2]
  if actual != predicted:
    incorrectInstances.append(instanceNum)
  if actual == "+" and predicted == "-":
    falseNegatives.append(instanceNum)
  elif actual == "-" and predicted == "+":
    falsePositives.append(instanceNum)
  line += 1

line = 0
correctCount = 0
incorrectCount = 0
for row in instancesf.readlines():
  line += 1
  if (line == 1):
    continue
  instanceNum = (line - 1)/2
  # if instanceNum in incorrectInstances and len(row) > 10:
  #   # incorrect.write(row)
  #   # correct_and_incorrect.write("incorrect," + row)
  #   incorrectCount += 1
  # elif len(row) > 10:
  #   # correct.write(row)
  #   correct_and_incorrect.write("correct," + row)
  #   correctCount += 1
  if len(row) > 10 and instanceNum in falsePositives:
    falsePos_Neg.write("false_positive," + row)
  elif len(row) > 10 and instanceNum in falseNegatives:
    falsePos_Neg.write("false_negative," + row)
instancesf.close()
modelresultsf.close()
  
# incorrect.close()
# correct.close()
# correct_and_incorrect.close()
falsePos_Neg.close()
# print "Finished splitting, with " + str(correctCount) + " correct, " + str(incorrectCount) + " incorrect"
# print "Should have " + str(len(incorrectInstances)) + " incorrect"