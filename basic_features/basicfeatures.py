"""
things to cover:
- avg token length
- gender
  - same/opposite gender mentions
- frequency of punctuation/capitalization
  - time & variance
- time of day (12-5am, weekend vs weekday)
- IC of words
"""

import csv
import datetime
import string
import sys
import cPickle as pickle


class BasicExtractor:

    def __init__(self, pickle_file):
        self._statuses = pickle.load(open(pickle_file, 'rb'))
        self._averages = dict()
        self._gender_stats = dict()
        self._capitalization = dict()
        self._punctuation = dict()
        self._weekend = dict()
        self._nighttime = dict()

    """
    Processes statuses. (For information on how the different data structures
    are set up, look at the comments for the getters.)
    """

    def process(self):
        totals = dict()
        lengths = dict()
        caps = dict()
        punct = dict()
        weekend_posts = dict()
        dark_hours = dict()

        for status in self._statuses[1:]:
            user = status[0]
            gender = int(status[4])
            # TODO: update things to use totals instead
            if user not in totals:
                totals[user] = [int(status[3]), 0, 0]
            if user not in lengths:
                lengths[user] = [0, 0]
            if user not in self._gender_stats:
                self._gender_stats[user] = [gender, 0, 0]
            if user not in caps:
                caps[user] = [0, 0]
            if user not in punct:
                punct[user] = 0
            if user not in weekend_posts:
                weekend_posts[user] = 0
            if user not in dark_hours:
                dark_hours[user] = 0

            # split status message into tokens
            tokens = status[1].split()
            for token in tokens:
                # update gender stats
                if token[:5] == '<PROP':
                    if gender == 1:
                        if token == '<PROPFEMALE>':
                            self._gender_stats[user][1] += 1
                        elif token == '<PROPMALE>':
                            self._gender_stats[user][2] += 1
                    else:
                        if token == '<PROPMALE>':
                            self._gender_stats[user][1] += 1
                        elif token == '<PROPFEMALE>':
                            self._gender_stats[user][2] += 1

                # all other status token processing
                else:
                    lengths[user][0] += len(token)
                    lengths[user][1] += 1
                    
                    # TODO: deal with formatting (backslashes 'n stuff)
                    for char in token:
                        if char in string.punctuation:
                            punct[user] += 1
                        elif char.isupper():
                            caps[user][0] += 1
                        caps[user][1] += 1

            # Formatting errors are giving this section trouble...
            """
            if status[2] != "" and status[2] != "\\":
                day = status[2].split()[0]
                date_list = day.split("-")
                date = datetime.date(int(date_list[0]), int(date_list[1]), \
                  int(date_list[2]))
                if date.weekday() == 5 or date.weekday() == 6:
                    weekend_posts[user] += 1

                time = status[2].split()[1]
                hour = int(time.split(":")[0])
                if hour < 5:
                    dark_hours[user] += 1
            """

        for user in lengths.keys():
            self._averages[user] = lengths[user][0] * 1.0 / lengths[user][1]
            self._capitalization[user] = caps[user][0] * 1.0 / caps[user][1]
            self._punctuation[user] = punct[user] * 1.0 / caps[user][1]
            self._weekend[user] = weekend_posts[user] * 1.0 / totals[user][0]
            self._nighttime[user] = dark_hours[user] * 1.0 / totals[user][0]

    """
    Returns a dict mapping user IDs to their average token lengths.
    """

    def avg_token_length(self):
        return self._averages

    """
    Returns a dict mapping user IDs to a list of [their gender, # of same
    gender mentions, # of opposite gender mentions]
    """

    def gender_stats(self):
        return self._gender_stats

    # TODO: time and variance for punctuation/capitalization

    """
    Returns a dict mapping user IDs to the frequency of their capitalization
    usage. This is done on a per-character basis (i.e. # of times a letter is
    capitalized / # of total characters they have used.)
    """

    def capitalization(self):
        return self._capitalization

    """
    Returns a dict mapping user IDs to the frequency of their punctuation
    usage. This is done on a per-character basis.
    """

    def punctuation(self):
        return self._punctuation

    """
    Returns a dict mapping user IDs to the frequency of their statuses being
    posted on a weekend.
    """

    def weekend(self):
        return self._weekend

    """
    Returns a dict mapping user IDs to the frequency of their statuses being
    posted between 12-5am.
    """

    def nighttime(self):
        return self._nighttime

    # TODO: figure out how to format the output for WEKA



def usage():
    print """usage: python basicfeatures.py [picklefile] [csvfile]
    [picklefile]: the name of the file containing the pickled statuses
    [csvfile]: the name of the csv file to write to"""

if __name__ == '__main__':
    if (len(sys.argv) < 3):
        usage()
        sys.exit()
    
    extractor = BasicExtractor(sys.argv[1])
    extractor.process()

    """
    print extractor.avg_token_length()
    print extractor.gender_stats()
    print extractor.capitalization()
    print extractor.punctuation()
    print extractor.weekend()
    print extractor.nighttime()
    """

    with open(sys.argv[2], "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter = ",", quotechar = '"')
        writer.writerow(["user", "avg_token_length", "gender", "same_gender", \
          "opposite_gender", "caps", "punct", "weekend", "night"])
        for user in extractor.avg_token_length().keys():
            avg = extractor.avg_token_length()[user]
            gender_stats = extractor.gender_stats()[user]
            caps = extractor.capitalization()[user]
            punct = extractor.punctuation()[user]
            wknd = extractor.weekend()[user]
            night = extractor.nighttime()[user]

            writer.writerow([user, avg] + gender_stats + [caps, punct, wknd, \
              night])
