# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class SaveItemToMongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri= crawler.settings.get('DATABASE').get('default').get('HOST'),
            mongo_db= crawler.settings.get('DATABASE').get('default').get('DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        pass


class SaveTeamRankItemToMongoPipeline(SaveItemToMongoPipeline):
    def process_item(self, item, spider):

        team_coll = self.db[spider.settings.get('MONGO_DB_TEAM_COLL')]
        participant_coll = self.db[spider.settings.get('MONGO_DB_PARTICIPANT_COLL')]

        type = item['rank_type']

        if type == 'Team':
            item_id = item['team_id']
            team = team_coll.find_one({'team_id': item_id})
            if team:
                # remove the existing team
                team_coll.delete_many({'team_id': item_id})
            spider.logger.info(f"Save the following team to mongodb. ")
            spider.logger.info(dict(item))
            item = dict(item)
            item.pop('rank_type')
            team_coll.insert_one(item)
            return item

        elif type == 'Participant':
            item_id = item['participant_id']
            participant = team_coll.find_one({'participant_id': item_id})
            if participant:
                # remove the existing participant
                participant_coll.delete_many({'participant_id': item_id})
            spider.logger.info(f"Save the following participant to mongodb. ")
            spider.logger.info(dict(item))
            item = dict(item)
            item.pop('rank_type')
            participant_coll.insert_one(item)
            return item

