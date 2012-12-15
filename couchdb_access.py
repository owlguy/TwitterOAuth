__author__ = 'Joe.Hootman'

import couchdb
from couchdb.mapping import TextField, IntegerField, DateField, ListField, DateTimeField
from couchdb import Server
import nltk
from nltk.corpus import wordnet as wn
from nltk import stem


server = Server('http://localhost:5984')
db = server['browncorpustwitter']

#map_fun = "hastag_count_1"
#
#results = db.query(map_fun)
#
#print len(results)


#create document class
class Tweet(couchdb.mapping.Document):
    write_stamp = DateTimeField()
    tweet = TextField()
    hashtags = ListField(
        TextField()
    )
    base_term = TextField()
    from_user_name = TextField()
    from_user_id = IntegerField()
    created_at = DateField()


#test base class
docid = '0000727b33274b19b3e02c339283d125'
doc = db[docid]
#print doc

tweetTest = Tweet.load(db, docid)
#print tweetTest.hashtags

#map_function = "function(doc) { if(doc.base_term == '#business') {  emit(doc.hashtags, 1); } }"
#reduce_function = "function(keys, values, rereduce) { return sum(values); }"

resultset = []

for row in db.view('_design/_views/_view/hashtag_count_1', group_level=1):
    resultset.append(row)

#resultset.sort()

resultset2 = sorted(resultset, key=lambda result: result.value, reverse=True)

for idx in range(129):
    print resultset2[idx]

exit()

#for item in resultset2:
#    print item


#build a vector with the base term

#build a corpus consisting of all the tweets for the base term
#then calc tf-idf vectors - use TextCollection TF-IDF
#build all results into Tweets - then go through Tweets and put them in a TextCollection
#run tf-idf off of them

#first corpus decision - whether to run with just hashtags or full tweet string.  Initially, just hashtags


all_hashtags_resultset = []

hashtags = db.view('_design/_views/_view/business_hashtags')
print 'hashtags = ', hashtags

for row in hashtags:
    for hashtag in row.value:
        all_hashtags_resultset.append(hashtag)
#    for hashtag in row:#.
#        print hashtag.key()
#        #all_hashtags_resultset.append(hashtag.key)

print 'all_hashtags_resultset = ', all_hashtags_resultset

collection = nltk.TextCollection(all_hashtags_resultset)

print "len(collection) = ", len(collection)

baseterm = 'business'
queryterm = 'women'

print "tf queryterm = ", collection.tf(queryterm, all_hashtags_resultset)
print "idf queryterm = ", collection.idf(queryterm, all_hashtags_resultset)
print "tf-idf queryterm = ", collection.tf_idf(queryterm, all_hashtags_resultset)

stemmer = stem.PorterStemmer()

stemmed_word = stemmer.stem(queryterm)

print 'stemmed_word = ', stemmed_word

baseterm_synset = wn.synset(baseterm + '.n.01')
hashtag_synset = wn.synset(hashtag + '.n.01')

print 'path similarity = ', baseterm_synset.path_similarity(hashtag_synset)
