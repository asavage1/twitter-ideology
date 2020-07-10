# twitter-ideology

A tool that can analyze the ideologies of a large amount of twitter users using the algorithm provided [here](https://github.com/pablobarbera/twitter_ideology).

This tool uses python 3.6+

1. `git clone https://github.com/asavage1/twitter-ideology.git`
2. Download refdataCA.rdata from the link above (file in the repo is located [here](https://github.com/pablobarbera/twitter_ideology/blob/master/pkg/tweetscores/data/refdataCA.rdata))
3. Edit the path to the "refdataCA.rdata" you just downloaded in "twitter_ideology.py" and "estimate_ideology.py"
4. Create a "keys.json" file which contains a key for the Google perspective api you plan on using. It should contain something like this:

```
{"perspective_key":"ExampleKey"}
```

4. `python twitter_ideology.py` should do the rest.

## Using get_followers.py alone

You can scrape the followers of the NYU actors without automatically doing the rest. Do this by cloning the repo as above, then running `python get_followers.py`.

You can pass in the optional flags listed below, if desired:

```
-s, --start  | The numerical index in the NYU actors list at which to start getting the followers of the actors

-e, --end    | The numerical index in the NYU actors list at which to end getting the followers of the actors

-p, --person | Only used if --start is not used. The first person in the list of NYU actors to get followers for, specified by their twitter handle.
```

For example, `python -s 100 -e 102 get_followers.py` will only get the followers of the 100th and 101st actors in the NYU actors list.
