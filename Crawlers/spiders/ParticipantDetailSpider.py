from scrapy.spiders.init import InitSpider
from scrapy.http import Request
from ..items import IndividualStepsItem
from ..settings import DATABASE
import json, pymongo

default_db = DATABASE.get('default')
db = pymongo.MongoClient(default_db.get('HOST'))[default_db.get('DB')]
participants_coll = db[default_db.get('PARTICIPANTS_COLL')]


class ParticipantDetailSpider(InitSpider):
    name = 'participant_spider'
    allowed_domains = ['']
    login_page = ''
    login_validate_page = ''
    participant_page = ''.format
    custom_settings = {
        'MONGO_DB_PARTICIPANT_DETAIL_COLL': 'participants',
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
        usr = 'username'
        pswd = 'password'
        data = {token_name: token_val, 'Username': usr, 'Password': pswd}
        return Request(url=self.login_validate_page, method='POST',
                       body=json.dumps(data),
                       headers={'Content-Type':'application/json'},
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

    def start_requests(self):
        participants = list(participants_coll.find({}))
        for participant in participants:
            id = participant.get('participant_id')
            participant_url = self.participant_page(id=id)
            yield Request(url=participant_url,
                          callback=self.parse,
                          dont_filter=True)

    def parse(self, response):
        text = response.text
        print(text)