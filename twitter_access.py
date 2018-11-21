import base64
import requests
import json
import time

run_type = 'list'


def parse_keys(file_name):
    lines = []
    with open(file_name, 'r') as f:
        lines += [line.rstrip() for line in f.readlines()]
    return lines[0].split()[-1], lines[1].split()[-1]


def authorize_twitter_access(api_key, api_secret_key):
    key_secret = '{}:{}'.format(api_key, api_secret_key).encode('ascii')
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')

    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)

    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    auth_data = {
        'grant_type': 'client_credentials'
    }

    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

    if auth_resp.status_code != 200:
        raise Exception('Bad authorization')

    return auth_resp.json()['access_token']


def get_followers(access_token, handle, count=100):
    base_url = 'https://api.twitter.com/'
    get_followers_url = '{0}1.1/followers/{1}.json'.format(base_url, run_type)
    followers_headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    followers_params = {
        'screen_name': handle,
        'count': count,
    }

    followers_resp = requests.get(get_followers_url, headers=followers_headers,
                                  params=followers_params)

    if followers_resp.status_code != 200:
        return 'i cannot'

    if run_type == 'ids':
        return json.loads(followers_resp.text)['ids']
    all_user_objects = json.loads(followers_resp.text)['users']
    return [user['screen_name'] for user in all_user_objects]


rep = ['realDonaldTrump', 'mike_pence', 'SpeakerRyan', 'SenateMajLdr',
       'tedcruz', 'SenatorCollins', 'LindseyGrahamSC', 'SenJohnMcCain']
dem = ['BarackObama', 'JoeBiden', 'HillaryClinton', 'NancyPelosi',
       'SenSchumer', 'BernieSanders', 'Sen_JoeManchin', 'SenGillibrand']
rl_media = ['BillOReilly', 'seanhannity', 'IngrahamAngle', 'benshapiro', 'hughhewitt']
ll_media = ['maddow', 'billmaher', 'VanJones68', 'chrislhayes', 'Lawrence']
actor_handles = rep + dem + rl_media + ll_media

untracked = []
actors_dict = {}
api_key, api_secret_key = parse_keys('access_keys.txt')
access_token = authorize_twitter_access(api_key, api_secret_key)
for handle in actor_handles:
    ret = get_followers(access_token, handle, 5000)
    if type(ret) is str:
        untracked.append(handle)
    else:
        actors_dict[handle] = ret
    time.sleep(60)  # Delay for 1 minute (15 requests in 15 minutes are allowed)

with open("serialized_actor_followers_{}.txt".format(run_type), "w") as f:
    json.dump(actors_dict, f)

print('done')
