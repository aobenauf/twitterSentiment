# coding: utf-8

# In[100]:

import tweepy
from textblob import TextBlob
import pandas as pd
consumer_key = 'TIVJtxHDEBWC9yoMPWl9i1JPh'
consumer_secret ='nVahog6TB8kyyDGXsYeZzOmW3g1Ng33dEd83iQnI7cspsf5TFM'
access_token = '426390930-QoJHM5sYa0FrVNFXdZrbCfOKmWeAXedTtyuEWyiK'
access_token_secret = 'sGO4wxpKId3nc55AncK7gXFVL2qGHXTfe9JNR0fE7ASuQ'
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)


# In[101]:

####TWEETS#####
from datetime import datetime as dt
friend = 'AlexObenauf27'

timeline = api.user_timeline(screen_name = friend, count = 100, include_rts = True)

#analysis on tweets liked
pages_of_likes = []
#collecting the first five pages which should be about 100 likes
for i in range(1,25):
    likes_per_page = api.favorites(friend,page=i)
    pages_of_likes.append(likes_per_page)


# In[102]:

tweets = {}
retweets = {}
replies = {}
tweet_ids = {}
tweet_detail = {}


for tweet in timeline:
    date = tweet.created_at.strftime('%m/%d/%y')
    if date in tweet_ids:
        tweet_ids[date].append(tweet.id)
    else:
        
        tweet_ids[date] = []
        tweet_ids[date].append(tweet.id)
        
#to get tweet text per tweet id
for tweet in timeline:
    tweet_id = tweet.id
    if tweet_id in tweet_detail:
        tweet_detail[tweet_id] = tweet.text
    else:     
        tweet_detail[tweet_id] = tweet.text


pos = 0
neg = 0
date_of_tweets = []
#for tweet sentiment
for tweet in timeline:
    #print(tweet.text)
    #analysis = TextBlob(tweet.text)
    #print(analysis.sentiment)
    date = tweet.created_at.strftime('%m/%d/%y')
    if tweet.retweeted == True:
        if date in retweets:
            retweets[date] += TextBlob(tweet.text).sentiment.polarity
        else:
            retweets[date] = TextBlob(tweet.text).sentiment.polarity
    elif tweet.in_reply_to_status_id != None:
        if date in replies:
            replies[date] += TextBlob(tweet.text).sentiment.polarity
        else:
            replies[date] = TextBlob(tweet.text).sentiment.polarity
    else:
        if date in tweets:
            tweets[date] += TextBlob(tweet.text).sentiment.polarity
        else:
            tweets[date] = TextBlob(tweet.text).sentiment.polarity
    
    #calculating how many positive and negative tweets per day
    if TextBlob(tweet.text).sentiment[0] > 0:
        pos += 1
    if TextBlob(tweet.text).sentiment[0] < 0:
        neg += 1
        
    date_of_tweets.append(date)
    

#consolidating the sentiment for each day for tweets,retweets and replies
tweet_sentiment = {}
for k, v in retweets.items():
    if k in tweet_sentiment:
        tweet_sentiment[k] += v
    else:
        tweet_sentiment[k] = v
        
for k, v in tweets.items():
    if k in tweet_sentiment:
        tweet_sentiment[k] += v
    else:
        tweet_sentiment[k] = v
        
for k, v in replies.items():
    if k in tweet_sentiment:
        tweet_sentiment[k] += v
    else:
        tweet_sentiment[k] = v


# In[103]:

likes = {}
like_ids = {}   #date: ID
like_detail = {}   #ID: Text
like_sentiment = {}

#this is to create the like_ids for each tweet
for page in pages_of_likes:
    for like in page:
        date = like.created_at.strftime('%m/%d/%y')
        if date in like_ids:
            like_ids[date].append(like.id)
        else:
            like_ids[date] = []
            like_ids[date].append(like.id)
        
#to get tweet text per tweet id
for page in pages_of_likes:
    for like in page:
        like_id = like.id
        if like_id in like_detail:
            like_detail[like_id] = like.text
        else:     
            like_detail[like_id] = like.text

            
            
#this is to get the sentiment of each tweet
for page in pages_of_likes:
    for like in page:
        date = like.created_at.strftime('%m/%d/%y')

        if date in like_sentiment:
            like_sentiment[date] += TextBlob(like.text).sentiment.polarity
        else:
            like_sentiment[date] = TextBlob(like.text).sentiment.polarity


# In[104]:
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
dates_of_tweets = sorted(date_of_tweets)
print("Tweets from: " + str(date_of_tweets[-1]) + " to " + str(date_of_tweets[0]))
print("Positive tweets: " + str(pos) + " || " + "Negative tweets: " + str(neg))
tweets_df = pd.DataFrame(list(tweets.items()), columns = ['Date','Tweet Sentiment'])
tweets_df['Date'] = pd.to_datetime(tweets_df['Date'])
retweets_df = pd.DataFrame(list(retweets.items()), columns = ['Date','RT Sentiment'])
retweets_df['Date'] = pd.to_datetime(retweets_df['Date'])
replies_df = pd.DataFrame(list(replies.items()), columns = ['Date','Reply Sentiment'])
replies_df['Date'] = pd.to_datetime(replies_df['Date'])
likes_df = pd.DataFrame(list(like_sentiment.items()), columns = ['Date', 'Like Sentiment'])
likes_df['Date'] = pd.to_datetime(likes_df['Date'])
#tweets_df.plot.line()
#retweets_df.plot.line()
#replies_df.plot.line()
plt.figure(figsize=(20,5))

try:
    plt.plot(tweets_df['Date'],tweets_df['Tweet Sentiment'])
except:
    print("No Tweet Data")

try:
    plt.plot(retweets_df['Date'],retweets_df['RT Sentiment'])
except:
    print("No RT Data")
    
try:
    plt.plot(replies_df['Date'],replies_df['Reply Sentiment'])
except:
    print("No Reply Data")
    
try:
    plt.plot(likes_df['Date'],likes_df['Like Sentiment'])
except:
    print("No Like Data")

plt.legend()


# In[105]:

from dateutil.parser import *
#a tool that looks at likes within a certain date timeframe 04/25/18
#Could switch this up to look at tweets by just changing like dictionaries to the tweet dictionaries
#TODO - could create some sort of visual aid to read them, with bubbles that have the text in them and colors for the sentiment it would be cool
#like_ids ---> #date: ID
#like_detail --->  #ID: Text
month_beg = parse('8/1/2017')
month_end = parse('9/1/2017')

for k, v in like_ids.items():
    if month_beg <= parse(k) <= month_end:
        #excludes tweets that had a 0.0 rated sentiment, could change to something like over abs value of .3 or something
        if like_sentiment[k] == 0.0:
            pass
        else:
            print(str(k) + " had " + str(len(v)) + " likes/s with an overall sentiment of " + str(like_sentiment[k]))
            for i in v:
                text = like_detail[i]
                print(text)


# In[106]:

#a tool that looks at tweets within a certain date timeframe 04/25/18
#Could switch this up to look at tweets by just changing like dictionaries to the tweet dictionaries
#TODO - could create some sort of visual aid to read them, with bubbles that have the text in them and colors for the sentiment it would be cool
#like_ids ---> #date: ID
#like_detail --->  #ID: Text
month_beg = parse('8/1/2017')
month_end = parse('9/1/2017')

for k, v in tweet_ids.items():
    if month_beg <= parse(k) <= month_end:
        #excludes tweets that had a 0.0 rated sentiment, could change to something like over abs value of .3 or something
        if tweet_sentiment[k] == 0.0:
            pass
        else:
            print(str(k) + " had " + str(len(v)) + " tweet/s with an overall sentiment of " + str(tweet_sentiment[k]))
            for i in v:
                text = tweet_detail[i]
                print(text)


# In[107]:

#WordClouds
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

tweet_words = " "
for k,v in tweet_detail.items():
    tweet_words += " " + v

tweets_no_urls_no_tags = " ".join([word for word in tweet_words.split()
                            if 'http' not in word
                                and not word.startswith('@')
                                and not word.startswith('.@')
                                and word != 'RT'
                            ])   

like_words = " "
for k,v in like_detail.items():
    like_words += " " + v

likes_no_urls_no_tags = " ".join([word for word in like_words.split()
                            if 'http' not in word
                                and not word.startswith('@')
                                and not word.startswith('.@')
                                and word != 'RT'
                            ])  

#print(no_urls_no_tags)
#for k,v in like_detail.items():

wordcloud1 = WordCloud(font_path=None,width=2400,height=1600,stopwords=STOPWORDS).generate(tweets_no_urls_no_tags)
wordcloud2 = WordCloud(font_path=None,width=2400,height=1600,stopwords=STOPWORDS).generate(likes_no_urls_no_tags)


# In[108]:

fig = plt.figure(figsize=(20,10))

ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)

ax1.imshow(wordcloud1)
ax1.axis('off')
ax2.imshow(wordcloud2)
ax2.axis('off')

ax1.set_title('Tweets')
ax2.set_title('Likes')

plt.show()


# In[109]:

#word cloud of only negative words and only positive words for Tweets
negative_tweet_words = " "
positive_tweet_words = " "

for k,v in tweet_detail.items():
    sentiment = TextBlob(v).sentiment.polarity
    if sentiment < 0:
        negative_tweet_words += " " + v
    elif sentiment > 0:
        positive_tweet_words += " " + v

            
            
negative_tweet_words_no_tags = " ".join([word for word in negative_tweet_words.split()
                    if 'http' not in word
                        and not word.startswith('@')
                        and not word.startswith('.@')
                        and word != 'RT'
                    ])            


positive_tweet_words_no_tags = " ".join([word for word in positive_tweet_words.split()
                if 'http' not in word
                    and not word.startswith('@')
                    and not word.startswith('.@')
                    and word != 'RT'
                ])

wordcloud3 = WordCloud(font_path=None,width=2400,height=1600,stopwords=STOPWORDS).generate(negative_tweet_words_no_tags)
wordcloud4 = WordCloud(font_path=None,width=2400,height=1600,stopwords=STOPWORDS).generate(positive_tweet_words_no_tags)


# In[110]:

fig2 = plt.figure(figsize=(20,10))

ax3 = fig2.add_subplot(1,2,1)
ax4 = fig2.add_subplot(1,2,2)

ax3.imshow(wordcloud3)
ax3.axis('off')
ax4.imshow(wordcloud4)
ax4.axis('off')

ax3.set_title('Negative Tweets')
ax4.set_title('Positive Tweets')

fig2.show()


# In[111]:

#word cloud of only negative words and only positive words for Tweets
negative_like_words = " "
positive_like_words = " "

for k,v in like_detail.items():
    sentiment = TextBlob(v).sentiment.polarity
    if sentiment < 0:
        negative_like_words += " " + v
    elif sentiment > 0:
        positive_like_words += " " + v

            
            
negative_likes_words_no_tags = " ".join([word for word in negative_like_words.split()
                    if 'http' not in word
                        and not word.startswith('@')
                        and not word.startswith('.@')
                        and word != 'RT'
                    ])            


positive_likes_words_no_tags = " ".join([word for word in positive_like_words.split()
                if 'http' not in word
                    and not word.startswith('@')
                    and not word.startswith('.@')
                    and word != 'RT'
                ])

wordcloud5 = WordCloud(font_path=None,width=2400,height=1600,stopwords=STOPWORDS).generate(negative_likes_words_no_tags)
wordcloud6 = WordCloud(font_path=None,width=2400,height=1600,stopwords=STOPWORDS).generate(positive_likes_words_no_tags)


# In[112]:

fig3 = plt.figure(figsize=(20,10))

ax5 = fig3.add_subplot(1,2,1)
ax6 = fig3.add_subplot(1,2,2)

ax5.imshow(wordcloud5)
ax5.axis('off')
ax6.imshow(wordcloud6)
ax6.axis('off')

ax5.set_title('Negative Likes')
ax6.set_title('Positive Likes')

fig3.show()
