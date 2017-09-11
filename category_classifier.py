#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import *
from collections import Counter
import datetime
from konlpy.tag import Mecab
from konlpy.tag import Twitter
from firebase import firebase
import operator
import json
import glob
import csv
import itertools
import time


#user_feedback(args['hotspot_id'],args['placeness'],args['feedback_score'])

def user_feedback(args):
    
    placeness = args['placeness']
    hotspot_id = args['hotspot_id']
    feedback_score = int(args['feedback_score'])
    
    db_address = "https://placenessdb3.firebaseio.com/"
    fb = firebase.FirebaseApplication(db_address, None)    
    fb.put("/Feedback/%s" % placeness, name=hotspot_id, data=feedback_score, params={'print': 'silent'})
    return True
    
    
def hotspot_placeness_extraction(hotspotId):
    
    db_address = "https://placenessdb3.firebaseio.com/"
    sub_address = "/CoexIparkPlaceness"
    
    fb = firebase.FirebaseApplication(db_address, None)    
    hotspot_address = "%s/%s/%s" % (db_address, sub_address, hotspotId)
    
    result = fb.get(hotspot_address, None, params={'shallow':'false'})
    resultDict = json.loads(result)
    
    
    placenessList = []
    for placeness, count in resultDict['placeness'].items():
        formattedDict = {}
        
        formattedDict['count'] = count
        
        items = placeness.split("/")
        
        for item in items:
            factor, value = item.split("_")
            formattedDict[factor] = value
            
        placenessList.append(formattedDict)
        
    placenessDict = {"hotspot_id":hotspotId, "placeness":placenessList}
    
    return placenessDict
     

def feature_extraction(text,timestamp):
    
    corpusName = "corpus_TOUM.csv"
    data = []
    
    #sampletimestamp = "1433435470"
    
    userid = "0"
    postid = "0"
    
    sampletuple = (text, datetime.datetime.fromtimestamp(int(timestamp)),userid,postid)
    data.append(sampletuple)
    
    textCL = TextClassifier()
    textCL.data = data
    textCL.loadCategoryFromFile(corpusName,"utf-8")
    textCL.extractCategory()

    result = getPlacenessCombination(textCL.outputList) 
    return result


def getPlacenessCombination(dataList):
    
    resultCounter = Counter()

    
    for data in dataList:
        
        totalList = []
        
                            
        for k, v in data.items():             
            if k not in ["text", "userid", "hotspot","pid","MoodCredibility","datetime"]:  # ignore text data
                for k2, v in v.items():
                    if v == 1:  # write all keys into json
                        totalList.append("%s_%s" % (k, k2))
                            
        n = 10
        r = min(n, len(totalList))
        
        for i in range(1, r + 1):
            comblist = list(itertools.combinations(totalList, i))
            
            for item in comblist:            
                if len(set([x.split("_")[0] for x in item])) == len(item):
                    
                    key = tuple(item)
                    
                    #if key == u"Occasion_\uc601\ud654/isWeekend_weekday":
                    #    print filename, data["text"]
                    resultCounter[key] += 1
                            
    
    
    resultList = []
    
    for key, count in resultCounter.items():
        formattedDict = {}
        
        formattedDict['count'] = count
        for item in key:
            if item != "":
                factor, value = item.split("_")
                formattedDict[factor] = value
            
        resultList.append(formattedDict)
        
    resultDict = {"placeness":resultList}
    
    return resultDict


def loadDataFromFirebase(db_address, sub_address, hotspotId):
    data = []
    fb = firebase.FirebaseApplication(db_address, None)
    
    hotspot_address = "%s/%s" % (sub_address, hotspotId)
    #print(hotspot_address)
    
    districtresult = fb.get(hotspot_address, None, params={'shallow':'true'})
    
    print(len(districtresult))
    
     
    
    count = 0
    for k,v in districtresult.items():        
        v = fb.get(hotspot_address + "/%s" % k, None)
        try:
            print(count, v)
            data.append((v['caption'],datetime.datetime.fromtimestamp(int(v['date'])),v['owner']['id'],v['id']))
        except:
            pass
        
        count += 1
        
    return data


class Classifier:

    __metaclass__ = ABCMeta
    
    @abstractproperty    
    def data(self):
        pass
    @data.setter
    def data(self, val):
        pass
    
    @abstractproperty
    def outputList(self):
        pass
    
    @abstractproperty
    def outputDict(self):
        pass
        
    @abstractproperty
    def category(self):
        pass
    
    @category.setter
    def category(self, val):
        pass
    
    @abstractmethod
    def extractCategory(self):
        pass
    
    def printer(self, prefix, encoding="utf-8"):       
        
        filename_list = "output/%s_list_%s.csv" % (prefix, encoding)
        
        fw = open(filename_list, "w")
        
        for result in self._outputList:
            fw.write("%s\n" % json.dumps(result)) 
        fw.close()

        
        filename_dict = "output/%s_dict_%s.csv" % (prefix, encoding) 
        
        
        fw = open(filename_dict, "w")
        fw.write("total: %s\n" % len(self._outputList))
        fw.write("category1,categeory2,count\n")
        
        
        for k1, v1 in self._outputDict.items():
            for k2, v2 in v1.items():
                fw.write("%s,%s,%s\n" % (k1.decode("utf-8").encode(encoding), k2.decode("utf-8").encode(encoding), v2))
                
        fw.close()
        """
        sorted_outputDict = sorted(self._outputDict.items(), key=operator.itemgetter(1),reverse=True)
        
        fw = open(filename_dict, "w")
        fw.write("total: %s\n" % len(sorted_outputDict))
        fw.write("category1,categeory2,count\n")        
        for k1,v1 in sorted_outputDict:
            
            for k2,v2 in 
            
            try:
                fw.write("%s,%s,%s\n" % (k.decode("utf-8").encode(encoding),v))
            except:
                pass                
        fw.close()
        
        """

class TimeClassifier(Classifier):
    _data = []
    _keywordCategoryDict = {}
    _outputList = []
    _outputDict = Counter()
    
    @property    
    def data(self):
        return self._data
        
    @data.setter
    def data(self, val):
        self._data = val         

    @property
    def outputList(self):
        return self._outputList
    
    @property
    def outputDict(self):
        return self._outputDict
        
    @property
    def category(self):
        return self._keywordCategoryDict
    
    @category.setter
    def category(self, val):
        for c, timeZone in val.items():            
            self.category[tuple(timeZone)] = c
            
    def isInTimeZone(self, _time, timeZone):
        start = timeZone[0]
        end = timeZone[1]
                
        if _time.time() >= start and _time.time() < end:
            return True
        else:
            return False
            
    def extractCategory(self):        
        for _time in self._data:            
            categoryCounter = Counter()
            for timeZone, category in self._keywordCategoryDict.items():                                 
                if self.isInTimeZone(_time, timeZone):                
                    categoryCounter[category] += 1
                    self._outputDict[category] += 1
            self._outputList.append(categoryCounter)
            
                    
class TextClassifier(Classifier):

    def __init__(self):    
        self._data = []
        self._keywordCategoryDict = {}
        self._categoryList = []
        self._outputList = []
        self._outputDict = Counter()
        self._wordCounter = Counter()
        self._weatherDict = {}        
        self._morph_analyzer = Twitter()
        

    @property    
    def data(self):
        return self._data
        
    @data.setter
    def data(self, val):
        self._data = val         

    @property
    def outputList(self):
        return self._outputList
    
    @property
    def outputDict(self):
        return self._outputDict
        
    @property
    def category(self):
        return self._keywordCategoryDict
    
    @category.setter
    def category(self, val):
        for c, wordList in val.items():
            for word in wordList:                
                self.category[word] = c
            
    def extractCategory(self,hotspot="None"):
        
        self._outputList = []
        self._outputDict = Counter()        

        isWeekdayDict = self.getWordDict("isWeekday.csv")
        isWeekendDict = self.getWordDict("isWeekend.csv")
                
        for text, timedata, userid, pid in self._data:            
            try:
                #print(pid)
                categoryCounter = self.setCategoryCounter()
                            
                categoryCounter["text"] = text            
                categoryCounter["userid"] = userid
                categoryCounter["hotspot"] = hotspot
                categoryCounter["pid"] = pid
                categoryCounter["datetime"] = timedata.strftime("%Y-%m-%d %H:%M:%S")
                categoryCounter["Weather"] = self.weatherDictProcess(timedata.strftime("%Y-%m-%d"))
                
                for word, pos in self._morph_analyzer.pos(text):
                    
                    #print(word, pos)   
                    self._wordCounter["%s,%s" % (word, pos)] += 1             
                    if word in self._keywordCategoryDict:
                        
                        clv1 = self._keywordCategoryDict[word][0]                             
                        clv2 = self._keywordCategoryDict[word][1]
                        
                        
                        """
                        if clv1 not in categoryCounter:
                            categoryCounter[clv1] = Counter()
                        """
                        
                        categoryCounter[clv1][clv2] += 1
                        
                        if clv1 not in self._outputDict:
                            self._outputDict[clv1] = Counter()
                        
                        self._outputDict[clv1][clv2] += 1                               
                        # print word, self._keywordCategoryDict[word]
                
                
                timeDict = self.setTimeCategory(text, timedata, isWeekdayDict, isWeekendDict)
                
                for k,v in timeDict.items():                    
                    categoryCounter[k] = v
                    
                    if k not in self._outputDict:
                        self._outputDict[k] = Counter()

                    for k1, v1 in v.items():
                        self._outputDict[k][k1] += v1
                
                self._outputList.append(categoryCounter)
                
                
            except:
                print("extraction error: ", text)                       
                # pass
                
    
    def loadDataFromFile(self, path, encoding):    
        self._data = []    
        f = open(path)        
        for l in f:
            self._data.append(l.strip().decode(encoding))            
        f.close()    
        
    def loadCategoryFromFile(self, path, encoding):        
        f = open(path, 'rt', encoding='UTF8')
        for l in f:
            ls = l.strip().split(",")            
            category1 = ls[0]         
            category2 = ls[1]
            
            self._categoryList.append((category1, category2))
            
            for word in ls[2:]:                
                self._keywordCategoryDict[word] = (category1, category2)        
        f.close()
        
    def getWordDict(self, path, encoding="utf-8"):
        
        wordDict = {}
        f = open(path, 'rt', encoding='UTF8')
        
        for l in f:
            word = l.strip()
            wordDict[word] = 0
            
        f.close()
        
        return wordDict
        
    def writeWordCounter(self, prefix, encoding="utf-8"):
        sorted_wordCounter = sorted(self._wordCounter.items(), key=operator.itemgetter(1), reverse=True)

        filename = "output/%s_wordcount_%s.csv" % (prefix, encoding)
        
        fw = open(filename, "w")
        fw.write("word,pos,count\n")
        for k, v in sorted_wordCounter:            
            try:
                fw.write("%s,%s\n" % (k.encode(encoding), v))                
            except:                
                pass
            
        fw.close()
        
    
    def setCategoryCounter(self):
        categoryCounter = Counter()
        
        for category1, category2 in self._categoryList:        
            if category1 not in categoryCounter:
                categoryCounter[category1] = {}
                
            categoryCounter[category1][category2] = 0
        
        return categoryCounter
    
    def setTimeCategory(self, text, timedata, isWeekdayDict, isWeekendDict):
        
        timeDict = {}
        
        self.checkMAEN(timedata, timeDict)
        self.checkSeason(timedata, timeDict)
        self.checkWeekend(timedata, timeDict, text, isWeekdayDict, isWeekendDict)
        
        return timeDict        
                
        
    
    def checkMAEN(self, timedata, timeDict):
        maenDict = {"morning":0, "afternoon":0, "evening":0, "night":0}
        
        hour = timedata.hour
        maen = ""
        
        if hour >= 6 and hour < 12: maenDict["morning"] += 1
        elif hour >= 12 and hour < 17: maenDict["afternoon"] += 1
        elif hour >= 17 and hour < 21: maenDict["evening"] += 1
        else: maenDict["night"] += 1
        
        timeDict["maen"] = maenDict
        
        
    
    def checkWeekend(self, timedata, timeDict, text, isWeekdayDict, isWeekendDict):
        
        for word in isWeekendDict.keys():
            if word in text:                
                timeDict["isWeekend"] = {"weekday":0, "weekend":1}
                return
                
        for word in isWeekdayDict.keys():
            if word in text:                
                timeDict["isWeekend"] = {"weekday":1, "weekend":0}
                return
        
        if timedata.weekday() > 4:
            timeDict["isWeekend"] = {"weekday":0, "weekend":1}            
        else:
            timeDict["isWeekend"] = {"weekday":1, "weekend":0}            
        
    def checkSeason(self, timedata, timeDict):
        seasonDict = {"spring":0, "summer":0, "autumn":0, "winter":0}

        
        month = timedata.month
        
        if month >= 3 and month < 6: seasonDict["spring"] += 1
        elif month >= 6 and month < 9: seasonDict["summer"] += 1
        elif month >= 9 and month < 12: seasonDict["autumn"] += 1
        else: seasonDict["winter"] += 1
        
        timeDict["Season"] = seasonDict

    def firebaseFormatter(self,hotspot):
        
        formattedDict = {}
        
        for output in self._outputList:
            formattedDict[output["pid"]] = output
                
        return formattedDict
    
    
    
    def getWeatherDict(self, pathname):
        filelist = glob.glob(pathname + "/*.csv")
        for fname in filelist:
            with open(fname) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    date = row["일시"]
                    if date not in self._weatherDict:
                        self._weatherDict[date] = {}   
                    
                    try:
                        self._weatherDict[date]["rain"] = float(row["일강수량.mm."])
                        self._weatherDict[date]["wind"] = float(row["평균.풍속.m.s."])
                        self._weatherDict[date]["temp"] = float(row["평균기온..C."])
                        self._weatherDict[date]["snow"] = float(row["일.최심적설.cm."])
                    except:
                        self._weatherDict[date]["rain"] = None
                        self._weatherDict[date]["wind"] = None
                        self._weatherDict[date]["temp"] = None
                        self._weatherDict[date]["snow"] = None
        
    
    #date의 자료형은 string이다. 예) "2010-01-01"
    def weatherDictProcess(self, date):
        resultDict = {}
        
        resultDict["rain"] = {"no":0, "low":0, "normal":0, "high":0}
        resultDict["wind"] = {"low":0, "normal":0, "high":0}
        resultDict["temp"] = {"low":0, "normal":0, "high":0}
        resultDict["snow"] = {"no":0, "low":0, "normal":0, "high":0}
        
        if date not in self._weatherDict:
            return resultDict 
        
        if self._weatherDict[date]["rain"] == 0:
            resultDict["rain"]["no"] = 1
        if self._weatherDict[date]["rain"] <= 2:
            resultDict["rain"]["low"] = 1            
        elif self._weatherDict[date]["rain"] <= 15:            
            resultDict["rain"]["normal"] = 1            
        else:
            resultDict["rain"]["high"] = 1
    
        if self._weatherDict[date]["wind"] <= 1:
            resultDict["wind"]["low"] = 1            
        elif self._weatherDict[date]["wind"] <= 2:            
            resultDict["wind"]["normal"] = 1            
        else:
            resultDict["wind"]["high"] = 1
            
        if self._weatherDict[date]["temp"] <= 15:
            resultDict["temp"]["low"] = 1            
        elif self._weatherDict[date]["temp"] <= 26:            
            resultDict["temp"]["normal"] = 1            
        else:
            resultDict["temp"]["high"] = 1
            
        if self._weatherDict[date]["snow"] == 0:
            resultDict["snow"]["no"] = 1
        elif self._weatherDict[date]["snow"] <= 1:
            resultDict["snow"]["low"] = 1            
        elif self._weatherDict[date]["snow"] <= 3:            
            resultDict["snow"]["normal"] = 1            
        else:
            resultDict["snow"]["high"] = 1
            
        return(resultDict)
            
if __name__ == "__main__":
    #hotspot_placeness_extraction("246221160")
    pass
    
        
        
    
    
    