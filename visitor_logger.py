#!/usr/bin/env python
# -*- coding: utf-8 -*-

from firebase import firebase
firebase = firebase.FirebaseApplication('https://placenessdb3.firebaseio.com', None)

def post_visit_data(visit_type, ip, timestamp, path, method):
    firebase_path = '/UserVisitData/{}/{}'.format(visit_type.lower(), timestamp)

    new_visit_data = {
        "ip":ip,
        "time":timestamp,
        "path":path,
        "method":method
    }
    result = firebase.post(firebase_path, data=new_visit_data, params={'print':'silent'}, headers={'X_FANCY_HEADER':'VERY FANCY'})

post_visit_data('api', '143.248.55.122', 1504013119, '/placeness_extraction.json', 'get')

