import csv

rep = ['realDonaldTrump', 'mike_pence', 'SpeakerRyan', 'SenateMajLdr',
       'tedcruz', 'SenatorCollins', 'LindseyGrahamSC', 'SenJohnMcCain']
dem = ['BarackObama', 'JoeBiden', 'HillaryClinton', 'NancyPelosi',
       'SenSchumer', 'BernieSanders', 'Sen_JoeManchin', 'SenGillibrand']
rl_media = ['BillOReilly', 'seanhannity', 'IngrahamAngle', 'benshapiro', 'hughhewitt']
ll_media = ['maddow', 'billmaher', 'VanJones68', 'chrislhayes', 'Lawrence']
actor_handles = rep + dem + rl_media + ll_media

with open('aggregated_tweets2.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    headers = None
    with open('everyday_users.csv', 'w') as e:
        csv_writer_eu = csv.writer(e)
        with open('major_actors.csv', 'w') as m:
            csv_writer_ma = csv.writer(m)
            for row in csv_reader:
                if headers is None:
                    headers = row
                    csv_writer_eu.writerow(headers)
                    csv_writer_ma.writerow(headers)
                    continue
                if row[2] in actor_handles:
                    csv_writer_ma.writerow(row)
                else:
                    csv_writer_eu.writerow(row)
