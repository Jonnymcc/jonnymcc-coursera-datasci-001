#! /usr/bin/env python
import urllib
import json

response = urllib.urlopen("http://search.twitter.com/search.json?q=microsoft")
for result in json.load(response)["results"]:
    print result["text"] + "\n"
