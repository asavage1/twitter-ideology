import twint
from itertools import zip_longest
import aiohttp
import time


def get_users_from_file(file_name):
    handles = []
    with open(file_name, 'r') as f:
        lines = [line.rstrip() for line in f.readlines()]
        handles += lines
    return handles


def search_for_all_handles(handles, search_phrases, output_folder):
    error_count = 0
    for handle in handles:
        error_count += search_phrases_in_handle(handle, search_phrases, output_folder)
    return error_count


def search_phrases_in_handle(handle, search_phrases, output_folder):
    error_count = 0

    for search_phrase in search_phrases:
        c = twint.Config()
        c.Username = handle
        c.Search = search_phrase
        c.Since = '2015-06-16'
        c.Output = output_folder
        c.Store_csv = True
        # c.Custom["username"] = ["username"]
        # c.Custom["date"] = ["date"]
        # c.Custom["tweet"] = ["tweet"]
        # c.Custom["replies"] = ["replies"]
        # c.Custom["retweets"] = ["retweets"]
        # c.Custom["likes"] = ["likes"]

        try:
            twint.run.Search(c)
        except TypeError:
            error_count += 1

    return error_count


def get_followers(handle, output_file_or_folder):
    error_count = 0

    c = twint.Config()
    c.Username = handle
    c.Output = output_file_or_folder
    # c.Store_csv = True
    c.Limit = 5000

    try:
        twint.run.Followers(c)
    except TypeError:
        error_count += 1

    return error_count


def get_friends(handles, output_file_or_folder):
    # error_count = 0

    for handle in handles:
        c = twint.Config()
        c.Username = handle
        c.Output = output_file_or_folder
        # c.Store_csv = True
        # c.User_full = False
        try:
            twint.run.Following(c)
        except TypeError:
            continue
            # error_count += 1
        except TimeoutError:
            return handles.index(handle)

    return None


# search_phrases = ['Trump', 'Pres', 'POTUS', 'President', 'Prez']
# ec = search_for_all_handles(get_users_from_file('users.txt'), search_phrases, 'test_search')

# rep = ['realDonaldTrump', 'mike_pence', 'SpeakerRyan', 'SenateMajLdr',
#        'tedcruz', 'SenatorCollins', 'LindseyGrahamSC', 'SenJohnMcCain']
# dem = ['BarackObama', 'JoeBiden', 'HillaryClinton', 'NancyPelosi',
#        'SenSchumer', 'BernieSanders', 'Sen_JoeManchin', 'SenGillibrand']
# rl_media = ['BillOReilly', 'seanhannity', 'IngrahamAngle', 'benshapiro', 'hughhewitt']
# ll_media = ['maddow', 'billmaher', 'VanJones68', 'chrislhayes', 'Lawrence']
# actor_handles = rep + dem + rl_media + ll_media
# for actor_handle in actor_handles:
#     file_start = 'actor_files/' + actor_handle
#     get_followers(actor_handle, file_start + '-followers.txt')

# for actor_handle in actor_handles:
#     file_start = 'actor_files/' + actor_handle
#
#     # parse the follower list
#     follower_list = []
#     with open(file_start + '-followers.txt', 'r') as f:
#         for line in f:
#             if '|' not in line:
#                 follower_list.append(line.rstrip())
#
#     res = get_friends(follower_list, file_start + '-friends.txt')
#     while res is not None:
#         res = get_friends(follower_list[res:], file_start + '-friends.txt')
#
#     followers_dict = {}
#     with open(file_start + '-friends.txt', 'r') as f:
#         last_seen = ''
#         for line in f:
#             if '|' in line:
#                 last_seen = line.split(' | ')[2][1:]
#                 if last_seen not in followers_dict:
#                     followers_dict[last_seen] = []
#             else:
#                 followers_dict[last_seen].append(line.rstrip())
#
#     with open(file_start + '-friends.txt', 'w') as f:
#         f.write(','.join(followers_dict.keys()) + '\n')
#         for line in zip_longest(*followers_dict.values(), fillvalue=''):
#             f.write(','.join(line) + '\n')

# print('done')


def get_tweets(search_phrase, years, days, output_file, limits, ngroups=2):
    geos = ["40.592034,-103.561408,1000mi", "38.470919,-85.076813,1000mi"]
    for year in years:
        for day, limit in zip(days, limits):
            for geo in geos:
                # year = random.choice(years)
                # day = random.randint(1, ndays)

                error_count = 0

                c = twint.Config()
                c.Search = search_phrase
                c.Since = '{}-03-{:02d}'.format(year, day)
                c.Until = '{}-03-{:02d}'.format(year, day + 1)
                c.Lang = 'en'
                c.Limit = limit
                c.Geo = geo
                # c.User_info = True
                c.Output = output_file
                c.Store_csv = True
                # c.Custom["username", "tweet"] = ["username", "tweet"]
                # c.Custom["date"] = ["date"]
                # c.Custom["tweet"] = ["tweet"]
                # c.Custom["replies"] = ["replies"]
                # c.Custom["retweets"] = ["retweets"]
                # c.Custom["likes"] = ["likes"]
                # TODO: Followers

                try:
                    x = twint.run.Search(c)
                except TypeError:
                    error_count += 1
                except aiohttp.client_exceptions.ClientOSError:
                    error_count += 1
                    time.sleep(5)


import random

ntweets = 35715
ngroups = 36
ntweets_in_group = 1000
years = ['2013', '2014', '2017', '2018']
keyword_sets = [
    {'Obamacare', 'Affordable Care Act', 'American Health Care Act', 'Trumpcare', 'RyanCare', 'repeal and replace'},
    {'school shooting', 'Sandy Hook', 'Parkland', 'Marjory Stoneman Douglas', 'gun rights', 'gun control', 'NRA',
     'Second Amendment', '2nd Amendment'},
    {'the environment', 'climate change', 'global warming', 'carbon emissions', 'sustainability', 'fossil fuels'},
    {'government deficit', 'national debt', 'budget deficit', 'entitlements', 'welfare', 'social security', 'Medicare',
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

################# VARIABLES ###############
# index = keyword_set_names.index('Health Care')
# year = '2013'
limit = 2500
days = 31
#####################################################

# days = [0 for _ in range(30)]
# for _ in range(int(10000 / 30)):
#     days[random.randint(0, 29)] += 100


for index in range(len(keyword_sets)):
    for year in ['2013', '2014', '2017', '2018']:
        query = r'"' + r'" OR "'.join(keyword_sets[index]) + r'"'
        output_file_name = keyword_set_names[index] + '_large.csv'

        for i in range(days):
            e = 0
            c = twint.Config()
            c.Search = query
            if i < 30:
                c.Since = '{}-03-{:02d}'.format(year, i + 1)
                c.Until = '{}-03-{:02d}'.format(year, i + 2)
            else:
                c.Since = '{}-03-31'.format(year)
                c.Until = '{}-04-01'.format(year)
            c.Lang = 'en'
            c.Limit = limit
            # c.User_info = True
            c.Output = output_file_name
            c.Store_csv = True

            try:
                x = twint.run.Search(c)
            except TypeError:
                e += 1
            except aiohttp.client_exceptions.ClientOSError:
                e += 1
                time.sleep(5)
            except:
                e += 1
                time.sleep(5)

# get_tweets(query, years=['2018'], days=[i + 1 for i in range(30)], output_file=output_file_name,
#            limits=[1000 for _ in range(30)])

# full = [False for _ in range(len(keyword_set_names))]
# while not all(full):
#     for name, keyword_set in zip([keyword_set_names[index]], [keyword_sets[index]]):
#         query = r'"' + r'" OR "'.join(keyword_set) + r'"'
#         output_file_name = name + '2.csv'
#         # output_file_name = 'tscrape.csv'
#
#         # nlines = 0
#         # with open(r'{}/tweets.csv'.format(name), 'r') as f:
#         #     nlines = len(list(f.readlines()))
#         # if nlines >= ntweets:
#         #     full[keyword_set_names.index(name)] = True
#         #     continue
