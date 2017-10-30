import sys
import os
from flask_restful import Resource, reqparse, output_json
from flask_api import status
sys.path.insert(0, os.getcwd()+'/relevanceLib')
import json
from flask import Response
from functools import wraps
from relevance import relevance
import glob as glob
from collections import OrderedDict
import operator
import numpy as np


# Logger-related modules
from flask import request
import time
import visitor_logger

# reload(sys)
# sys.setdefaultencoding('utf8')

metadata_json=open('data/venue_info.json', encoding='utf-8').read()
venue_metadata=json.loads(metadata_json)

# Q Group
#
class RelevanceExtraction(Resource):
    def get(self):
        method='pagerank'
        graph='gexf/tf-idf_placeness_venue_with_cutoff.gexf'

        parser = reqparse.RequestParser()
        parser.add_argument('method', type=str)
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
        input_params = '/relevance_extraction.json?method={}&time_kwd={}&with_kwd={}&occasion_kwd={}&mood_kwd={}&weather_kwd={}&weight_date={}&weight_with={}&weight_occasion={}&weight_weather={}&weight_query={}&topk={}'.format(
                            args['method'],
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
        if args['method'] is not None:
            method = args['method']

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
        weight_mood = 0.01
        if args['weight_mood'] is not None:
            weight_mood = float(args['weight_mood'])
        weight_time = 0.1
        if args['weight_date'] is not None:
            weight_time = float(args['weight_date'])
        weight_occasion = 1.0
        if args['weight_occasion'] is not None:
            weight_occasion = float(args['weight_occasion'])
        weight_with = 1.0
        if args['weight_with'] is not None:
            weight_with = float(args['weight_with'])
        weight_weather = 1.0
        if args['weight_weather'] is not None:
            weight_weather = float(args['weight_weather'])
        alpha = 0.1
        if args['weight_query'] is not None:
            alpha = float(args['weight_query'])
        user_kwds=[]

        q = time_kwds + with_kwds + occasion_kwds + mood_kwds + weather_kwds + user_kwds
        topk = 10
        if args['topk'] is not None:
            topk = int(args['topk'])

        if method == "community":
            graphs = glob.glob('gexf/subgraphs/*.gexf')
            recs=[]
            for g in graphs:
                recs.append(relevance())
                recs[-1].load_network(g)
                recs[-1].load_placeness_keywords()
            print("Assigning random walkers onto the network..")
            print("Done")
            print("Estimating the relevance of venues given the query using the subgraphs…")

            merged_result=dict()
            dummy_times=[]
            running_times=[]
            for rec in recs:
                result=rec.query(time_kwd=time_kwds,with_kwd=with_kwds, occasion_kwd=occasion_kwds, mood_kwd=mood_kwds, weather_kwd=weather_kwds, user_kwd=user_kwds, topk=topk, weight_query=alpha, weight_time=weight_time, weight_mood=weight_mood, weight_occasion=weight_occasion, weight_with=weight_with
                                 ,weight_weather=weight_weather)

                dummy_times.append(result[1])
                num_nodes=rec.graph.number_of_nodes()
                num_query_nodes=0
                if type(q) is list:
                    for q_i in q:
                        num_query_nodes += len(rec.get_placeness(q_i))
                else:
                    num_query_nodes = len(rec.get_placeness(q))

                for res in result[0]:
                    merged_result[venue_metadata[res[0]]['name']]=res[1]*num_nodes*num_query_nodes
            running_times.append(np.sum(dummy_times))

            response = {'venues':OrderedDict(sorted(merged_result.items(), key=operator.itemgetter(1), reverse=True)[:topk])}
            print("Results:")
            print(response)
            return response

        else :
            rec=relevance()
            rec.load_network(graph)
            rec.load_placeness_keywords()
            print("Assigning random walkers onto the network..")
            print("Done")
            print("Estimating the relevance of venues given the query…")

            result=rec.query(time_kwd=time_kwds,with_kwd=with_kwds, occasion_kwd=occasion_kwds, mood_kwd=mood_kwds, weather_kwd=weather_kwds, user_kwd=user_kwds, topk=topk, weight_query=alpha, weight_time=weight_time, weight_mood=weight_mood, weight_occasion=weight_occasion, weight_with=weight_with
                             ,weight_weather=weight_weather)

            result_obj = {}

            for res in result[0]:
                result_obj[venue_metadata[res[0]]['name']] = res[1]

            response = {'venues':OrderedDict(sorted(result_obj.items(), key=operator.itemgetter(1), reverse=True))}

            print("Results:")
            print(response)

            return response
