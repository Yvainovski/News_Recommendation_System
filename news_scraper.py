# -*- coding: utf-8 -*-
'''
This file implement functions that scrap news from newAPI and store them into
mlab MongoDB
'''
import os
import sys
import time
from newsapi import NewsApiClient
from pymongo import MongoClient

#----------NewsAPI & MongoDB(mLab)------------------#
newsAPI_key = 'NoSHOW'
mongodb_user = 'NoSHOW'
mongodb_password = 'NoSHOW'
mongodb_host = 'NoSHOW'
#---------------------------------------------------
newsapi = NewsApiClient(api_key=newsAPI_key)
mlab_url = 'mongodb://{}:{}@{}/news_db'.format(mongodb_user,mongodb_password,mongodb_host)
client = MongoClient(mlab_url)
news_db = client.get_database('news_db')
news_coll = news_db.news
#---------------------------------------------#

categories = ['business','entertainment','general','health',
            'science', 'sports', 'technology']
countries = ['us','gb','ca','au']
news_added = 0


def ins_mongo_news(news):
    global news_added
    #check if news already exists in db
    ret = news_coll.find_one({'title':news['title']})
    if(ret is None):
        all_news = news_coll.insert_one(news)
        news_added += 1

def news_db_info():
    for category in categories:
        ret = news_coll.find({'category':category})
        print('{}: {}'.format(category,ret.count()))
    print('News Total: {}'.format(news_coll.count()))

def scrap_news():
    for country in countries:

        for category in categories:
            top_headlines = newsapi.get_top_headlines( category=category,
                                                  language='en',
                                                  country=country)
            for t_h in top_headlines['articles']:
                news = dict()
                #title
                news['title'] = t_h['title']
                #description
                if(t_h['description'] == '' or t_h['description'] is None):
                    news['description'] = t_h['title']
                else:
                    news['description'] = t_h['description']
                #category
                news['category'] = category
                #date(publishedAt)
                news['date'] = t_h['publishedAt']
                #author
                news['author'] = t_h['author']
                #source
                news['source'] = t_h['source']['name']
                #url
                news['url'] = t_h['url']
                #urlToImage
                news['img_url'] = t_h['urlToImage']
                #country
                news['country'] = country
                # print(news)
                # Insert Into mongodb
                ins_mongo_news(news)
            #for-END
        #for-END
    #for-END



if __name__ == '__main__':
    while(True):
        scrap_news()
        print('----------------------------------')
        news_db_info()
        print('***Newly added: {}***'.format(news_added))
        news_added = 0
        os.system('mongoexport -h {} -d news_db -c news -u {} -p {} -o news.json'.format(mongodb_host,mongodb_user,mongodb_password))
        for t in range(30,0,-1):
            print(t)
            time.sleep(1)
        # sys.exit()
