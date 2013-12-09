import buildclassifier
import sys
import csv

##### CHECK USAGE #####

if len(sys.argv) < 3:
  print """USAGE: python classifier.py [input_filename] [output_filename]
  
This script sentiment-analyzes a tweet database given as a file.
The input format for each row is TweetID <tab> TweetText.
The output format is TweetID <tab> SentimentScore.
SentimentScore ranges from -1 (fully negative) to 1 (fully positive).

To run this script, you'll need:
--The files 'classifier.pickle','features.pickle', and 'time_limit.py' in 
  the same directory
--The python package 'nltk' installed on your system (run 'easy_install nltk'
  from the terminal; you may need to be root)
--The 'stopwords' corpus installed (run 'nltk.download()' from the python
  prompt, then 'd stopwords' at the 'Downloader>' prompt)"""
  sys.exit()

##### CLASSIFY THE INPUT CSV FILE #####

buildclassifier.load(classifierFile='classifier.pickle',featureFile='features.pickle')

print "Reading & Classifying tweets..."

inFilename = sys.argv[1]
outFilename = sys.argv[2]
sep = '\t'

f = open(inFilename, 'rU')
g = open(outFilename, 'w')
fin = csv.reader(f, delimiter=sep)
fout = csv.writer(g, delimiter=sep)

line = 1
for row in fin:
  if line == 1:
    headers = ["userid", "message", "updated_time", "n_status", "gender", "neuro", "positive_emoji_count", \
      "negative_emoji_count", "net_emoji_count", "sentiment"]
    fout.writerow(headers)
  # silently skip empty lines
  if len(row) == 0:
    line += 1
    continue
  # complain about malformatted lines
  if len(row) != 9:
    print "Malformatted line: %i; skipping." % line
    line += 1
    continue
  text = row[1]
  score = buildclassifier.classify(text)
  row.append(score)
  fout.writerow(row)
  line += 1

f.close()
g.close()

print "Finished!"

