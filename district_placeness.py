from flask_restful import Resource, reqparse
from flask_api import status

import district_classifier

# Logger-related modules
from flask import request
import time
import visitor_logger

# CDSNLab
# Get the name of a district for a GPS coordinate
class DistrictRetrieval(Resource):
    def get(self):
        # Parse GET parameters
        parser = reqparse.RequestParser()
        parser.add_argument('lat', type=str)
        parser.add_argument('lon', type=str)
        args = parser.parse_args(strict=True)
        lat = float(args['lat'])
        lon = float(args['lon'])

        # Logger
        client_ip = request.environ['REMOTE_ADDR']
        input_params = '/district.json?lat={}&lon={}'.format(lat, lon)
        visitor_logger.post_visit_data('api', client_ip, int(time.time()), input_params, 'get')

        # Internal function for the API request
        districtName = district_classifier.getDistrict(lat, lon)
        return {'name':districtName}, status.HTTP_200_OK

class DistrictAddition(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('nw_lat', type=float)
        parser.add_argument('nw_lon', type=float)
        parser.add_argument('se_lat', type=float)
        parser.add_argument('se_lon', type=float)
        args = parser.parse_args(strict=True)

        if(args['name'] is not None):
            # addDistrictToDict(name, gps_nw, gps_se):
            gps_nw = ()
            gps_se = ()
            gps_nw['lat'] = args['nw_lat']
            gps_nw['lon'] = args['nw_lon']
            gps_se['lat'] = args['se_lat']
            gps_se['lon'] = args['se_lon']
            district_classifier.addDistrictToDict(args['name'], gps_nw, gps_se)

            # Logger
            client_ip = request.environ['REMOTE_ADDR']
            input_params = '/district.json/new?name={}&nw_lat={}&nw_lon={}&se_lat={}&se_lon={}'.format(
                                            args['name'],
                                            args['nw_lat'],
                                            args['nw_lon'],
                                            args['se_lat'],
                                            args['se_lon'],)
            visitor_logger.post_visit_data('api', client_ip, int(time.time()), input_params, 'post')

            return {'msg':'ok'}, status.HTTP_200_OK
        else:
            return {'msg':'place name not specified.'}, status.HTTP_400_BAD_REQUEST

# CDSNLab
# Classes for district placeness APIs
class DistrictPlaceness(Resource):
    def get(self):
        # Parse GET parameters
        parser = reqparse.RequestParser()
        parser.add_argument('lat', type=str)
        parser.add_argument('lon', type=str)
        parser.add_argument('name', type=str)
        parser.add_argument('count', type=str)
        args = parser.parse_args(strict=True)
        districtName = ''
        count = 3 # default count value

        # Logger
        client_ip = request.environ['REMOTE_ADDR']
        input_params = '/district_placeness_extraction.json?lat={}&lon={}&name={}&count={}'.format(
                            args['lat'],
                            args['lon'],
                            args['name'],
                            args['count'])
        visitor_logger.post_visit_data('api', client_ip, int(time.time()), input_params, 'get')


        # Internal function for the API request
        if(args['lat'] is not None and args['lon'] is not None):
            lat = float(args['lat'])
            lon = float(args['lon'])
            districtName = district_classifier.getDistrict(lat, lon)
        elif(args['name'] is not None):
            districtName = args['name']
        else:
            # error: place not specified
            return {'error':401, 'msg':'bad request (GPS or placename not specified)'}

        # parse count
        if(args['count'] is not None):
            count = int(args['count'])

        if(districtName is not ''):
            value = extract_placeness(districtName.lower(), count)
            if(value is not None):
                return {'name':value['name'], 'count':value['count']}, status.HTTP_200_OK
            else:
                return {'msg':'Placeness not found'}, status.HTTP_404_NOT_FOUND




def extract_placeness(place_name, count):
    # TODO: Implement
    value = {}
    value['name'] = place_name
    value['count'] = count
    return value
