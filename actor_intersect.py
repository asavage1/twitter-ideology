import json
import os
import rpy2.robjects as robjects
import time
import twint
from collections import defaultdict
from itertools import zip_longest

import estimate_ideology

PATH_TO_REFDATACA = r'~/Downloads/refdataCA.rdata'
robjects.r['load'](PATH_TO_REFDATACA)
ACTORS = robjects.r['refdataCA'][4]

REPUBLICAN_ACTORS = ['realDonaldTrump', 'mike_pence', 'SpeakerRyan',
                     'SenateMajLdr', 'tedcruz', 'SenatorCollins', 'LindseyGrahamSC', 'SenJohnMcCain']
DEMOCRATIC_ACTORS = ['BarackObama', 'JoeBiden', 'HillaryClinton', 'SpeakerPelosi',
                     'SenSchumer', 'BernieSanders', 'Sen_JoeManchin', 'SenGillibrand']
RIGHT_LEANING_MEDIA = ['BillOReilly', 'seanhannity',
                       'IngrahamAngle', 'benshapiro', 'hughhewitt']
LEFT_LEANING_MEDIA = ['maddow', 'billmaher',
                      'VanJones68', 'chrislhayes', 'Lawrence']
ALL_ACTOR_HANDLES = REPUBLICAN_ACTORS + DEMOCRATIC_ACTORS + \
    RIGHT_LEANING_MEDIA + LEFT_LEANING_MEDIA


def get_followers(handle, output_file_or_folder, limit):
    error_count = 0

    c = twint.Config()
    c.Username = handle
    c.Output = output_file_or_folder
    if limit:
        c.Limit = limit

    try:
        twint.run.Followers(c)
    except TypeError:
        error_count += 1
    except TimeoutError:  # on failed network connections, wait 5? seconds then try again
        time.sleep(5)
        get_followers(handle, output_file_or_folder, limit)

    return error_count


def get_all_actor_followers(limit):
    for actor in ACTORS:
        get_followers(actor, 'actor_followers/' + actor + '.txt', limit)


def index_followers():
    users = defaultdict(list)
    for actor in ACTORS:
        try:
            with open('actor_followers/' + actor + '.txt', 'r') as f:
                for line in f:
                    users[line.rstrip()].append(actor)
            print(actor)
        except FileNotFoundError:
            print(actor + ' not found')
            continue

    with open('twitter_followers.json', 'w') as f:
        json.dump(users, f)


def get_actor_scores(limit):
    users = None
    with open('twitter_followers.json', 'r') as f:
        users = json.load(f)

    for actor_handle in ALL_ACTOR_HANDLES:
        file_name = 'actor_files/' + actor_handle + '-followers.txt'
        get_followers(actor_handle, file_name, limit)

    all_scores = []
    used_handles = []

    for actor_handle in ALL_ACTOR_HANDLES:
        file_name = 'actor_files/' + actor_handle + '-followers.txt'
        scores = []

        if not os.path.exists(file_name):
            get_followers(actor_handle, file_name, limit)

        try:
            with open(file_name, 'r') as f:
                for line in f:
                    user = line.rstrip()
                    if user in users:
                        score = estimate_ideology.estimateIdeology2(
                            user, users[user])
                        scores.append(score)
            all_scores.append(scores)
            used_handles.append(actor_handle)
        except FileNotFoundError:
            print(actor_handle)

    all_scores_by_column = list(
        map(list, zip_longest(*all_scores, fillvalue=0)))
    import csv
    with open('actor_scores.csv', 'w', newline='') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow(used_handles)
        for score_row in all_scores_by_column:
            csv_writer.writerow(score_row)


def main():
    limit = 20000
    get_all_actor_followers(limit)
    index_followers()
    # get_actor_scores(limit)


if __name__ == "__main__":
    main()
