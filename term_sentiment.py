import sys
import json

def get_sentiment(sent_file):
    afinnfile = open(sent_file)
    scores = {} 
    for line in afinnfile:
      term, score  = line.split("\t")  
      scores[term] = int(score)  
    
    return scores 

class message(object):
    
    def __init__(self, text=""):
        self.positive = False
        self.negative = False    
        self.text = text

class term(object):
    
    def __init__(self):
        self.count_pos = float(0)
        self.count_neg = float(0)

    def get_sentiment(self):
        if self.count_pos == 0 or self.count_neg == 0:
            return 0
        score = self.count_pos / self.count_neg
        if score >= 1:
            score += -1
        else:
            score = -((1 / score) - 1)
        return score

def main():
    sent_file = sys.argv[1]
    tweet_file = open(sys.argv[2])

    terms = {}
    sentiment = get_sentiment(sent_file)
    #inter_msgs = []

    for line in tweet_file:
        msg = None
        # is it a tweet or delete?
        if not "delete"  in json.loads(line).keys():
            sent = 0
            msg = message(json.loads(line)["text"])
            # Check each word in text, pos or negative?
            for w in msg.text.split():
                w = w.strip("""!@#$%^&*."'""").encode('utf-8').lower()
                # Add new terms
                if w not in terms:
                    terms[w] = term()  
                # Check sentiment of message
                if w in sentiment.keys():
                    sent += sentiment[w]
                    if sentiment[w] > 0:
                        msg.positive = True
                        terms[w].count_pos += 1
                    elif sentiment[w] < 0:
                        msg.negative = True
                        terms[w].count_pos += 1
            
            for w in msg.text.split():
                w = w.strip("""!@#$%^&*."'""").encode('utf-8').lower()
                if msg.positive:
                    terms[w].count_pos += 1
                if msg.negative:
                    terms[w].count_neg += 1
                
    for x, y in terms.iteritems():
        if y.count_pos > 0 and y.count_neg > 0:
            print x, y.get_sentiment()

if __name__ == '__main__':
    main()
