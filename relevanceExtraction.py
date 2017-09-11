import sys
import os
from flask_restful import Resource, reqparse
from flask_api import status
sys.path.insert(0, os.getcwd()+'/relevanceLib')
import json
from relevance import relevance
import glob as glob

# Logger-related modules
from flask import request
import time
import visitor_logger

# reload(sys)
# sys.setdefaultencoding('utf8')

metadata_json=open('data/venue_info.json', encoding='utf-8').read()
venue_metadata=json.loads(metadata_json)

method='pagerank'
alpha=0.1

graph='gexf/tf-idf_user_placeness_venue.gexf'

rec=relevance()
rec.load_network(graph)
rec.load_placeness_keywords()

# Q Group
#

class RelevanceExtraction(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('time_kwd', type=str)
        parser.add_argument('with_kwd', type=str)
        parser.add_argument('occasion_kwd', type=str)
        parser.add_argument('mood_kwd', type=str)
        parser.add_argument('weather_kwd', type=str)
        parser.add_argument('weight_date', type=str)
        parser.add_argument('weight_with', type=str)
        parser.add_argument('weight_occasion', type=str)
        parser.add_argument('weight_mood', type=str)
        parser.add_argument('weight_weather', type=str)
        parser.add_argument('weight_query', type=str)
        parser.add_argument('topk', type=int)
        args = parser.parse_args(strict=True)

        # Logger
        client_ip = request.environ['REMOTE_ADDR']
        input_params = '/relevance_extraction.json?time_kwd={}&with_kwd={}&occasion_kwd={}&mood_kwd={}&weather_kwd={}&weight_date={}&weight_with={}&weight_occasion={}&weight_weather={}&weight_query={}&topk={}'.format(
                            args['time_kwd'],
                            args['with_kwd'],
                            args['occasion_kwd'],
                            args['mood_kwd'],
                            args['weather_kwd'],
                            args['weight_date'],
                            args['weight_with'],
                            args['weight_occasion'],
                            args['weight_mood'],
                            args['weight_weather'],
                            args['weight_query'],
                            args['topk'])
        visitor_logger.post_visit_data('api', client_ip, int(time.time()), input_params, 'get')

        occasion_kwds=[]
        if args['occasion_kwd'] is not None:
            occasion_kwds = [args['occasion_kwd']]
        mood_kwds=[]
        if args['mood_kwd'] is not None:
            occasion_kwds = [args['mood_kwd']]
        with_kwds=[]
        if args['with_kwd'] is not None:
            occasion_kwds = [args['with_kwd']]
        time_kwds=[]
        if args['time_kwd'] is not None:
            occasion_kwds = [args['time_kwd']]
        weather_kwds=[]
        if args['weather_kwd'] is not None:
            occasion_kwds = [args['weather_kwd']]
        user_kwds=[]
        topk = 10
        if args['topk'] is not None:
            topk = int(args['topk'])

        print(occasion_kwds)
        print(mood_kwds)
        print(with_kwds)
        print(time_kwds)
        print(weather_kwds)

        result=rec.query(time_kwd=time_kwds,with_kwd=with_kwds, occasion_kwd=occasion_kwds, mood_kwd=mood_kwds, weather_kwd=weather_kwds, user_kwd=user_kwds, topk=topk, weight_query=alpha)

        result_obj = {}

        for res in result[0]:
            result_obj[venue_metadata[res[0]]['name']] = res[1]

        return {'venues':result_obj}
