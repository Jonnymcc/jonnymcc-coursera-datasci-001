import sys
import collections
import json


class tweet_obj(object):
    
    def __init__(self, line=""):
        self.tweet = json.loads(line)
        self.has_entities = "entities" in self.tweet.keys()
        if self.has_entities:
            self.hashtags = [hsh["text"] for hsh in \
                self.tweet["entities"]["hashtags"]]

def main():
    tweet_file = open(sys.argv[1])

    hashtags = []

    for line in tweet_file:
        tweet = tweet_obj(line)
        if tweet.has_entities == False:
            continue

        hashtags.extend(tweet.hashtags)

    for x,y in  collections.Counter(hashtags).most_common(10):
        print x, float(y)
    
if __name__ == '__main__':
    main()
