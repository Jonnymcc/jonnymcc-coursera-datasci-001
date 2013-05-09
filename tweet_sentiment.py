import sys
import json

def get_sentiment(sent_file):
    afinnfile = open(sent_file)
    scores = {} 
    for line in afinnfile:
      term, score  = line.split("\t")  
      scores[term] = int(score)  
    
    return scores 

def main():
    sent_file = sys.argv[1]
    tweet_file = open(sys.argv[2])

    sentiment = get_sentiment(sent_file)

    for line in tweet_file:
        sent = 0
        if not "delete"  in json.loads(line).keys():
            for w in json.loads(line)["text"].split():
                w = w.strip("""!@#$%^&*."'""").encode('utf-8')
                if w in sentiment.keys():
                    sent += sentiment[w]
        print "\t", sent

if __name__ == '__main__':
    main()
