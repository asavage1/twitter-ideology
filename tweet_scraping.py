import twint
from itertools import zip_longest


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

actor_handles = ['JoeBiden', 'HillaryClinton']
for actor_handle in actor_handles:
    file_start = 'actor_files/' + actor_handle
    get_followers(actor_handle, file_start + '-followers.txt')

for actor_handle in actor_handles:
    file_start = 'actor_files/' + actor_handle

    # parse the follower list
    follower_list = []
    with open(file_start + '-followers.txt', 'r') as f:
        for line in f:
            if '|' not in line:
                follower_list.append(line.rstrip())

    res = get_friends(follower_list, file_start + '-friends.txt')
    while res is not None:
        res = get_friends(follower_list[res:], file_start + '-friends.txt')

    followers_dict = {}
    with open(file_start + '-friends.txt', 'r') as f:
        last_seen = ''
        for line in f:
            if '|' in line:
                last_seen = line.split(' | ')[2][1:]
                if last_seen not in followers_dict:
                    followers_dict[last_seen] = []
            else:
                followers_dict[last_seen].append(line.rstrip())

    with open(file_start + '-friends.txt', 'w') as f:
        f.write(','.join(followers_dict.keys()) + '\n')
        for line in zip_longest(*followers_dict.values(), fillvalue=''):
            f.write(','.join(line) + '\n')

print('done')
