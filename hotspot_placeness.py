from flask_restful import Resource, Api, reqparse
from flask import request
import time

import category_classifier
from unicodedata import category
import visitor_logger

# Lee Wonjae
class HotspotPlaceness(Resource):
    def get(self):
        # Parse GET parameters
        parser = reqparse.RequestParser()
        parser.add_argument('hotspot_id', type=str)
        args = parser.parse_args(strict=True)

        # Logger
        client_ip = request.environ['REMOTE_ADDR']
        input_params = '/hotspot_placeness_extraction.json?hotspot_id={}'.format(args['hotspot_id'])
        visitor_logger.post_visit_data('api', client_ip, int(time.time()), input_params, 'get')

        # Internal function for the API request
        value = category_classifier.hotspot_placeness_extraction(args['hotspot_id'])
        return value



class FeatureExtraction(Resource):
    def post(self):
        # Parse GET parameters
        parser = reqparse.RequestParser()
        parser.add_argument('caption', type=str)
        parser.add_argument('timestamp', type=str)
        #1433435470
        args = parser.parse_args(strict=True)

        # Internal function for the API request

        if args['timestamp'] == None:
            args['timestamp']= int(time.time())

        # Logger
        client_ip = request.environ['REMOTE_ADDR']
        input_params = '/feature_extraction.json?caption={}&timestamp={}'.format(args['caption'], args['timestamp'])
        visitor_logger.post_visit_data('api', client_ip, int(time.time()), input_params, 'get')

        value = category_classifier.feature_extraction(args['caption'], args['timestamp'])
        value['caption'] = args['caption']
        value['timestamp'] = int(args['timestamp'])
        return value

# Lee Wonjae
class UserFeedback(Resource):
    def get(self):
        # Parse GET parameters
        parser = reqparse.RequestParser()
        parser.add_argument('hotspot_id', type=str)
        parser.add_argument('placeness', type=str)
        parser.add_argument('feedback_score', type=str)

        args = parser.parse_args(strict=True)

        # Logger
        client_ip = request.environ['REMOTE_ADDR']
        input_params = '/user_feedback.json?hotspot_id={}&placeness={}&feedback_score={}'.format(args['hotspot_id'], args['placeness'], args['feedback_score'])
        visitor_logger.post_visit_data('api', client_ip, int(time.time()), input_params, 'get')

        value = category_classifier.user_feedback(args)

        return value
