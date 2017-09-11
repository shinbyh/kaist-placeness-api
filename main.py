from flask import Flask, render_template, request
from flask_restful import Resource, Api, reqparse
from flask_api import status
import sys, time
import json
import ast

# CDSNLab
from district_placeness import DistrictPlaceness
from district_placeness import DistrictRetrieval
from district_placeness import DistrictAddition
from activities_trend import VisitorActivityData

# CDSNLab, for Web Applications
import category_classifier
import district_classifier
import location_metadata
import hotspot_analyzer
import random
import instagram_crawler
import visitor_logger
import hotspot_mood
import mood_extractor

# Lee Wonjae
from hotspot_placeness import HotspotPlaceness
from hotspot_placeness import FeatureExtraction
from hotspot_placeness import UserFeedback

# Cha Meeyoung
from hotspot_mood import MoodExtraction
from hotspot_mood import HotspotMoodDistribution

# TheQ
from relevanceExtraction import RelevanceExtraction


app = Flask(__name__)
app.config['SECRET_KEY'] = 'cdsnlab'
api = Api(app)

# Web pages
@app.route('/', methods=['GET'])
def index():
    client_ip = request.environ['REMOTE_ADDR']
    visitor_logger.post_visit_data('web', client_ip, int(time.time()), '/', 'get')
    return render_template("index.html")

@app.route('/sample/', methods=['GET'])
def sample():
    client_ip = request.environ['REMOTE_ADDR']
    visitor_logger.post_visit_data('web', client_ip, int(time.time()), '/sample', 'get')
    return render_template("sample.html")

@app.route('/hotspot', methods=['GET'])
def sampleHotspot():
    hotspot_id = request.args.get('hotspot_id')

    client_ip = request.environ['REMOTE_ADDR']
    input_params = '/hotspot?hotspot_id={}'.format(hotspot_id)
    visitor_logger.post_visit_data('web', client_ip, int(time.time()), input_params, 'get')

    hotspot_name = location_metadata.getLocationName(hotspot_id)
    value = category_classifier.hotspot_placeness_extraction(hotspot_id)
    placeness_list = value['placeness']
    placeness_list_sorted = sorted(placeness_list, key=lambda k: k['count'], reverse=True)
    value_sorted = {}
    value_sorted['hotspot_id'] = hotspot_id
    value_sorted['placeness'] = placeness_list_sorted

    return render_template("hotspot.html",
                            hotspot_id=hotspot_id,
                            hotspot_name=hotspot_name,
                            value=value_sorted)

@app.route('/placeness', methods=['GET'])
def sampleDistrict():
    district = request.args.get('district')
    activity = request.args.get('activity')
    age = request.args.get('age')

    client_ip = request.environ['REMOTE_ADDR']
    input_params = '/placeness?district={}&activity={}&age={}'.format(district, activity, age)
    visitor_logger.post_visit_data('web', client_ip, int(time.time()), input_params, 'get')

    return render_template("sample.html", district=district, activity=activity, age=age)

@app.route('/hotspot-placeness', methods=['GET'])
def sampleHotspotPlaceness():
    sns_url = request.args.get('sns_url')

    client_ip = request.environ['REMOTE_ADDR']
    input_params = '/hotspot-placeness?sns_url={}'.format(sns_url)
    visitor_logger.post_visit_data('web', client_ip, int(time.time()), input_params, 'get')

    proc_data = {
        'season':'',
        'mood':'',
        'activity':'',
        'isWeekend':'',
        'maen':''
    }

    if(sns_url == 'https://www.instagram.com/p/BTb50_Slnzp/'):
        imgfile = 'static/iiii2.png'
        proc_data['season'] = 'Spring'
        proc_data['mood'] = '북적이는'
        proc_data['activity'] = '끼니, 음주'
        proc_data['isWeekend'] = 'weekend'
        proc_data['maen'] = 'evening'
    elif(sns_url == 'https://www.instagram.com/p/BXsLO_zhM0z/'):
        imgfile = 'static/iiii.png'
        proc_data['season'] = 'Spring'
        proc_data['mood'] = '전통적, 친절한'
        proc_data['activity'] = '끼니'
        proc_data['isWeekend'] = 'weekend'
        proc_data['maen'] = 'evening'
        sns_timestamp = 1502505343
    else:
        # https://www.instagram.com/p/BFlOW81Dwwy/
        proc_data['season'] = 'Spring'
        proc_data['mood'] = '세련된'
        proc_data['activity'] = '문화생활'
        proc_data['isWeekend'] = 'weekday'
        proc_data['maen'] = 'afternoon'
        sns_timestamp = 1495161343
        imgfile = 'static/iiii3.png'

    tt = instagram_crawler.parsePost(sns_url)
    sns_text = tt['caption']
    sns_timestamp = tt['timestamp']
    feature_ext_result = category_classifier.feature_extraction(sns_text, sns_timestamp)

    return render_template("hotspot_placeness.html",
                            sns_url=sns_url,
                            feature_ext_result=feature_ext_result,
                            imgfile=imgfile,
                            proc_data=proc_data)

@app.route('/gmap', methods=['POST','GET'])
def gmap():
    #print('  POST data:', request.form['locations'])
    locations = ast.literal_eval(request.form['locations'])
    district = request.form['district']

    client_ip = request.environ['REMOTE_ADDR']
    input_params = '/gmap?district={}'.format(district)
    visitor_logger.post_visit_data('web', client_ip, int(time.time()), input_params, 'post')

    center = district_classifier.getCenter(district)
    #print(district, 'center:', center)

    return render_template("gmap2.html",
                            locations=json.dumps(locations),
                            center_lat=center[0],
                            center_lon=center[1])

@app.route('/district-placeness', methods=['GET'])
def sampleDistrictPlaceness():
    district = request.args.get('district')
    activity = request.args.get('activity')
    maen = request.args.get('maen')
    mood = request.args.get('mood')

    client_ip = request.environ['REMOTE_ADDR']
    input_params = '/district-placeness?district={}&activity={}&maen={}&mood={}'.format(district, activity, maen, mood)
    visitor_logger.post_visit_data('web', client_ip, int(time.time()), input_params, 'get')

    search_result = []

    if(mood == 'none'):
        # Mood is not specified. Filter hotspots first by activity.
        temp_result = hotspot_analyzer.get_hotspot_array_by_activity(district, activity)
        idx = 0
        for temp in temp_result:
            idx += 1
            temp['rank'] = idx
            temp['hotspot_name'] = location_metadata.getLocationName(temp['hotspot_id'])
            gps = location_metadata.getGPS(temp['hotspot_id'])
            temp['gps_lat'] = gps[0]
            temp['gps_lon'] = gps[1]

            #hotspot_moods = hotspot_mood.getCredibleMoodsOfHotspot(temp['hotspot_id'], 0.3)
            hotspot_moods = mood_extractor.get_hotspot_moods(district, temp['hotspot_id'])
            if(hotspot_moods is None or len(hotspot_moods) == 0):
                temp['mood'] = 'none'
            else:
                temp['mood'] = hotspot_moods[0]

            # Get mood index for showing a Google Map icon.
            temp['mood_index'] = mood_extractor.get_gmap_mood_index(temp['mood'])

            # Predefine some hotspots for demo
            if(temp['hotspot_id'] == '149949'):
                temp['mood_index'] = 4
            elif(temp['hotspot_id'] == '319602204' or
                temp['hotspot_id'] == '100554430385266'):
                temp['mood_index'] = 3
            elif(temp['hotspot_id'] == '1345605272126786'):
                temp['mood_index'] = 1
            elif(temp['hotspot_id'] == '918860378233238' or
                temp['hotspot_id'] == '968345939922770'):
                temp['mood_index'] = 0
            elif(temp['hotspot_id'] == '447938232'):
                temp['mood_index'] = 6
            elif(temp['hotspot_id'] == '1023159399'):
                temp['mood_index'] = 2

            search_result.append(temp)
            if(idx == 15):
                break

    else:
        # Mood is specified. Filter hotspots by mood first.
        mood_eng = mood_extractor.convert_mood_eng(mood)
        if(mood_eng is not None):
            temp_result = hotspot_analyzer.get_hotspot_array_by_mood(district, mood, activity)
            idx = 0
            for temp in temp_result:
                idx += 1
                temp['rank'] = idx
                temp['hotspot_name'] = location_metadata.getLocationName(temp['hotspot_id'])
                gps = location_metadata.getGPS(temp['hotspot_id'])
                temp['gps_lat'] = gps[0]
                temp['gps_lon'] = gps[1]
                temp['mood_index'] = mood_extractor.get_gmap_mood_index(mood_eng)
                search_result.append(temp)
                if(idx == 10):
                    break

    result_hotspots = []
    for item in search_result:
        spot_to_add = []
        spot_to_add.append(item['hotspot_name'])
        spot_to_add.append(float(item['gps_lat']))
        spot_to_add.append(float(item['gps_lon']))
        spot_to_add.append(item['mood_index'])
        spot_to_add.append(item['count'])
        result_hotspots.append(spot_to_add)

    search_result = sorted(search_result, key=lambda k: k['rank'])
    return render_template("district_placeness.html",
                            district=district,
                            activity=activity,
                            maen=maen,
                            mood=mood,
                            search_result=search_result,
                            result_hotspots=result_hotspots)


@app.route('/district-hotspots', methods=['GET'])
def getHotspotsOfDistrict():
    district = request.args.get('district')

    client_ip = request.environ['REMOTE_ADDR']
    input_params = '/district-hotspots?district={}'.format(district)
    visitor_logger.post_visit_data('web', client_ip, int(time.time()), input_params, 'get')

    hotspots = district_classifier.getHotspots(district)
    return render_template("sample.html",
                            district=district,
                            hotspots=hotspots)




# List of REST APIs
api.add_resource(DistrictPlaceness, '/district_placeness_extraction.json')
api.add_resource(DistrictRetrieval, '/district.json')
api.add_resource(DistrictAddition, '/district.json/new')
api.add_resource(HotspotPlaceness, '/hotspot_placeness_extraction.json')
api.add_resource(FeatureExtraction, '/feature_extraction.json')
api.add_resource(UserFeedback, '/user_feedback.json')
api.add_resource(RelevanceExtraction, '/relevance_extraction.json')
api.add_resource(MoodExtraction, '/mood')
api.add_resource(HotspotMoodDistribution, '/hotspot_mood')
api.add_resource(VisitorActivityData, '/activity_time_trend.json/activity')

def show_usage():
    print('Usage:\n python main.py [HOST_IP] [PORT]')
    print('HOST_IP and PORT not specified, loading default.')

if __name__ == '__main__':
    if(len(sys.argv) == 1):
        show_usage()
        app.run(debug=True, host='0.0.0.0', port=8080)
    else:
        app.run(debug=True, host=sys.argv[1], port=int(sys.argv[2]))
