import csv
import tweepy
from dotenv import dotenv_values
from os.path import join, dirname, abspath

from libs.notifications import Notifications


class ConnectToTwitter(Notifications):

    def __init__(self):
        super().__init__()
        self.login_twitter()

    def login_twitter(self):
        """
        Function to connect to twitter's API. It reads variables API_KEY, API_SECRET, ACCESS_TOKEN and
        ACCESS_TOKEN_SECRET from .env
        :return:
        """
        self.notification("Connecting to twitter")
        auth = tweepy.OAuthHandler(
            dotenv_values()['API_KEY'], dotenv_values()['API_SECRET'])
        auth.set_access_token(dotenv_values()['ACCESS_TOKEN'], dotenv_values()[
            'ACCESS_TOKEN_SECRET'])
        self.api = tweepy.API(auth, wait_on_rate_limit=True)


class ExtractTwitterInfo(ConnectToTwitter):
    path = dirname(abspath(__file__))

    def __init__(self):
        super().__init__()
        self.read_terms_to_search()

    def read_terms_to_search(self):
        """
        Reads the file terms_to_search.csv and search the terms which are inside it
        """
        self.notification("Starting a tweet extraction")

        with open('terms_to_search.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.search_term(row[0])

    @staticmethod
    def format_search_to_get_exact_match(string: str):
        """
        Formats an string to the format which twitter's API needs to get an exact match
        :param string: An string
        """

        isRetweet = ' -filter:retweets' if dotenv_values()[
            'EXCLUDE_RETWEETS'] else ''

        return f'"{string.lower().replace(" ", "&")}" {isRetweet}'

        # isRetweet = ' -is:retweet' if dotenv_values()['EXCLUDE_RETWEETS'] else ''
        # return f'"{string.lower().replace(" ", " AND ")}" {isRetweet}'

    def write_into_csv(self, ls_data: list):
        with open(join(self.path, dotenv_values()['OUTPUT_FILE']), 'a') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(ls_data)

    def search_term(self, search: str):
        contador = 1
        self.notification(
            f'Extracting tweets which includes the term -> {search}')
        print(self.format_search_to_get_exact_match(search))
        for tweet in tweepy.Cursor(self.api.search_tweets,
                                   q=self.format_search_to_get_exact_match(
                                       search),
                                   count=100,
                                   tweet_mode='extended').items():

            if contador % 100 == 0:
                self.notification(f'Extracting tweets - {contador}')

            contador += 1

            ft_twit = tweet.full_text.encode("utf-8").decode("utf-8")

            try:
                ft_rt_twit = tweet.retweeted_status.full_text.encode(
                    "utf-8").decode("utf-8")

                if len(ft_rt_twit) > ft_twit:
                    ft_twit = ft_rt_twit
            except:
                pass

            # columns = ["search_term", "user", "user_name", "twit_id", "created_at", "favorite_count",
            #            "retweet_count", "text", "hashtags", "user_mentions",
            #            "urls", "in_reply_to_status_id", "in_reply_to_status_id_str",
            #            "in_reply_to_user_id", "in_reply_to_screen_name", "text_range", "geo", "coordinates"])

            self.write_into_csv([search,
                                tweet.user.screen_name,
                                tweet.user.name,
                                tweet.id_str,
                                tweet.created_at,
                                tweet.favorite_count,
                                tweet.retweet_count,
                                ft_twit,
                                [i['text']
                                    for i in tweet.entities['hashtags']],
                                [i['screen_name']
                                 for i in tweet.entities['user_mentions']],
                                [i['display_url']
                                 for i in tweet.entities['urls']],
                                tweet.in_reply_to_status_id,
                                tweet.in_reply_to_status_id_str,
                                tweet.in_reply_to_user_id,
                                tweet.in_reply_to_screen_name,
                                tweet.display_text_range[1],
                                tweet.geo,
                                tweet.coordinates])


if __name__ == "__main__":
    ExtractTwitterInfo()
