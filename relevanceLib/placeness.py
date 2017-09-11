# -*- coding: utf-8 -*-

import networkx as nx
import os.path

class placeness:
    graph=None
    
    def __init__(self):    
        return
                    
    def load_graph(self,fname=None,gname=None):
        #print self._json
        if gname:
            self.graph=nx.read_gexf(gname)
        else:
            if fname:
                # graph init
                self.graph=nx.Graph()            
                
                f=open(fname)
                
                while 1:
                    line=f.readline()
                    if not line:
                        break
                    
                    venue=line.rstrip().split('\t')[0]
                    placeness=line.rstrip().split('\t')[1].decode('utf-8')
                    #print placeness
                    user='u'+line.rstrip().split('\t')[2]
                    
                    if not self.graph.has_node(venue):
                        self.graph.add_node(venue,bipartite='venue')                
                    if not self.graph.has_node(placeness):
                        self.graph.add_node(placeness,bipartite='pl')
                    if not self.graph.has_node(user):
                        self.graph.add_node(user,bipartite='user')
                    
                    if not self.graph.has_edge(venue,placeness):
                        self.graph.add_edge(venue,placeness,weight=1)
                    else:
                        self.graph[venue][placeness]['weight']+=1
                    
                    if not self.graph.has_edge(placeness,user):
                        self.graph.add_edge(placeness,user,weight=1)
                    else:
                        self.graph[placeness][user]['weight']+=1
            else:
                print('Specify a file to load a graph')        
        return    
    
    def write_graph(self,fname):
        if self.graph:
            print('Writing the graph into a file')
            nx.write_gexf(self.graph,fname)
            print('Done')
        else:
            print('load graph file first')
    
    def get_nodes_by_type(self, t, g=None):
        nodes=None
        
        if self.graph:
            nodes=list((n for n in self.graph.nodes() if self.graph.node[n]['bipartite']==t))
        else:
            print('load graph file first')
            
        return nodes

# sample code of using placeness class

def function_tests():
    #load json file into class
    fname='../data/placeness_by_post.tsv'
    gname='../gexf/user_placeness_venue.gexf'
    
    P=placeness()    
    
    if os.path.isfile(gname):
        P.load_graph(gname=gname)
    else:
        P.load_graph(fname=fname)
        P.write_graph(gname)
        
    print('The number of venue nodes: ', len(P.get_nodes_by_type('venue')))
    print('The number of placeness nodes: ', len(P.get_nodes_by_type('pl')))
    print('The number of user nodes: ', len(P.get_nodes_by_type('user')))