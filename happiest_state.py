import sys
import json

def get_sentiment(sent_file):
    afinnfile = open(sent_file)
    scores = {} 
    for line in afinnfile:
      term, score  = line.split("\t")  
      scores[term] = int(score)  
    
    return scores 

class tweet_obj(object):
    
    def __init__(self, line=""):
        self.tweet = json.loads(line)
        self.has_text = "text" in self.tweet.keys()
        self.text = ""
        if self.has_text == True:
            self.text = self.tweet["text"]

        self.has_lang = "lang" in self.tweet.keys()
        self.lang = ""
        if self.has_lang == True:
            self.lang = self.tweet["lang"]
        
        self.state = []
        if "place" in self.tweet.keys():
            if self.tweet["place"] is not None:
                if "country_code" in self.tweet["place"]:
                    self.in_us = self.tweet["place"]["country_code"] == "US"
                    if self.in_us == True:
                        self.state = \
                            self.tweet["place"]["full_name"].split(',')[1].strip() 
        if len(self.state) > 2:
            self.state = None

        self.sentiment = 0

class state_obj(object):
    
    def __init__(self, name=""):
        self.name = name
        self.num_tweets = 0
        self.total_sentiment = 0.0

    def get_happy(self):

        if self.num_tweets == 0:
            return 0
        return self.total_sentiment / self.num_tweets
        
def main():
    sent_file = sys.argv[1]
    tweet_file = open(sys.argv[2])

    sentiment = get_sentiment(sent_file)
    tweets = []

    for line in tweet_file:
        tweet = tweet_obj(line)
        if tweet.has_text == False:
            continue
        if tweet.lang != "en":
            continue
        if not tweet.state:
            continue
        for w in tweet.text.split():
            w = w.strip("""!@#$%^&*."'""").encode('utf-8')
            if w in sentiment.keys():
                tweet.sentiment += sentiment[w]

        tweets.append(tweet)
    
    states = {}
    for tweet in tweets:
        if tweet.state not in states:
            states[tweet.state] = state_obj(tweet.state)
        states[tweet.state].num_tweets += 1
        states[tweet.state].total_sentiment += tweet.sentiment 
    
    states = dict([(st,tw.get_happy()) for st,tw in states.iteritems()])
    happy_state = max(states.iterkeys(), key=(lambda key: states[key]))
    print happy_state
    

if __name__ == '__main__':
    main()
