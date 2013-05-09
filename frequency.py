import sys
import json

def main():
    tweet_file = open(sys.argv[1])

    terms = {}

    for line in tweet_file:
        if not "delete"  in json.loads(line).keys():
            for w in json.loads(line)["text"].split():
                w = w.strip("""!@#$%^&*."'""").encode('utf-8').lower()
                if w not in terms:
                    terms[w] = 1
                else:
                    terms[w] += 1

    for word, freq in terms.iteritems():
        print word, freq

if __name__ == '__main__':
    main()
