from flask_restful import Resource, reqparse
from flask_api import status
from datetime import datetime, date
import get_trend

class VisitorActivityData(Resource):
    def get(self):
        parser = getArguments(self)
        args = parser.parse_args(strict=True)
        category = str(args['category'])
        time_range = str(args['time_range'])
        start, end = getTimeRange(self, time_range)
        visitor_age = visitor_gender = area = limit = None
        # category required, query allows case insensitive True, T or False, F
        if category.lower() in 'true':
            category = True
        elif category.lower() in 'false':
            category = False
        else:
                return {'error':401, 'msg':'bad request. category query takes case insensitive True, T, False, or F'}

        # age not required, defaults to all age ranges
        if args['visitor_age'] != None:
            visitor_age = int(args['visitor_age'][:-1])
            if visitor_age%10 != 0:
                return {'error':401, 'msg':'bad request. visitor_age takes query format such as: 10s (teens), 20s, ... Defaults to all age range)'}

        # gender not required, defaults to all genders
        if args['visitor_gender'] != None:
            visitor_gender = str(args['visitor_gender']).lower()
            if not (visitor_gender.lower() in 'female'):
                return {'error':401, 'msg':'bad request. visitor_gender only takes male or female as argument. Defaults to both genders'}

        # area not required, defaults to both coex and ipark
        if args['area'] != None:
            area = str(args['area'])
            if area.lower() == 'coex':
                area = 'coex'
            elif area.lower() == 'ipark':
                area = 'ipark'
            else:
                return {'error':401, 'msg':'bad request. area only takes coex or ipark as argument. Defaults to both areas'}

        if args['limit'] != None:
            limit = int(args['limit'])

        placeness = get_trend.analysis(self, category=category, area=area,
            start=start, end=end, age=visitor_age, gender=visitor_gender, limit=limit)
        return placeness, status.HTTP_200_OK

def getArguments(self):
    parser = reqparse.RequestParser()
    parser.add_argument('category', type=str, required=True)
    parser.add_argument('time_range', type=str, required=True)
    parser.add_argument('visitor_age', type=str)
    parser.add_argument('visitor_gender', type=str)
    parser.add_argument('area', type=str)
    parser.add_argument('limit', type=int)
    return parser

def getTimeRange(self, time_range):
    range = time_range.split('-')
    if len(range) == 2:
        start = range[0]
        start = date(int(start[0:4]), int(start[4:6]), int(start[-2:]))
        end = range[1]
        end = date(int(end[0:4]), int(end[4:6]), int(end[-2:]))
    else:
        start = range[0];
        start = date(int(start[0:4]), int(start[4:6]), int(start[-2:]))
        end = date.today()
        print(end)
    return start, end
