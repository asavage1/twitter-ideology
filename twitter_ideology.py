import csv
import json
import time
from collections import defaultdict

import twint
import rpy2.robjects as robjects
from googleapiclient import discovery, errors

from estimate_ideology import estimateIdeology2


def get_followers(user, output_file):
    c = twint.Config()
    c.Username = user
    c.Output = output_file

    try:
        twint.run.Followers(c)
    except TimeoutError:
        time.sleep(5)
        get_followers(user, output_file)
    except TypeError:
        pass


def get_all_followers(users):
    for user in users:
        get_followers(user, f'actor_followers/{user}.txt')


def reverse_index_all_followers(users, index_filename=None):
    followers = defaultdict(list)
    for user in users:
        try:
            with open(f'actor_followers/{user}.txt', 'r') as f:
                for line in f:
                    followers[line.rstrip()].append(user)
        except FileNotFoundError:
            print(f'{user}\'s follower list does not exist.')
            continue

    if index_filename:
        with open(index_filename, 'w') as f:
            json.dump(followers, f)

    return followers


def scrape_tweets(keyword_set_names, keyword_sets, years, limit=2500):
    get_query = lambda search_words: r'"' + r'" OR "'.join(search_words) + r'"'

    for index, keyword_set in enumerate(keyword_sets):
        for year in years:
            query = get_query(keyword_set)
            output_filename = f'{keyword_set_names[index]}.csv'

            for i in range(31):  # 31 Days in March
                c = twint.Config()
                c.Search = query
                c.Lang = 'en'
                c.Limit = limit
                c.Output = output_filename
                c.Store_csv = True
                if i < 30:
                    c.Since = f'{year}-03-{i + 1:02d}'
                    c.Until = f'{year}-03-{i + 2:02d}'
                else:
                    c.Since = f'{year}-03-31'
                    c.Until = f'{year}-04-01'

                try:
                    twint.run.Search(c)
                except:
                    time.sleep(5)


def get_perspective(ser, text):
    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}}
    }
    if 'http' in text and len(text.split()) == 1:  # Just a link, tool errors out
        return None

    try:
        response = ser.comments().analyze(body=analyze_request).execute()
        return response['attributeScores']['TOXICITY']['summaryScore']['value']
    except errors.HttpError as network_error:
        print(network_error)
        return None
    except ConnectionResetError:
        return ConnectionResetError


def analyze_tweets(actors, followers, topics, actor_filename, common_filename):
    with open(actor_filename, 'w') as csvwritefileactor:
        with open(common_filename, 'w') as csvwritefilecommon:
            csv_writer_actor = csv.writer(csvwritefileactor)
            csv_writer_common = csv.writer(csvwritefilecommon)
            csv_writer_actor.writerow(
                ['Date', 'Time', 'User', '(n)Replies', '(n)Retweets', 'Tweet', 'Topic', 'Ideology Score', 'Toxicity'])
            csv_writer_common.writerow(
                ['Date', 'Time', 'User', '(n)Replies', '(n)Retweets', 'Tweet', 'Topic', 'Ideology Score', 'Toxicity'])
            writer = None

            perspective_window = 100  # in seconds
            nrequests = 0
            window_start = time.time()
            max_requests = 1000

            for topic in topics:
                with open(f'{topic}/tweets.csv', 'r') as csvreadfile:
                    csv_reader = csv.reader(csvreadfile)
                    headers = None
                    for i, row in enumerate(csv_reader):
                        if headers is None:
                            headers = row
                        else:
                            qi = lambda col_header: row[headers.index(col_header)]
                            user = qi('username')

                            if user in actors:
                                writer = csv_writer_actor
                            else:
                                writer = csv_writer_common

                            ideology = estimateIdeology2(user, followers[user]) if user in followers else 0

                            tweet = qi('tweet')
                            if nrequests == max_requests:
                                sleep_time = perspective_window - (time.time() - window_start)
                                if sleep_time > 0:
                                    time.sleep(sleep_time)
                                else:
                                    time.sleep(perspective_window)
                                window_start = time.time()
                                nrequests = 0

                            perspective_score = get_perspective(service, tweet)
                            nrequests += 1

                            if perspective_score == ConnectionResetError:
                                print(f'Stopped at row {i} in file {topic}')
                                exit(1)

                            writer.writerow(
                                [qi('date'), qi('time'), user, qi('replies_count'), qi('retweets_count'), tweet, topic,
                                 ideology, perspective_score])


if __name__ == '__main__':
    robjects.r['load'](r'/path/to/refdataCA.rdata')  # TODO: edit path
    actors = robjects.r['refdataCA'][4]
    get_all_followers(actors)
    followers = reverse_index_all_followers(actors, 'indexed_actor_followers')

    years = ['2013', '2014', '2017', '2018']
    keyword_sets = [
        {'Obamacare', 'Affordable Care Act', 'American Health Care Act', 'Trumpcare', 'RyanCare', 'repeal and replace'},
        {'school shooting', 'Sandy Hook', 'Parkland', 'Marjory Stoneman Douglas', 'gun rights', 'gun control', 'NRA',
         'Second Amendment', '2nd Amendment'},
        {'the environment', 'climate change', 'global warming', 'carbon emissions', 'sustainability', 'fossil fuels'},
        {'government deficit', 'national debt', 'budget deficit', 'entitlements', 'welfare', 'social security',
         'Medicare',
         'minimum wage', 'unemployment', 'tax reform', 'tax plan', 'Tax Cuts and Jobs Act', 'economic inequality',
         'income inequality'},
        {'DACA', 'Deferred Action for Childhood Arrivals', 'DREAMers', 'Muslim ban', 'illegal immigrants',
         'illegal immigration', 'border security', 'southern border', 'border wall'},
        {'marriage equality', 'same sex marriage', 'homophobia', 'black lives matter', 'police brutality', 'racism',
         'discrimination', 'sexism', 'feminism'},
        {'Congress', 'SCOTUS', 'Supreme Court', 'House of Representatives', 'Senate', 'Executive Branch', 'Presidency',
         'POTUS', 'President of the United Statues', 'Trump', 'Obama', 'State of the Union', 'SOTU'}
    ]
    keyword_set_names = ['Health Care', 'Gun Violence', 'Environment', 'Fiscal', 'Immigration', 'Discrimination',
                         'Government']

    scrape_tweets(keyword_set_names, keyword_sets, years)

    perspective_key = '...'  # TODO: Insert perspective key
    service = discovery.build('commentanalyzer', 'v1alpha1', developerKey=perspective_key)
    analyze_tweets(actors, followers, keyword_set_names, 'actor_tweets.csv', 'common_tweets.csv')
