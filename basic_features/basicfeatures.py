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

import sys
import cPickle as pickle


class BasicExtractor:

    def __init__(self, pickle_file):
        self._statuses = pickle.load(open(pickle_file, 'rb'))
        self._averages = dict()
        self._gender_stats = dict()

    """
    Processes statuses. (For information on how the different data structures
    are set up, look at the comments for the getters.)
    """

    def process(self):
        lengths = dict()
        for status in self._statuses[1:]:
            user = status[0]
            gender = int(status[4])
            if user not in lengths:
                lengths[user] = [0, 0]
            if user not in self._gender_stats:
                self._gender_stats[user] = [gender, 0, 0]

            # split status message into tokens
            tokens = status[1].split()
            for token in tokens:
                # update gender stats
                if token[:5] == '<PROP':
                    # TODO: make sure 0 is female
                    if gender == 0:
                        if token == '<PROPFEMALE>':
                            self._gender_stats[user][1] += 1
                        elif token == '<PROPMALE>':
                            self._gender_stats[user][2] += 1
                    else:
                        if token == '<PROPMALE>':
                            self._gender_stats[user][1] += 1
                        elif token == '<PROPFEMALE>':
                            self._gender_stats[user][2] += 1

                # all other token processing
                elif token != '<X>':
                    lengths[user][0] += len(token)
                    lengths[user][1] += 1

        for user in lengths.keys():
            self._averages[user] = lengths[user][0] * 1.0 / lengths[user][1]

    """
    Returns a dict mapping user IDs to their average token lengths.
    """

    def avg_token_length(self):
        return self._averages

    """
    Returns a dict mapping user IDs to a list of [their gender, # of
    same gender mentions, # of opposite gender mentions]
    """

    def gender_stats(self):
        return self._gender_stats

    # TODO: figure out how to format the output for WEKA



def usage():
    print """usage: python basicfeatures.py [picklefile]
    [picklefile]: the name of the file containing the pickled statuses"""

if __name__ == '__main__':
    if (len(sys.argv) == 1):
        usage()
        sys.exit()
    
    extractor = BasicExtractor(sys.argv[1])
    extractor.process()
    print extractor.avg_token_length()
    print extractor.gender_stats()
