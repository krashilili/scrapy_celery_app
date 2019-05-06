import scrapy, re, json, pymongo
from scrapy.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from ..items import TeamRankItem, IndividualRankItem
# from ..settings import DATABASE, DRIVER_URL_PREX

# default_db = DATABASE.get('default')
# db = pymongo.MongoClient(default_db.get('HOST'))[default_db.get('DB')]
# io_data_coll = db[default_db.get('IOData_COLL')]


class CustomSpider(InitSpider):
    name = 'custom_spider'
    allowed_domains = ['']
    login_page = ''
    login_validate_page = ''
    start_urls = ['team_ranks_page', 'participant_ranks_page']

    custom_settings = {
        'MONGO_DB_TEAM_COLL': 'team_rank',
        'MONGO_DB_PARTICIPANT_COLL': 'participant_rank',
    }

    def init_request(self):
        """This function is called before crawling starts."""
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        """Generate a login request."""
        cookies = response.headers.getlist('Set-Cookie')
        token = cookies[-1].decode('ascii').split('=')
        token_name = token[0]
        token_val = token[1].split(';')[0]

        # form data
        usr = ''
        pswd = ''
        data = {token_name: token_val, 'Username': usr, 'Password': pswd}
        return Request(url=self.login_validate_page, method='POST',
                       body=json.dumps(data),
                       headers={'Content-Type': 'application/json'},
                       callback=self.after_login,
                       dont_filter=True)

    def after_login(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        res=response.text
        res_json = json.loads(res)
        status = res_json.get('Success')
        if status:
            print("Login successfully!")
            # Now the crawling can begin..
            return self.initialized()
        else:
            print("Failed to login!")

    def parse(self, response):
        text_str = response.text
        resp_dict = json.loads(text_str)
        status = resp_dict.get('Success')
        url = response.url
        if status:
            data = resp_dict.get('Data')
            if 'Team' in url:
                # team_count = data.get('TeamCount')
                teams = data.get('TeamRankings')
                for team_data in teams:
                    team = TeamRankItem()
                    team['rank_type'] = 'Team'
                    team['team_id'] = team_data.get('TeamId')
                    team['rank'] = team_data.get('Rank')
                    team['name'] = team_data.get('Name')
                    team['color'] = team_data.get('Color')
                    team['emblem'] = team_data.get('Emblem')
                    team['cumulative_steps'] = team_data.get('CumulativeSteps')
                    team['wins'] = team_data.get('Wins')
                    yield team
            elif 'Participants' in url:
                participants = data.get('ParticipantsRanksListItems')
                for participant in participants:
                    part_item = IndividualRankItem()
                    part_item['rank_type'] = 'Participant'
                    part_item['participant_id'] = participant.get('BattleParticipantId')
                    part_item['rank'] = participant.get('Rank')
                    part_item['nickname'] = participant.get('NickName')
                    part_item['total_steps'] = participant.get('TotalSteps')
                    part_item['color'] = participant.get('Color')
                    part_item['wins'] = participant.get('Wins')
                    yield part_item
