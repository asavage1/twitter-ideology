import twint
import rpy2.robjects as robjects


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


robjects.r['load'](r'~/Downloads/refdataCA.rdata')

for actor in robjects.r['refdataCA'][4]:  # colnames columns
    # Scrape all followers
    get_followers(actor, 'actor_followers/' + actor + '.txt')
