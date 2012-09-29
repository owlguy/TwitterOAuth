__author__ = 'Joe.Hootman'

# -*- coding: utf-8 -*-

import csv
import datetime
import sys
import json
import re
import twitter
from uuid import uuid4
import couchdb

#pull top 500 terms from csv and look them up
with open('Top500BrownCorpusTerms.csv', 'rb') as csvfile:
    termreader = csv.reader(csvfile, delimiter=',')
    terms = []
    for row in termreader:
        terms.append(row)
        #print '. '.join(row)

print terms.count
exit

for term in terms:

    Q = term

    print 'base_term = ', Q

    exit

#Q = ' '.join(sys.argv[1:])

    MAX_PAGES = 15
    RESULTS_PER_PAGE = 100

    twitter_search = twitter.Twitter(domain="search.twitter.com")

    search_results = []
    for page in range(1,MAX_PAGES+1):
        search_results += twitter_search.search(q=Q, rpp=RESULTS_PER_PAGE, page=page)['results']

    for result in search_results:
        #print result
        if (result['iso_language_code']) == 'en':

            tweet = result['text']
            created_at = result['created_at']
            from_user_name = result['from_user_name']
            from_user_id = result['from_user_id']

            docid = uuid4().hex
            write_stamp = '%s' % datetime.datetime.now()
            hashtags = re.findall('#(\w+)', tweet)

            if hashtags.count > 1:

                doc = {'_id' : docid, 'tweet' : tweet, 'base_term' : Q, 'hashtags' : hashtags, 'from_user_name': from_user_name, \
                       'from_user_id' : from_user_id, 'created_at' : created_at, 'write_stamp' : write_stamp }

                print json.dumps(doc, indent=1)


                server = couchdb.Server('http://localhost:5984')
                DB = 'browncorpustwitter'

                try:
                    db = server.create(DB)

                except couchdb.http.PreconditionFailed, e:
                    # Already exists, so append to it, keeping in mind that duplicates could occur
                    db = server[DB]

                db.save(doc)


    #print json.dumps(search_results, indent=1)
