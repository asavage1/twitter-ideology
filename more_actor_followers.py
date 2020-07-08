from estimate_ideology import estimateIdeology2
import json
import csv

actors = ['realDonaldTrump', 'BarackObama',
          'HillaryClinton', 'billmaher', 'VanJones68']
actor_scores = [[] for _ in range(len(actors))]

users = None
with open('twitter_followers.json', 'r') as f:
    users = json.load(f)

for actor in actors:
    n = 0
    with open(r'/Users/Andrew/Desktop/School/Other/Programs/twitter-ideology-project/twitter-ideology/actor_followers/{}.txt'.format(actor), 'r') as f:
        fl = True
        for line in f:
            if fl:
                fl = False
                continue
            follower = line.rstrip()
            score = estimateIdeology2(follower, users[follower])
            if score is not None:
                actor_scores[actors.index(actor)].append(score)
                n += 1
                if n == 2500:
                    break

transposed_scores = map(list, zip(*actor_scores))
with open('extra_followers.csv', 'w') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(actors)
    for row in transposed_scores:
        csv_writer.writerow(row)
