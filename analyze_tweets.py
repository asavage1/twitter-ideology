from estimate_ideology import estimateIdeology2
from googleapiclient import discovery, errors
import csv
import json
import rpy2.robjects as robjects
import time

TOPICS = ['Health Care', 'Gun Violence', 'Environment',
          'Fiscal', 'Immigration', 'Discrimination', 'Government']
with open("keys.json") as f:
    keys = json.load(f)

PERSPECTIVE_KEY = keys["perspective_key"]
SERVICE = discovery.build('commentanalyzer', 'v1alpha1',
                          developerKey=PERSPECTIVE_KEY)

robjects.r['load'](r'~/Downloads/refdataCA.rdata')
ACTORS = robjects.r['refdataCA'][4]

USERS = None
with open('twitter_followers.json', 'r') as f:
    USERS = json.load(f)


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


with open('aggregated_actor_tweets_large.csv', 'a') as csvwritefileactor:
    with open('aggregated_tweets_large.csv', 'a') as csvwritefilecommon:
        csv_writer_actor = csv.writer(csvwritefileactor)
        csv_writer_common = csv.writer(csvwritefilecommon)
        csv_writer_actor.writerow(['Date', 'Time', 'User', '(n)Replies',
                                   '(n)Retweets', 'Tweet', 'Topic', 'Ideology Score', 'Toxicity'])
        csv_writer_common.writerow(['Date', 'Time', 'User', '(n)Replies',
                                    '(n)Retweets', 'Tweet', 'Topic', 'Ideology Score', 'Toxicity'])
        writer = None

        perspective_window = 100  # in seconds
        nrequests = 0
        window_start = time.time()
        max_requests = 1000

        for topic in TOPICS:
            with open(r'{}_large/tweets.csv'.format(topic), 'r') as csvreadfile:
                csv_reader = csv.reader(csvreadfile)
                headers = None
                for i, row in enumerate(csv_reader):
                    if headers is None:
                        headers = row
                    else:
                        def qi(
                            col_header): return row[headers.index(col_header)]
                        # date, time, username, tweet, replies_count, retweets_count
                        # topic, ideology score, toxicity
                        user = qi('username')

                        if user in ACTORS:
                            writer = csv_writer_actor
                        else:
                            writer = csv_writer_common

                        ideology = estimateIdeology2(
                            user, USERS[user]) if user in USERS else 0

                        tweet = qi('tweet')
                        if nrequests == max_requests:
                            sleep_time = perspective_window - \
                                (time.time() - window_start)
                            if sleep_time > 0:
                                time.sleep(sleep_time)
                            else:
                                time.sleep(perspective_window)
                            window_start = time.time()
                            nrequests = 0

                        perspective_score = get_perspective(SERVICE, tweet)
                        nrequests += 1

                        if perspective_score == ConnectionResetError:
                            print('Stopped at row {} in file {}'.format(i, topic))
                            exit(1)

                        writer.writerow([qi('date'), qi('time'), user, qi('replies_count'), qi(
                            'retweets_count'), tweet, topic, ideology, perspective_score])
