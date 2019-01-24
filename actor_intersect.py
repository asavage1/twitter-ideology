import twint
import rpy2.robjects as robjects
import time


def get_followers(handle, output_file_or_folder):
    error_count = 0

    c = twint.Config()
    c.Username = handle
    c.Output = output_file_or_folder

    try:
        twint.run.Followers(c)
    except TypeError:
        error_count += 1
    except TimeoutError:  # on failed network connections, wait 5? seconds then try again
        time.sleep(5)
        get_followers(handle, output_file_or_folder)

    return error_count


robjects.r['load'](r'~/Downloads/refdataCA.rdata')
actors = robjects.r['refdataCA'][4]

for actor in actors[actors.index('marstu67') + 1:]:  # colnames columns
    # Scrape all followers
    get_followers(actor, 'actor_followers/' + actor + '.txt')
