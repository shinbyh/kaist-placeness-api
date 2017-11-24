import json
import datetime
#from sets import Set


categories = {'Work': ['Business', 'Education', 'LegalAndFinance'],
    'Living': ['Relaxation', 'Religion', 'Chores', 'FoodAndDining', 'Childcare',
        'HealthAndMedical'],
    'Leisure': ['FashionAndBeauty', 'OutdoorAndActive', 'Traveling', 'Socializing',
        'Entertainment', 'ArtAndCulture']}
placeness = {}
def addToJSON(self, place, category, post_id, activities, post_time, post_age, post_gender):
    for activity in activities:
        try:
            key = None
            if category:
                for cat in categories:
                    pair = [act for act in categories[cat] if activity in act.lower()]
                    if len(pair) > 0:
                        pair = [k for k in categories if pair[0] in categories[k]]
                        key = pair[0]
            else:
                pair = [k for k in placeness[place].iteritems() if activity in k.lower()]
                key = pair[0][0]

            placeness[place][key][post_id] = {}
            placeness[place][key][post_id]['date'] = post_time.strftime('%Y-%m-%d')
            placeness[place][key][post_id]['time'] = post_time.strftime('%H:%M')
            placeness[place][key][post_id]['age'] = post_age
            placeness[place][key][post_id]['gender'] = post_gender
            placeness[place][key][post_id]['activities'] = activities
        except:
            pass

def analysis(self, category, area, start, end, age, gender, limit):
    if area == None:
        placeness['coex'] = {}
        placeness['ipark'] = {}
    else:
        placeness[area] = {}
    for place in placeness:
        if category:
            for cat in categories:
                placeness[place][cat] = {}
        else:
            for cat in categories:
                for act in categories[cat]:
                        placeness[place][act] = {}

    for place in placeness:
        # open file with json objects of posts
        with open("placenessdb-experiment-{0}-export.json".format(place)) as data_file:
            post_data = json.load(data_file)
            print(place)

        count = 0
        no_gen = 0
        for post_id in post_data:
            if count >= limit:
                print(count)
                return placeness

            post = post_data[post_id]
            post_time = datetime.datetime.fromtimestamp(int(post['date']))
            img_activities = set([])
            txt_activities = set([])
            try:
                post_age = int(post['profile_image_analysis']['faces'][0]['age'])
                post_gender = post['profile_image_analysis']['faces'][0]['gender']
            except KeyError as e:
                post_age = -1
                post_gender = 'None'
            try:
                img_activities = set(post['img_keywords'])
            except:
                pass
            try:
                txt_activities = set(post['text_keywords'])
            except:
                pass

            activities = img_activities.union(txt_activities)
            activities = list(activities)
            activitiesCount = 0
            for activity in activities:
                act_loc = activities.index(activity)
                activities[act_loc] = activity.replace('&', 'and')
                activitiesCount += 1

            conditions = False

            if ((age == None or (age <= post_age < (age + 10)))
                and (gender == None or post_gender.lower() == gender)
                and (start < post_time.date() < end)
                and activitiesCount):
                conditions = True
                if post_gender == 'None':
                    no_gen +=1

            if conditions:
                addToJSON(self, place, category, post_id, activities, post_time, post_age, post_gender)
                count +=1
        print (count)
        print (no_gen)
    return placeness
