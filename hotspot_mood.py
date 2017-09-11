#-*- coding: utf-8 -*-

'''
Created on 2017. 7. 25.

@author: Jaewoo Kim
@edit: Jaewoo Kim
'''

# for python 3.5
import sys, glob, os

# for python 2.7
# import sys, glob, os
# reload(sys)
# sys.setdefaultencoding('utf-8')

from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse
from flask_api import status

import csv, json, time, random
from gensim.models import Word2Vec
import numpy as np

from operator import itemgetter
from collections import OrderedDict

from location_metadata import getLocationName as namereturn

from scipy.interpolate import interp1d
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.3f')

# Logger-related modules
from flask import request
import time
import visitor_logger

def removeOutBound(_input, _lowerBound, _upperBound):
    _output = _input
    if _input > _upperBound:
        _output = _upperBound
    elif _input < _lowerBound:
        _output = _lowerBound

    return _output


class MoodExtraction(Resource):
    def get(self):
        # Parse GET parameters
        parser = reqparse.RequestParser()
        parser.add_argument('post', type=str)
        parser.add_argument('mode', type=str)
        parser.add_argument('threshold', type=float)
        args = parser.parse_args(strict=True)

        # Logger
        client_ip = request.environ['REMOTE_ADDR']
        input_params = '/mood?post={}&mode={}&threshold={}'.format(
                            args['post'],
                            args['mode'],
                            args['threshold'])
        visitor_logger.post_visit_data('api', client_ip, int(time.time()), input_params, 'get')


        textTotal = args['post']
        threshold = 0.2
        if args['threshold']:
            threshold = removeOutBound(args['threshold'], 0, 1.0)

        # choose 'binary' or None
        thresholdMode = args['mode']

        model = Word2Vec.load("./load/model/insta_160929.model")
        with open('./load/'+'moodWords.json', 'r') as infile:
            for line in infile:
                # json_string = line.read().decode()
                moodWordSeed = json.loads(line)

        list_friendlyWords = moodWordSeed['friendly']
        list_crampWords = moodWordSeed['cramp']
        list_traditionalWords = moodWordSeed['traditional']
        list_modernWords = moodWordSeed['modern']
        list_romanticWords = moodWordSeed['romantic']
        list_relaxingWords = moodWordSeed['relaxing']
        list_loudWords = moodWordSeed['loud']

        m1 = 0
        m2 = 0
        m3 = 0
        m4 = 0
        m5 = 0
        m6 = 0
        m7 = 0
        mc = 0

        linecount = 10
        credMap = interp1d([0.1, 5], [0.1, 0.8])
        modelMap = interp1d([0,1], [0, 0.2])
        scoreMap = interp1d([0, linecount], [0, 1.0])
        scoreMapXLarge = interp1d([0, linecount], [0, 0.7])
        scoreMapLarge = interp1d([0, linecount], [0, 0.8])
        scoreMapSmall = interp1d([0, linecount], [0, 1.2])
        scoreMapXSmall = interp1d([0, linecount], [0, 1.5])
        totalCount = 0


        count = 0
        scoreByModel = 0
        for w in list_friendlyWords:
            count += textTotal.count(w)
            try:
                scoreByModel += modelMap(model.similarity(w,u'친절한'))
            except:
                pass
        count += scoreByModel
        m1 += scoreMapLarge(removeOutBound(count, 0, linecount))
        totalCount += count


        count = 0
        scoreByModel = 0
        for w in list_crampWords:
            count += textTotal.count(w)
            try:
                scoreByModel += modelMap(model.similarity(w,u'답답한'))
            except:
                pass
        count += scoreByModel
        m2 += scoreMapSmall(removeOutBound(count, 0, linecount))
        totalCount += count


        count = 0
        scoreByModel = 0
        for w in list_traditionalWords:
            count += textTotal.count(w)
            try:
                scoreByModel += modelMap(model.similarity(w,u'전통적'))
            except:
                pass
        count += scoreByModel
        m3 += scoreMapLarge(removeOutBound(count, 0, linecount))
        totalCount += count


        count = 0
        scoreByModel = 0
        for w in list_modernWords:
            count += textTotal.count(w)
            try:
                scoreByModel += modelMap(model.similarity(w,u'세련된'))
            except:
                pass
        count += scoreByModel
        m4 += scoreMapSmall(removeOutBound(count, 0, linecount))
        totalCount += count


        count = 0
        scoreByModel = 0
        for w in list_romanticWords:
            count += textTotal.count(w)
            try:
                scoreByModel += modelMap(model.similarity(w,u'로맨틱한'))
            except:
                pass
        count += scoreByModel
        m5 += scoreMapXLarge(removeOutBound(count, 0, linecount))
        totalCount += count



        count = 0
        scoreByModel = 0
        for w in list_relaxingWords:
            count += textTotal.count(w)
            try:
                scoreByModel += modelMap(model.similarity(w,u'편안한'))
            except:
                pass
        count += scoreByModel
        m6 += scoreMap(removeOutBound(count, 0, linecount))
        totalCount += count


        count = 0
        scoreByModel = 0
        for w in list_loudWords:
            count += textTotal.count(w)
            try:
                scoreByModel += modelMap(model.similarity(w,u'북적이는'))
            except:
                pass
        count += scoreByModel
        m7 += scoreMapXSmall(removeOutBound(count, 0, linecount))
        totalCount += count

        # normalizing scores
        raw = [m1,m2,m3,m4,m5,m6,m7]
        if totalCount >= 1:
            norm = [float(i)/sum(raw) for i in raw]
        else:
            norm = raw
        norm = np.round(norm,3)

        if thresholdMode:
            if thresholdMode.lower()=='binary':
                # threshold = 0.2
                tempResult = []
                for n in norm:
                    if n >= threshold:
                        tempResult.append(1)
                    else:
                        tempResult.append(0)
                norm = tempResult



        try:
            wordModelCred = modelMap(model.accuracy(textTotal))
        except:
            wordModelCred = random.uniform(0,0.2)

        mc += (credMap(removeOutBound(totalCount, 0.1, 5)) + removeOutBound(wordModelCred, 0, 0.2))


        # Return a json object.
        if textTotal != '':
            return {'Mood':{'Friendly': norm[0], 'Cramp': norm[1], 'Romantic': norm[4], 'Relaxing': norm[5], 'Loud': norm[6], 'Traditional': norm[2], 'Modern': norm[3]}, 'MoodCredibility':round(mc,3)}
        else:
            return {'msg':'Post not found'}, status.HTTP_404_NOT_FOUND



def getHotspotMoodDistribution(threshold, mode, hotspotName):
    default_threshold = 0.2
    if threshold:
        threshold = removeOutBound(threshold, 0, 1.0)
    else:
        threshold = default_threshold

    # choose 'binary' or None
    thresholdMode = mode

    pid = hotspotName

    directory = './load'
    txtFiles = []

    for files in os.listdir(directory):
        if files.endswith('.txt'):
            txtFiles.append(files)

    for file in txtFiles:
        with open(directory+'/'+file, 'r') as inFile:
            hotspots = {}
            moods = {}
            texts = {}
            creds = {}
            matched = False
            for line in inFile:
                data = json.loads(line)
                # print data['text']
                hotspotName = data['hotspot']
                if hotspotName == pid:

                    nameText = namereturn(hotspotName)
                    m1 = data['Mood'][u'친절한']
                    m2 = data['Mood'][u'답답한']
                    m3 = data['Mood'][u'로맨틱한']
                    m4 = data['Mood'][u'편안한']
                    m5 = data['Mood'][u'북적이는']
                    m6 = data['Mood'][u'전통적']
                    m7 = data['Mood'][u'세련된']
                    mc = data['MoodCredibility']

                    matched = True
                    break

    if not matched:
        #return {'msg':'No matched place id'}, status.HTTP_404_NOT_FOUND
        return None

    # Return a json object.
    else:
        norm = [m1,m2,m3,m4,m5,m6,m7]
        if thresholdMode:
            if thresholdMode.lower()=='binary':
                # threshold = 0.2
                tempResult = []
                for n in norm:
                    if n >= threshold:
                        tempResult.append(1)
                    else:
                        tempResult.append(0)
                norm = tempResult
        return {'Hotspot':nameText,'Mood':{'Friendly': norm[0], 'Cramp': norm[1], 'Romantic': norm[2], 'Relaxing': norm[3], 'Loud': norm[4], 'Traditional': norm[5], 'Modern': norm[6]}, 'MoodCredibility': mc}

def getCredibleMoodsOfHotspot(hotspotId, credibility):
    threshold = 0.2
    mode = 'binary'
    hotspotId = '{}'.format(hotspotId)

    dist = getHotspotMoodDistribution(threshold, mode, hotspotId)
    if(dist is None):
        return None
    elif(credibility <= float(dist['MoodCredibility'])):
        moodList = []

        if(dist['Mood']['Loud'] == 1):
            moodList.append('Loud')
        if(dist['Mood']['Relaxing'] == 1):
            moodList.append('Relaxing')
        if(dist['Mood']['Modern'] == 1):
            moodList.append('Modern')
        if(dist['Mood']['Traditional'] == 1):
            moodList.append('Traditional')
        if(dist['Mood']['Romantic'] == 1):
            moodList.append('Romantic')
        if(dist['Mood']['Friendly'] == 1):
            moodList.append('Friendly')
        if(dist['Mood']['Cramp'] == 1):
            moodList.append('Cramp')

        return moodList
    else:
        return None


class HotspotMoodDistribution(Resource):
    def get(self):
        # Parse GET parameters
        parser = reqparse.RequestParser()
        parser.add_argument('hotspot_name', type=str)
        parser.add_argument('mode', type=str)
        parser.add_argument('threshold', type=float)
        args = parser.parse_args(strict=True)

        # Logger
        client_ip = request.environ['REMOTE_ADDR']
        input_params = '/mood?hotspot_name={}&mode={}&threshold={}'.format(
                            args['hotspot_name'],
                            args['mode'],
                            args['threshold'])
        visitor_logger.post_visit_data('api', client_ip, int(time.time()), input_params, 'get')

        result = getHotspotMoodDistribution(args['threshold'], args['mode'], args['hotspot_name'])
        if(result is None):
            return {'msg':'No matched place id'}, status.HTTP_404_NOT_FOUND
        else:
            return result
        #return getHotspotMoodDistribution(args['threshold'], args['mode'], args['hotspot_name'])


if __name__ == "__main__":
    #result = getHotspotMoodDistribution(0.2, 'binary', '1028771101')
    result = getCredibleMoodsOfHotspot('1028771101', 0.5)
    print(result)
