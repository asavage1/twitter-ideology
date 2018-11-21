import twint


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


def get_followers(follow_list, output_folder):
    error_count = 0

    for handle in follow_list:
        c = twint.Config()
        c.Username = handle
        c.Output = output_folder
        c.Store_csv = True
        c.Limit = 5000

        try:
            twint.run.Followers(c)
        except TypeError:
            error_count += 1

    return error_count


def get_friends(handle, output_folder):
    error_count = 0

    c = twint.Config()
    c.Username = handle
    c.Output = output_folder
    c.Store_csv = True
    # c.User_full = False

    try:
        twint.run.Following(c)
    except TypeError:
        error_count += 1

    return error_count


# search_phrases = ['Trump', 'Pres', 'POTUS', 'President', 'Prez']
# ec = search_for_all_handles(get_users_from_file('users.txt'), search_phrases, 'test_search')

get_friends('mike_pence', 'test_friends_output')
get_friends('mike_pence', 'test_friends_output')
