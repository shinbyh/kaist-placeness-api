#!/usr/bin/env python
# -*- coding: utf-8 -*-

import category_classifier
import district_classifier
import hotspot_mood
import location_metadata
import mood_extractor

import json
import sys

maen = {
    'morning':0,
    'afternoon':0,
    'evening':0,
    'night':0
}
weekday = {
    'weekday':0,
    'weekend':0
}
user = {
    u'직장인':0,
    u'with가족':0,
    u'with친구':0,
    u'with유아':0,
    u'with어른':0
}
mood = {
    u'전통적':0,
    u'세련된':0,
    u'답답한':0,
    u'친절한':0,
    u'편안한':0,
    u'로맨틱한':0,
    u'북적이는':0
}
season = {
    'spring':0,
    'summer':0,
    'autumn':0,
    'winter':0
}
activityDict = {
    u'카페':0,
    u'운동':0,
    u'회식':0,
    u'의료':0,
    u'집안일':0,
    u'휴식':0,
    u'문화생활':0,
    u'나들이':0,
    u'맛집탐방':0,
    u'키덜트':0,
    u'데이트':0,
    u'공부':0,
    u'디저트':0,
    u'영화':0,
    u'뷰티':0,
    u'끼니':0,
    u'음주':0,
    u'경조사':0,
    u'쇼핑':0,
    u'여행':0
}

def get_default_summary_data_activity():
    summary_data = {}

    for activity_item in activityDict:
        summary_data[activity_item] = {
            'mood':mood.copy(),
            'maen':maen.copy(),
            'weekday':weekday.copy(),
            'user':user.copy(),
            'season':season.copy(),
            'count':0
        }
    return summary_data


def get_default_summary_data_mood():
    summary_data = {}
    for mood_item in mood:
        summary_data[mood_item] = {
            'mood':mood_item,
            'maen':maen.copy(),
            'weekday':weekday.copy(),
            'user':user.copy(),
            'season':season.copy(),
            'activity':activityDict.copy(),
            'count':0
        }
    return summary_data
    #return summarize_data_mood

def summarize_hotspot_activity(hotspot_id):
    summary_data = get_default_summary_data_activity()
    hotspot_data = category_classifier.hotspot_placeness_extraction(hotspot_id)

    for item in hotspot_data['placeness']:
        if('Occasion' in item.keys()):
            act = summary_data[item['Occasion']]
            count = item['count']
            act['count'] += count
            act['maen'][item['maen']] += count
            act['weekday'][item['isWeekend']] += count
            act['season'][item['Season']] += count
            if('User' in item.keys()):
                if(item['User'] not in act['user'].keys()):
                    act['user'][item['User']] = count
                else:
                    act['user'][item['User']] += count
    return summary_data


def summarize_hotspot_mood(hotspot_id):
    summary_data = get_default_summary_data_mood()
    hotspot_data = category_classifier.hotspot_placeness_extraction(hotspot_id)

    for item in hotspot_data['placeness']:
        #print(item)
        if('Mood' in item.keys()):
            mood = summary_data[item['Mood']]
            count = item['count']
            mood['count'] += count
            mood['maen'][item['maen']] += count
            mood['weekday'][item['isWeekend']] += count
            mood['season'][item['Season']] += count

            if('User' in item.keys()):
                if(item['User'] not in mood['user'].keys()):
                    mood['user'][item['User']] = count
                else:
                    mood['user'][item['User']] += count
            if('Occasion' in item.keys()):
                mood['activity'][item['Occasion']] += count

    return summary_data

def get_hotspot_array_by_activity(district, activity):
    data = open('data/hotspot_summary_activity_{}2.json'.format(district)).read()
    hotspot_summary = json.loads(data)
    result_arr = []
    for hotspot_id in hotspot_summary.keys():
        temp = {}
        hotspot = hotspot_summary[hotspot_id]
        if(hotspot[activity]['count'] == 0):
            continue

        # Filter out some hotspots for demo
        if(hotspot_id == '138200'):
            if(activity != u'문화생활'):
                continue
        if(hotspot_id == '214348478'):
            if(activity != u'문화생활' or activity != u'영화' or activity != u'휴식'):
                continue
        if(hotspot_id == '1450103671873685' or hotspot_id == '414040022'):
            if(activity != u'쇼핑'):
                continue
        if(hotspot_id == '284660200' and activity != u'뷰티'):
            continue

        # Analyze mood of each hotspot.
        # Commented because of too long time (170907)
        #mood_list = hotspot_mood.getCredibleMoodsOfHotspot(hotspot_id, 0.5)
        #if(mood_list is not None):
        #    temp['mood'] = mood_list[0]
        #else:
        #    temp['mood'] = 'none'

        temp['hotspot_id'] = hotspot_id
        temp['count'] = hotspot[activity]['count']
        #temp['mood'] = hotspot[activity]['mood']
        temp['weekday'] = hotspot[activity]['weekday']
        temp['user'] = hotspot[activity]['user']
        result_arr.append(temp)
    sorted_result = sorted(result_arr, key=lambda k: k['count'], reverse=True)
    return sorted_result

def get_activity_count_of_hotspot_summary(hotspot_summary_by_id, hotstpot_id, mood, activity):
    if(mood in hotspot_summary_by_id.keys()):
        if('activity' in hotspot_summary_by_id[mood].keys()):
            return hotspot_summary_by_id[mood]['activity'][activity]
        else:
            return 0
    else:
        print('[Hotspot analyzer] no such mood [{}] for the hotspot: {}'.format(mood, hotspot_id))
        return 0

def get_hotspot_array_by_mood(district, mood, activity):
    mood_eng = mood_extractor.convert_mood_eng(mood)
    hotspots = mood_extractor.get_locationids_of_mood(district, mood_eng)
    if(hotspots is None):
        print('[Hotspot analyzer] Error: failed to load hotspots for the mood:', mood_eng)
        return []

    data = open('data/hotspot_summary_mood_{}2.json'.format(district)).read()
    all_hotspots_summary = json.loads(data)
    result_arr = []

    # Make dict of hotspots matching the mood.
    hotspot_summary = {}
    for hotspot_id in hotspots:
        hotspot_summary[hotspot_id] = all_hotspots_summary[hotspot_id]

    # For each hotspot for the mood,
    # make a count number based on activity frequency.
    for hotspot_id in hotspot_summary.keys():
        temp = {}
        hotspot = hotspot_summary[hotspot_id]

        # Filter out some hotspots for demo.
        if(hotspot_id == '138200' or
            hotspot_id == '214348478' or
            hotspot_id == '1450103671873685' or
            hotspot_id == '414040022' or
            hotspot_id == '314286935300506'):
            continue

        temp['hotspot_id'] = hotspot_id
        #temp['count'] = hotspot[mood]['count']
        temp['count'] = get_activity_count_of_hotspot_summary(hotspot, hotspot_id, mood, activity)
        temp['weekday'] = hotspot[mood]['weekday']
        temp['activity'] = hotspot[mood]['activity']
        temp['user'] = hotspot[mood]['user']
        result_arr.append(temp)
    sorted_result = sorted(result_arr, key=lambda k: k['count'], reverse=True)
    return sorted_result




def main(argv):
    district = argv[1]
    #activity = argv[2]
    #print('Target District:', district, ', activity:', activity)

#    result = get_hotspot_array_by_activity(district, activity)
#    print(result)

    final_result = {}
    hotspot_list = district_classifier.getHotspots(district)

    for hotspot in hotspot_list:
        print('analyzing', hotspot['id'])
        result_hotspot = summarize_hotspot_mood(hotspot['id'])
        #result_hotspot = summarize_hotspot_activity(hotspot['id'])
        final_result[hotspot['id']] = result_hotspot

    with open('data/hotspot_summary_mood_{}.json'.format(district), 'w') as fp:
        json.dump(final_result, fp)

if __name__ == "__main__":
    main(sys.argv)
