import csv
import sys


def main():
    if (len(sys.argv) == 1):
        print "need the name of the csv file to open"

    statuses = []
    with open(sys.argv[1], 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            statuses.append(row)

    for row in statuses:
        print row



if __name__ == '__main__' : main()
