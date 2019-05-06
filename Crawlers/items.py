# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class IndividualStepsItem(scrapy.Item):
    participant_id = scrapy.Field()
    nickname = scrapy.Field()
    device_type = scrapy.Field()
    has_device = scrapy.Field()
    team_id = scrapy.Field()
    team_name = scrapy.Field()
    team_color = scrapy.Field()
    team_emblem = scrapy.Field()
    was_merged_onto_team = scrapy.Field()

    # all steps
    all_steps = scrapy.Field()
    # steps stats
    battle_stats = scrapy.Field()
    # round stats
    round_stats = scrapy.Field()


class IndividualRankItem(scrapy.Item):
    rank_type = scrapy.Field()
    participant_id = scrapy.Field()
    rank = scrapy.Field()
    nickname = scrapy.Field()
    total_steps = scrapy.Field()
    color = scrapy.Field()
    wins = scrapy.Field()


class TeamRankItem(scrapy.Item):
    rank_type = scrapy.Field()
    team_id = scrapy.Field()
    rank = scrapy.Field()
    name = scrapy.Field()
    color = scrapy.Field()
    emblem = scrapy.Field()
    cumulative_steps = scrapy.Field()
    wins = scrapy.Field()