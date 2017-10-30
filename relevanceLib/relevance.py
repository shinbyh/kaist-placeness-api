# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 13:10:18 2017

@author: doheum
"""

import networkx as nx
import sys
import operator
import time
import imp

imp.reload(sys)

class relevance:
    def __init__(self):        
        self.graph=None
        self.venues=[]
        self.users=[]
        self.placeness=[]
        self.occasion_keywords=[]
        self.mood_keywords=[]
        self.time_keywords=[]
        self.with_keywords=[]
        self.user_keywords=[]
        self.weather_keywords=[]
        
        return
        
    def load_network(self, file_path):
        self.graph=nx.read_gexf(file_path)
        self.venues=list((n for n in self.graph.nodes() if self.graph.node[n]['bipartite']=='venue'))
        self.users=list((n for n in self.graph.nodes() if self.graph.node[n]['bipartite']=='user'))
        self.placeness=list((n for n in self.graph.nodes() if self.graph.node[n]['bipartite']=='pl'))
        print("The basic properties of the network:")
        print('The number of venues: ', len(self.venues))
        print('The number of users: ', len(self.users))
        print('The number of placeness: ', len(self.placeness))
        print('The number of edges:', self.graph.number_of_edges())
        
        return
        
    def load_placeness_keywords(self):
        placeness_set=set()
        for pl in self.placeness:
            for plu in pl.split('/'):
                placeness_set.add(plu)
        
        self.occasion_keywords=[]
        self.mood_keywords=[]
        self.time_keywords=[]
        self.user_keywords=[]
        self.weather_keywords=[]
        self.with_keywords=[]
        
        for pl in placeness_set:
            if 'Occasion' in pl:
                self.occasion_keywords.append(pl)
            elif 'With' in pl:
                self.with_keywords.append(pl)
            elif 'Mood' in pl:
                self.mood_keywords.append(pl)
            elif 'User' in pl:
                self.user_keywords.append(pl)
            elif 'Weather' in pl:
                self.weather_keywords.append(pl)
            else:
                self.time_keywords.append(pl)
        return
    
    def EgocentricPagerankTopNwithQuery(self,query,topk,alpha,weights=None):
        result=self.calculateEgocentricPagerankwithQuery(query,alpha,weights)
        #print result
        if topk=='all':
            return result
        else:
            return result[0:topk]
    ## 
    
    def calculateEgocentricPagerankwithQuery(self,query,alpha,weights):
        personalization_weight=1000000#sys.maxint
        if query:
            personalized=dict.fromkeys(nx.nodes(self.graph),1)
            
            for q in query:
                w=0
                if q in self.time_keywords:
                    w=weights['time']
                elif q in self.with_keywords:
                    w=weights['with']
                elif q in self.occasion_keywords:
                    w=weights['occasion']
                elif q in self.mood_keywords:
                    w=weights['mood']
                elif q in self.user_keywords:
                    w=weights['user']
                elif q in self.weather_keywords:
                    w=weights['weather']
                
                #q=unicode(q)

                match_query=self.get_placeness(q)
                #print(match_query[0])
                #print(personalization_weight*w)
                for m in match_query:
                    personalized[m] += personalization_weight*w
                        #print q, m
            pr=nx.pagerank(self.graph, personalization=personalized,alpha=alpha)
        else:
            pr=nx.pagerank(self.graph, alpha=alpha)
            
        venue_pr = dict((k,v) for k,v in list(pr.items()) if k in self.venues)
        venue_pr = sorted(list(venue_pr.items()), key = operator.itemgetter(1))
        venue_pr.reverse()
        
        return venue_pr
        
    def query(self, time_kwd=None, with_kwd=None, occasion_kwd=None, mood_kwd=None, weather_kwd=None, user_kwd=None, weight_time=1.0, weight_with=1.0, weight_occasion=1.0, weight_mood=1.0, weight_weather=1.0, weight_user=1.0, weight_query=0.85, topk=5):
        recommendation=None        
        
        start_time = time.time()        
        
        query=[]
        if time_kwd:
            query+=self.convert_time(time_kwd)
        if with_kwd:
            query+=self.convert_with(with_kwd)
        if occasion_kwd:
            query+=self.convert_occasion(occasion_kwd)
        if mood_kwd:
            query+=self.convert_mood(mood_kwd)
        if weather_kwd:
            query+=self.convert_weather(weather_kwd)
        if user_kwd:
            query+=self.convert_user(user_kwd)

        #print(query)
        
        weights={'time': weight_time, 'with': weight_with, 'occasion': weight_occasion, 'mood': weight_mood, 'weather': weight_weather, 'user': weight_user}

        #print(weights)

        recommendation=self.EgocentricPagerankTopNwithQuery(query,topk,weight_query,weights)
                
        end_time = time.time()
        
        print('Done, it took %.03f seconds' % (end_time - start_time))
        running_time = end_time-start_time 
        
        return recommendation, running_time
        
    def convert_time(self, kwds):
        #query=[]        
        return kwds
    
    def convert_with(self, kwds):
        #query=[]        
        return kwds
    
    def convert_occasion(self, kwds):
        #query=[]        
        return kwds
    
    def convert_mood(self, kwds):
        #query=[]        
        return kwds
        
    def convert_weather(self, kwds):
        #query=[]        
        return kwds
	
    def convert_user(self, kwds):
        #query=[]        
        return kwds
        
    def get_placeness(self, query=None):
        list_placeness=self.placeness
        if query:
            list_placeness = [k for k in self.placeness if query in k]
            
        return list_placeness