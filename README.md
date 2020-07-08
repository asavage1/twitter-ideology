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
