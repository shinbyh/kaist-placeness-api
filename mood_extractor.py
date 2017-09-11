#!/usr/bin/env python
# -*- coding: utf-8 -*-
import district_classifier
import hotspot_mood
import json
import sys

mood_summary_by_hotspot = {}
mood_summary_by_moodword = {}
mood_kor_eng = {
    u"친절한":"Friendly",
    u"편안한":"Relaxing",
    u"로맨틱한":"Romantic",
    u"세련된":"Modern",
    u"전통적":"Traditional",
    u"북적이는":"Loud",
    u"답답한":"Cramp"
}

def load_mood_summary_by_hotspot(district):
    try:
        # Debug
        print('[Mood_extractor] loading mood summary by hotspot:', district)
        data = open('data/hotspot_summary_mood_{}3.json'.format(district)).read()
        mood_summary_by_hotspot[district] = json.loads(data)
    except:
        # Error: District is none or unknown.
        print('[Mood_extractor] Error: district [{}] is invalid.'.format(district))

def load_mood_summary_by_moodword(district):
    try:
        # Debug
        print('[Mood_extractor] loading mood summary by moodword:', district)
        data = open('data/mood_summary_hotspot_{}.json'.format(district)).read()
        mood_summary_by_moodword[district] = json.loads(data)
    except:
        # Error: District is none or unknown.
        print('[Mood_extractor] Error: district [{}] is invalid.'.format(district))

load_mood_summary_by_hotspot('coex')
load_mood_summary_by_hotspot('iparkmall')
load_mood_summary_by_moodword('coex')
load_mood_summary_by_moodword('iparkmall')

def convert_mood_eng(mood_kor):
    if(mood_kor in mood_kor_eng.keys()):
        return mood_kor_eng[mood_kor]
    else:
        return None

def get_gmap_mood_index(mood_str):
    default_index = 7
    mood_index = default_index

    if(mood_str == 'none'):
        mood_index = default_index
    elif(mood_str == 'Loud'):
        mood_index = 5
    elif(mood_str == 'Relaxing'):
        mood_index = 1
    elif(mood_str == 'Modern'):
        mood_index = 3
    elif(mood_str == 'Traditional'):
        mood_index = 4
    elif(mood_str == 'Romantic'):
        mood_index = 2
    elif(mood_str == 'Friendly'):
        mood_index = 0
    elif(mood_str == 'Cramp'):
        mood_index = 6

    return mood_index

def get_hotspot_moods(district, hotspot_id):
    try:
        # For safety, hotspot_id must be a string.
        hotspot_id = '{}'.format(hotspot_id)

        hotspot_mood = mood_summary_by_hotspot[district][hotspot_id]
        if('MoodList' in hotspot_mood.keys()):
            return hotspot_mood['MoodList']
        else:
            return None

    except:
        # Error: district or hotspot_id null or unknown.
        return None

def get_locationids_of_mood(district, mood):
    try:
        return mood_summary_by_moodword[district][mood]
    except:
        print('[Mood_extractor] Error: failed to get locationids by moodword:', district)
        return None


def write_hotspot_summary_mood_data(district):
    hotspot_list = district_classifier.getHotspots(district)
    result = {}

    for hotspot in hotspot_list:
        print('Analyzing', hotspot['id'])
        mood_dist = hotspot_mood.getHotspotMoodDistribution(0.2, 'binary', hotspot['id'])
        found_moods = hotspot_mood.getCredibleMoodsOfHotspot(hotspot['id'], 0.0)

        if(mood_dist is not None):
            mood_dist['MoodList'] = found_moods
            result[hotspot['id']] = mood_dist

    print('Writing results to file...')
    with open('data/hotspot_summary_mood_{}3.json'.format(district), 'w') as fp:
        json.dump(result, fp)

def write_mood_summary_hotspot_data(district):
    hotspot_list = district_classifier.getHotspots(district)
    result = {}
    result['Loud'] = []
    result['Relaxing'] = []
    result['Modern'] = []
    result['Traditional'] = []
    result['Romantic'] = []
    result['Friendly'] = []
    result['Cramp'] = []

    for hotspot in hotspot_list:
        print('Checking', hotspot['id'])
        #found_moods = hotspot_mood.getCredibleMoodsOfHotspot(hotspot['id'], 0.0)

        if(hotspot['id'] in mood_summary_by_hotspot[district].keys()):
            print(' - Analyzing', hotspot['id'])
            found_mood_hotspot = mood_summary_by_hotspot[district][hotspot['id']]
            if(found_mood_hotspot is not None):
                found_moods = found_mood_hotspot['MoodList']
                if(found_moods is not None):
                    for mood_word in found_moods:
                        result[mood_word].append(hotspot['id'])

    print('Writing results to file...')
    with open('data/mood_summary_hotspot_{}.json'.format(district), 'w') as fp:
        json.dump(result, fp)

if __name__ == "__main__":
    # For all locationids in a district,
    # extract mood list and append it to the dict with hotspot id.
    # Save the dict to a json file.
    #if(len(sys.argv) >= 2):
    #    district = sys.argv[1]
    #else:
    #    district = 'coex'
    #write_hotspot_summary_mood_data(district)

    write_mood_summary_hotspot_data('iparkmall')
    write_mood_summary_hotspot_data('coex')
