# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 13:10:18 2017

@author: doheum
"""

import networkx as nx
from scipy.spatial.distance import cosine
import sys
import operator
import csv
import copy
import time
import imp

imp.reload(sys)
sys.setdefaultencoding('utf8')

class recommendation:
    def __init__(self):        
        self.tag_venue_graph=None
        self.user_venue_graph=None
        self.user_placeness_venue_graph=None
        self.venues=[]
        self.tags=[]
        self.users=[]
        self.placeness=[]
        self.UserSimilarityMatrix=None
        self.community={}
        self.num_exists=0
        self.num_dne=0
        
        return
        
    def load_tripartite_network(self, file_path):
        self.user_placeness_venue_graph=nx.read_gexf(file_path)
        self.venues=list((n for n in self.user_placeness_venue_graph.nodes() if self.user_placeness_venue_graph.node[n]['bipartite']=='venue'))
        self.users=list((n for n in self.user_placeness_venue_graph.nodes() if self.user_placeness_venue_graph.node[n]['bipartite']=='user'))
        self.placeness=list((n for n in self.user_placeness_venue_graph.nodes() if self.user_placeness_venue_graph.node[n]['bipartite']=='pl'))
        
        print('The number of venues: ', len(self.venues))
        print(self.venues)
        print('The number of users: ', len(self.users))
        print('The number of placeness: ', len(self.placeness))
        
        return
    
    def load_networks(self, user_placeness_venue_file_path, tag_venue_file_path, user_venue_file_path):
        self.user_placeness_venue_graph=nx.read_gexf(user_placeness_venue_file_path)
        self.tag_venue_graph=nx.read_gexf(tag_venue_file_path)
        self.user_venue_graph=nx.read_gexf(user_venue_file_path)
        
        prev_venues=len(self.venues)
        prev_users=len(self.users)
        prev_placeness=len(self.placeness)
        prev_tags=len(self.tags)
        
        # extract the joint of three networks
        while 1:
            deg = self.tag_venue_graph.degree()
            to_remove = [n for n in deg if deg[n] == 0]
            self.tag_venue_graph.remove_nodes_from(to_remove)
            
            deg = self.user_venue_graph.degree()
            to_remove = [n for n in deg if deg[n] == 0]
            self.user_venue_graph.remove_nodes_from(to_remove)
            
            deg = self.user_placeness_venue_graph.degree()
            to_remove = [n for n in deg if deg[n] == 0]
            self.user_placeness_venue_graph.remove_nodes_from(to_remove)
            
            v_user_placeness_venue_graph=list((n for n in self.user_placeness_venue_graph.nodes() if self.user_placeness_venue_graph.node[n]['bipartite']=='venue'))
            v_tag_venue_graph=list((n for n in self.tag_venue_graph.nodes() if self.tag_venue_graph.node[n]['bipartite']=='venue'))
            v_user_venue_graph=list(set((n for n in self.user_venue_graph.nodes() if self.user_venue_graph.node[n]['bipartite']=='venue')))
            
            u_user_placeness_venue_graph=list((n for n in self.user_placeness_venue_graph.nodes() if self.user_placeness_venue_graph.node[n]['bipartite']=='user'))
            u_user_venue_graph=list(set((n for n in self.user_venue_graph.nodes() if self.user_venue_graph.node[n]['bipartite']=='user')))
            
            self.venues = list(set(v_tag_venue_graph) & set(v_user_venue_graph) & set(v_user_placeness_venue_graph))
            self.users = list(set(u_user_venue_graph) & set(u_user_placeness_venue_graph))
            self.tags=list((n for n in self.tag_venue_graph.nodes() if self.tag_venue_graph.node[n]['bipartite']=='tag'))
            self.placeness=list((n for n in self.user_placeness_venue_graph.nodes() if self.user_placeness_venue_graph.node[n]['bipartite']=='pl'))
            
            # trim networks       
            for v in v_tag_venue_graph:
                if not v in self.venues:
                    self.tag_venue_graph.remove_node(v)
                    
            for v in v_user_venue_graph:
                if not v in self.venues:
                    self.user_venue_graph.remove_node(v)
            
            for v in v_user_placeness_venue_graph:
                if not v in self.venues:
                    self.user_placeness_venue_graph.remove_node(v)
                    
            for u in u_user_venue_graph:
                if not u in self.users:
                    self.user_venue_graph.remove_node(u)
                    
            for u in u_user_placeness_venue_graph:
                if not u in self.users:
                    self.user_placeness_venue_graph.remove_node(u)
            
            if prev_venues==len(self.venues) and prev_users==len(self.users) and prev_placeness==len(self.placeness) and prev_tags==len(self.tags):
                break
            else:
                prev_venues=len(self.venues)
                prev_users=len(self.users)
                prev_placeness=len(self.placeness)
                prev_tags=len(self.tags)
        
        print('The number of venues: ', len(self.venues))
        print(self.venues)
        print('The number of users: ', len(self.users))
        print('The number of tags: ', len(self.tags))
        print('The number of placeness: ', len(self.placeness))
    
    """
    popularityTopN
    
    @desc: This function calculates the popularity (the number of visits) of each venue
    and sort the venues in the decreasing order. Then it fetches top N venues from the sorted list and return it.
    
    @input:
    - topN: the range of the ranks to fetch (ex: 1 - Top 1, 5 - Top 5)
    
    @output:
    - popularTopN: the list of Top N venues in the order of its popularity
    """
    def popularityTopN(self,topN):
        sorted_places=[]    
        for p in self.venues:
            if nx.degree(self.user_venue_graph,p,weight='weight')=={}:
                sorted_places.append([p,0.0])
            else:
                sorted_places.append([p,nx.degree(self.user_venue_graph,p,weight='weight')])
        sorted_places=sorted(sorted_places, key=lambda t: t[1],reverse=True)
        
        popularTopN=sorted_places[0:topN]
            
        return popularTopN
    
    """
    calculateEgocentricPagerank
    
    @desc: This function calculates the egocentric pagerank of each venue for a user
    and sort the venues in the decreasing order. Then it fetches top N venues from the sorted list and return it.
    
    @input:
    - topN: the range of the ranks to fetch (ex: 1 - Top 1, 5 - Top 5)
    
    @output:
    - venue_pr: the list of Top N venues in the order of its popularity
    """
    def calculateEgocentricPagerank(self,user,_alpha):        
        personalized=dict.fromkeys(nx.nodes(self.user_placeness_venue_graph),1)
        personalized[user]=sys.maxsize
        
        pr=nx.pagerank(self.user_placeness_venue_graph, personalization=personalized,alpha=_alpha)
        
        venue_pr = dict((k,v) for k,v in list(pr.items()) if k in self.venues)
        venue_pr = sorted(list(venue_pr.items()), key = operator.itemgetter(1))
        venue_pr.reverse()

        return venue_pr
    
    """
    EgocentricPagerankTopN
    
    @desc: This function fetches top N venues from the list of venues with egocentric pagerank values and return them.
    
    @input:
    - topN: the range of the ranks to fetch (ex: 1 - Top 1, 5 - Top 5)
    
    @output:
    - result[0:topk]: the list of Top N venues in the order of egocentric pagerank values
    """    
    def EgocentricPagerankTopN(self,user,topk,alpha):
        result=self.calculateEgocentricPagerank(user,alpha)
        #print result
        return result[0:topk]
    
    """
    loadCommunity
    
    @desc: This function saves the communities to which the nodes belong into ''self.community'' by loading a community file.
    
    @input:
    - file_path: the file path for the community file
    
    """ 
    def loadCommunity(self,file_path):
        with open(file_path, mode='r') as infile:
            reader = csv.reader(infile)
            for rows in reader:
                node=str(rows[0])
                comm=int(rows[1])
                if node.count('user_') > 0:
                    node=str(node.replace('user_','u'))
                elif node.count('venue_') > 0:
                    node=str(node.replace('venue_','v'))
                #print node
                self.community[node]=int(comm)
        
        return
    
    """
    loadCommunity
    
    @desc: This function extracts a subgraph to which 'node' belongs.
    
    @input:
    - node: the target node to find to which community it belongs
    
    @output:
    - community: the subgraph to which 'user' belongs (network type)
    """ 
    def extractCommunity(self,node):
        community=nx.Graph()     
        
        node=str(node)
        if node in self.community:
            self.num_exists+=1
            community_num=self.community[node]
            community=copy.deepcopy(self.user_placeness_venue_graph)
        
            for n in community.nodes():
                if n in self.community:
                    if not self.community[n] == community_num:
                        community.remove_node(n)
                else:
                    #print n, ' DNE'
                    community.remove_node(n)
        else:
            self.num_dne+=1
            #print node, 'does not exist'
            #exit()
        
        return community
        
    def calculateCommunityEgocentricPagerank(self,user,_alpha):
        #community subgraph
        community=self.extractCommunity(user)
        personalized=dict.fromkeys(nx.nodes(community),1)
        personalized[user]=sys.maxsize
        
        pr=nx.pagerank(community, personalization=personalized,alpha=_alpha)
        
        venue_pr = dict((k,v) for k,v in list(pr.items()) if k in self.venues)
        venue_pr = sorted(list(venue_pr.items()), key = operator.itemgetter(1))
        venue_pr.reverse()

        return venue_pr
    
    def CommunityEgocentricPagerankTopN(self,user,topk,alpha):
        result=self.calculateCommunityEgocentricPagerank(user,alpha)
        return result[0:topk]
    
    def EgocentricPagerankTopNwithQuery(self,query,topk,alpha,weights=None):
        result=self.calculateEgocentricPagerankwithQuery(query,alpha)
        #print result
        return result[0:topk]
    ## 
    
    def calculateEgocentricPagerankwithQuery(self,query,_alpha):

        if query:
            personalized=dict.fromkeys(nx.nodes(self.user_placeness_venue_graph),1)
            
            #print query
            if type(query) is list:
                for q in query:
                    q=str(q)
                    if q in self.users:
                        personalized[q]=sys.maxsize
                    elif q in self.venues:
                        personalized[q]=sys.maxsize
                    else:
                        match_query = [k for k in list(personalized.keys()) if q in k]
                        for m in match_query:
                            personalized[m] = sys.maxsize
                            #print q, m
            else:
                query=str(query)
                if query in self.users:
                    personalized[query]=sys.maxsize
                elif query in self.venues:
                    personalized[query]=sys.maxsize
                else:   
                    match_query = [k for k in list(personalized.keys()) if query in k]
                    for m in match_query:
                        personalized[m] = sys.maxsize
            pr=nx.pagerank(self.user_placeness_venue_graph, personalization=personalized,alpha=_alpha)
        else:
            pr=nx.pagerank(self.user_placeness_venue_graph, alpha=_alpha)
            
        venue_pr = dict((k,v) for k,v in list(pr.items()) if k in self.venues)
        venue_pr = sorted(list(venue_pr.items()), key = operator.itemgetter(1))
        venue_pr.reverse()     
        
        return venue_pr
    
    def CommunityEgocentricPagerankTopNwithQuery(self,query,topk,alpha):
        result=self.calculateCommunityEgocentricPagerankwithQuery(query,alpha)
        return result[0:topk]
    
    def calculateCommunityEgocentricPagerankwithQuery(self,query,_alpha):
        self.num_exists=0
        self.num_dne=0
        total_graph=nx.Graph()
        if query:
            if type(query) is list:
                for q in query:
                    if q in self.users or q in self.venues:
                        community=self.extractCommunity(q)
                        total_graph=nx.compose(total_graph,community)
                    else:   
                        match_query = [k for k in self.placeness if q in k]
                        for m in match_query:
                            community=self.extractCommunity(m)
                            total_graph=nx.compose(total_graph,community)
            else:
                if query in self.users or query in self.venues:
                    total_graph=self.extractCommunity(query)
                else:   
                    match_query = [k for k in self.placeness if query in k]
                    for m in match_query:
                        community=self.extractCommunity(m)
                        total_graph=nx.compose(total_graph,community)
            
            personalized=dict.fromkeys(nx.nodes(total_graph),1)
            
            if type(query) is list:
                for q in query:
                    if q in self.users:
                        personalized[q]=sys.maxsize
                    elif q in self.venues:
                        personalized[q]=sys.maxsize
                    else:   
                        match_query = [k for k in list(personalized.keys()) if q in k]
                        for m in match_query:
                            personalized[m] = sys.maxsize
            else:
                if query in self.users:
                    personalized[query]=sys.maxsize
                elif query in self.venues:
                    personalized[query]=sys.maxsize
                else:   
                    match_query = [k for k in list(personalized.keys()) if query in k]
                    for m in match_query:
                        personalized[m] = sys.maxsize
                        
            pr=nx.pagerank(total_graph, personalization=personalized,alpha=_alpha)
        else:
            pr=nx.pagerank(self.user_placeness_venue_graph, alpha=_alpha)
            
        venue_pr = dict((k,v) for k,v in list(pr.items()) if k in self.venues)
        venue_pr = sorted(list(venue_pr.items()), key = operator.itemgetter(1))
        venue_pr.reverse()

        print(self.num_exists, self.num_dne)  

        return venue_pr
        
    def test(self, method='popularity', topk=5, alpha=0.85, f_comm=None):
        start_time = time.time()        
        
        true_positive=0
        false_positive=0
        false_negative=0        
        
        if method=='cf':
            self.createUserSimilarityMatrix()
        elif method=='community_pagerank':
            if f_comm:
                self.loadCommunity(f_comm)
            else:
                print('Please specify the path for community file')
        
        for u in self.users:
            if method=='popularity':
                recommendation=self.popularityTopN(topk)
            elif method=='cf':
                recommendation=self.CollaboFilteringTopN(u,topk)
            elif method=='pagerank':
                recommendation=self.EgocentricPagerankTopN(u,topk,alpha)
            elif method=='community_pagerank':
                recommendation=self.CommunityEgocentricPagerankTopN(u,topk,alpha)
                
            recommended_places=[]
            for p in recommendation:
                recommended_places.append(p[0])
            
            visited_places=nx.neighbors(self.user_venue_graph,u)
            for p in visited_places:
                if p in recommended_places:
                    true_positive+=1
                else:
                    false_negative+=1
            for p in recommended_places:
                if not p in visited_places:
                    false_positive+=1
        
        # result
        print('True Positive: ', true_positive)
        print('False Positive: ', false_positive)
        print('False Negative: ', false_negative)
        
        precision=float(true_positive)/float(true_positive+false_positive)
        recall=float(true_positive)/float(true_positive+false_negative)
        f_measure=2*(precision*recall)/(precision+recall)
        
        print('Precision: ', precision)
        print('Recall: ', recall)
        print('F-measure: ', f_measure)
        
        end_time = time.time()
        
        print('Running Time : %.03f s' % (end_time - start_time))
        running_time = end_time-start_time 
        
        return running_time
        
    def query(self, method='popularity', topk=5, alpha=0.85, query=None, f_comm=None):
        recommendation=None        
        
        start_time = time.time()        
        
        if method=='community_pagerank':
            if f_comm:
                self.loadCommunity(f_comm)
            else:
                print('Please specify the path for community file')
        
        if method=='popularity':
            recommendation=self.popularityTopN(topk)
        
        elif method=='pagerank':
            if query:
                recommendation=self.EgocentricPagerankTopNwithQuery(query,topk,alpha)
            else:
                recommendation=self.EgocentricPagerankTopNwithQuery(query,topk,alpha)
            
        elif method=='community_pagerank':
            if query:
                recommendation=self.CommunityEgocentricPagerankTopNwithQuery(query,topk,alpha)
            else:
                recommendation=self.CommunityEgocentricPagerankTopNwithQuery(query,topk,alpha)
                
        end_time = time.time()
        
        #print 'Running Time : %.03f s' % (end_time - start_time)
        running_time = end_time-start_time 
        
        return recommendation, running_time
        
    def relevance_query(self, date=None, with_whom=None, occasion=None, mood=None, weight_date=1.0, weight_with=1.0, weight_occasion=1.0, weight_mood=1.0, weight_query=0.85, topk=5):
        recommendation=None        
        
        start_time = time.time()        
        
        query=[]
        query+=self.convert_date(date)
        query+=self.convert_with(with_whom)
        query+=self.convert_occasion(occasion)
        query+=self.convert_mood(mood)
        
        weights={'date': weight_date, 'with': weight_with, 'occasion': weight_occasion, 'mood': weight_mood}
        
        recommendation=self.EgocentricPagerankTopNwithQuery(query,topk,weight_query,weights)
                
        end_time = time.time()
        
        #print 'Running Time : %.03f s' % (end_time - start_time)
        running_time = end_time-start_time 
        
        return recommendation, running_time
        
    def convert_date(self, _input):
        query=[]        
        return query
    
    def convert_with(self, _input):
        query=[]        
        return query
    
    def convert_occasion(self, _input):
        query=[]        
        return query
    
    def convert_mood(self, _input):
        query=[]        
        return query

# code for collaborative filtering
#"""
#    createUserSimilarityMatrix
#    
#    @author: doheum, yonghan
#    
#    @desc: This function creates the matrix of user similarity values. In this function, the similarity of two different users
#    is defined as the cosine similarity of their check-in vectors.
#    
#    @input:
#    
#    @output:
#    - UserSimilarityMatrix: the nested list of user similarity values
#    """
#    def createUserSimilarityMatrix(self):
#        # code here    
#        self.UserSimilarityMatrix=[[0 for col in range(len(self.users))] for row in range(len(self.users))]
#        #places=list((n for n in graph.nodes() if graph.node[n]['bipartite']==1))
#            
#        for user1 in self.users:
#            
#            X=dict.fromkeys(self.venues,0)
#            
#            for nb in nx.neighbors(self.user_venue_graph,user1):
#                #print user1, nb, graph.has_node(nb)
#                if self.user_venue_graph.has_node(nb):
#                    X[nb]+=self.user_venue_graph[user1][nb]['weight']
#                
#        
#            for user2 in self.users:
#                Y=dict.fromkeys(self.venues,0)
#                for nb in nx.neighbors(self.user_venue_graph,user2):
#                    if self.user_venue_graph.has_node(nb):
#                        Y[nb]+=self.user_venue_graph[user2][nb]['weight']        
#                
#                #print user1, user2
#                self.UserSimilarityMatrix[self.users.index(user1)][self.users.index(user2)] = 1-cosine(X.values(), Y.values())
#        
#        return self.UserSimilarityMatrix
#        
#    """
#    getUserSimilarity
#    
#    @author: doheum, yonghan
#    
#    @desc: This function fetches the similarity value of two different users and returns it.
#    
#    @input:
#    - UserSimilarityMatrix: the nested list of user similarity values
#    - userA: the target user A
#    - userB: the target user B
#    
#    @output:
#    - similarity: the similarity value of user A and B
#    """
#    def getUserSimilarity(self,userA,userB):
#        # code here    
#        similarity = self.UserSimilarityMatrix[self.users.index(userA)][self.users.index(userB)]
#        return similarity
#        
#    """
#    estimateUserVisitVector
#    
#    @author: doheum, seulkee
#    
#    @desc: This function estimates the visit vector of a user based on the collaborative filtering method.
#    
#    @input:
#    - graph: a graph with users and venues constructed by checkin data (read or constructed by networkx library)
#    - UserSimilarityMatrix: the nested list of user similarity values
#    - user: the user of which the visit vector is calculated
#    
#    @output:
#    - visit_vector: the estimated visit vector of a user (dictionary)
#    """
#    def estimateUserVisitVector(self,user):
#        visit_vector={}
#        
#        for p in self.venues:
#            c = 0
#            for u in self.users:
#                if self.user_venue_graph.has_edge(u,p) and not u==user:
#                    c += self.getUserSimilarity(user,u) * self.user_venue_graph[u][p]['weight']
#    
#            visit_vector[p]=float(c)/float(len(self.users))
#         
#        return visit_vector
#        
#    """
#    CollaboFilteringTopN
#    
#    @author: doheum
#    
#    @desc: This function returns the list of top N venues in the order of the estimated visit value
#    by estimateUserVisitVector.
#    
#    @input:
#    - graph: a graph with users and venues constructed by checkin data (read or constructed by networkx library)
#    - UserSimilarityMatrix: the nested list of user similarity values
#    - venues: the list of venues
#    - user: the target user for recommendation
#    - topN: the range of the ranks to fetch (ex: 1 - Top 1, 5 - Top 5)
#    
#    @output:
#    - collaboTopN: the list of Top N venues in the order of their estimated visit values
#    """
#    def CollaboFilteringTopN(self,user,topN):
#        # code here    
#        visit_vector=self.estimateUserVisitVector(user)  
#        
#        sorted_visit_vector=sorted(visit_vector.items(), key=lambda t: t[1],reverse=True)
#        #print sorted_visit_vector[0]
#        
#        collaboTopN=sorted_visit_vector[0:topN]
##        for p in sorted_visit_vector[0:topN]:
##            collaboTopN.append(p[0])
#        
#        return collaboTopN