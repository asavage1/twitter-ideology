import argparse
import constants
import os
import time
from collections import defaultdict

import twint
import rpy2.robjects as robjects

TIME_TO_SLEEP_ON_TWITTER_REJECT_IN_SECONDS = 5


def get_followers(user, output_file):
    c = twint.Config()
    c.Username = user
    c.Output = output_file
    c.Hide_output = True

    try:
        twint.run.Followers(c)
    except TimeoutError:
        time.sleep(TIME_TO_SLEEP_ON_TWITTER_REJECT_IN_SECONDS)
        get_followers(user, output_file)
    except TypeError:
        pass


def get_all_followers(users):
    try:
        os.mkdir(constants.FOLLOWERS_OUTPUT_FOLDER_NAME)
    except FileExistsError:
        pass

    for user in users:
        print(f'Getting followers for {user}')
        get_followers(
            user, f'{constants.FOLLOWERS_OUTPUT_FOLDER_NAME}/{user}.txt')


def main(users, args=None):
    get_all_followers(users[args.start: args.end])


if __name__ == "__main__":
    robjects.r['load'](constants.PATH_TO_REFDATA)
    actors = robjects.r['refdataCA'][4]

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", type=int,
                        help="start index into NYU users list",
                        default=0)
    parser.add_argument("-e", "--end", type=int,
                        help="end index into NYU users list",
                        default=len(actors))
    parser.add_argument("-p", "--person", type=str,
                        help="first person to search for in the NYU users")
    args = parser.parse_args()

    if args.person and args.start == 0:
        try:
            args.start = actors.index(args.person)
        except ValueError:
            print(f'${args.person} not in list of NYU actors')

    main(actors, args)
