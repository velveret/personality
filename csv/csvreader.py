import csv
import re
import sys
import cPickle as pickle


def main():
    if (len(sys.argv) == 1):
        print "need the name of the csv file to open"

    statuses = []
    timestamp_pattern = re.compile("\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d")
    with open(sys.argv[1], 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if timestamp_pattern.match(row[2]):
                statuses.append(row)

    # if you want to pickle the array, provide a filename to pickle to
    if (len(sys.argv) == 3):
        pickle_file = sys.argv[2]
        pickled_output = open(pickle_file, 'wb')
        pickle.dump(statuses, pickled_output, -1)
        pickled_output.close()

    for row in statuses:
        print row



if __name__ == '__main__' : main()
