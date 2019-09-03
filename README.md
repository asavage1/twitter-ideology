# twitter-ideology
We want to use nyu twitter ideology estimation tool
1. Download the refdataCA.rdata file to use it, format path in actor_intersect.py
2. Scrape all followers of actors used for estimation in this tool (get_all_actor_followers() in
actor_intersect.py without any indexing into actors).
3. Index all actors into a json file (index_followers() in actor_intersect.py)
4. (optional) Get the ideology scores of actor followers by using get_actor_scores()
5. Gotta get tweets now, use tweet_scraping.py
6. Now we got it all, use analyze_tweets.py with estimate_ideology.py to 
