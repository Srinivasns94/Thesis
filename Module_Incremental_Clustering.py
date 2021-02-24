# -*- coding: utf-8 -*-
"""KG_PeiLee

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RaJfxUB8efgNWIxXutgUJzTPcGs0g5k4
"""

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import csv
import requests
import tqdm
import math
import json
import sys, setuptools, tokenize

from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from itertools import permutations 
from scipy.optimize import linear_sum_assignment
from collections import OrderedDict

def read_from_path(node_path, edge_path):
  node_df = pd.read_csv(node_path, sep=";")
  edge_df = pd.read_csv(edge_path, sep=";")
  return node_df, edge_df

def read_Gt_graph (node_df, edge_df, window_length, start_date):
  end_date = start_date +  relativedelta(months =+ window_length*3)
  end_time = math.ceil(end_date.month/window_length)

  nodes_cloumns = ['Occurance', 'Node', 'Time', 'Country']
  edges_columns = ['Coccurance', 'Node1', 'Node2', 'Time', 'Country']
  node_array = node_df.to_numpy()
  edge_array = edge_df.to_numpy()
  nodes = []
  edges = []

  for row in node_array:
    given_date = datetime.strptime(row[2].strip()[0:10], '%Y-%m-%d')
    time = math.ceil(given_date.month/window_length)
    if start_date <= given_date < end_date:
      nodes.append([row[0], row[1], time, row[3]])
  for row in edge_array:
    given_date = datetime.strptime(row[3].strip()[0:10], '%Y-%m-%d')
    time = math.ceil(given_date.month/window_length)
    if start_date <= given_date < end_date:
      edges.append([row[0], row[1], row[2], time, row[4]])
  G = read_graph(nodes, edges)
  return G, end_time

def read_Gt1_graph (node_df, edge_df, window_length, start_date):
  end_date = start_date +  relativedelta(months =+ window_length*4)
  end_time = math.ceil(end_date.month/window_length)

  nodes_cloumns = ['Occurance', 'Node', 'Time', 'Country']
  edges_columns = ['Coccurance', 'Node1', 'Node2', 'Time', 'Country']
  node_array = node_df.to_numpy()
  edge_array = edge_df.to_numpy()
  nodes = []
  edges = []

  for row in node_array:
    given_date = datetime.strptime(row[2].strip()[0:10], '%Y-%m-%d')
    time = math.ceil(given_date.month/window_length)
    if start_date <= given_date < end_date:
      nodes.append([row[0], row[1], time, row[3]])
  for row in edge_array:
    given_date = datetime.strptime(row[3].strip()[0:10], '%Y-%m-%d')
    time = math.ceil(given_date.month/window_length)
    if start_date <= given_date < end_date:
      edges.append([row[0], row[1], row[2], time, row[4]])
  G = read_graph(nodes, edges)
  return G, end_time

def get_G_old (node_df, edge_df, window_length, start_date):
  end_date = start_date +  relativedelta(months =+ window_length*1)
  end_time = math.ceil(end_date.month/window_length)

  nodes_cloumns = ['Occurance', 'Node', 'Time', 'Country']
  edges_columns = ['Coccurance', 'Node1', 'Node2', 'Time', 'Country']
  node_array = node_df.to_numpy()
  edge_array = edge_df.to_numpy()
  nodes = []
  edges = []

  for row in node_array:
    given_date = datetime.strptime(row[2].strip()[0:10], '%Y-%m-%d')
    time = math.ceil(given_date.month/window_length)
    if start_date <= given_date < end_date:
      nodes.append([row[0], row[1], time, row[3]])
  for row in edge_array:
    given_date = datetime.strptime(row[3].strip()[0:10], '%Y-%m-%d')
    time = math.ceil(given_date.month/window_length)
    if start_date <= given_date < end_date:
      edges.append([row[0], row[1], row[2], time, row[4]])
  G = read_graph(nodes, edges)
  return G, end_time

def get_G_new (node_df, edge_df, window_length, start_date):
  start_date = start_date +  relativedelta(months =+ window_length*3)
  end_date = start_date +  relativedelta(months =+ window_length*1)
  end_time = math.ceil(end_date.month/1)

  nodes_cloumns = ['Occurance', 'Node', 'Time', 'Country']
  edges_columns = ['Coccurance', 'Node1', 'Node2', 'Time', 'Country']
  node_array = node_df.to_numpy()
  edge_array = edge_df.to_numpy()
  nodes = []
  edges = []

  for row in node_array:
    given_date = datetime.strptime(row[2].strip()[0:10], '%Y-%m-%d')
    time = math.ceil(given_date.month/window_length)
    if start_date <= given_date < end_date:
      nodes.append([row[0], row[1], time, row[3]])
  for row in edge_array:
    given_date = datetime.strptime(row[3].strip()[0:10], '%Y-%m-%d')
    time = math.ceil(given_date.month/window_length)
    if start_date <= given_date < end_date:
      edges.append([row[0], row[1], row[2], time, row[4]])
  G = read_graph(nodes, edges)
  return G, end_time

def read_graph (nodes, edges):
  G = nx.Graph()
  for row in nodes:
    if G.has_node(row[1]):
      G.nodes[row[1]]['attr_dict']['occurance'] = G.nodes[row[1]]['attr_dict']['occurance'] + row[0]
    else:
      G.add_node(row[1], attr_dict = {'time':row[2], 'country':row[3], 'occurance':row[0]})

  for row in edges:
    if G.has_edge(row[1], row[2]):
      G.edges[row[1], row[2]]['attr_dict']['Coccurance'] = G.edges[row[1], row[2]]['attr_dict']['Coccurance'] + row[0]
    else:
      G.add_edge(row[1], row[2], attr_dict = {'Coccurance':row[0]})
  return G

def generate_post_graph (G):
  post_graph = nx.Graph()
  for n1 in G.nodes():
    for n2 in G.nodes(): 
      o1 = G.nodes[n1]['attr_dict']['occurance']
      o2 = G.nodes[n2]['attr_dict']['occurance']
      t1 = G.nodes[n1]['attr_dict']['time']
      t2 = G.nodes[n2]['attr_dict']['time']
      data = G.get_edge_data(n1,n2)
      if data is not None:
        co = data['attr_dict']['Coccurance']
        fading_similarity = (co*co)/((o1*o2) * abs(math.exp(abs(t1-t2))))
        #print(n1,n2, o1, o2, co, fading_similarity, t1, t2)
        if fading_similarity > 0.15 :
          post_graph.add_node(n1, attr_dict = {'time':G.nodes[n1]['attr_dict']['time'], 
                                                'country':G.nodes[n1]['attr_dict']['country'], 
                                                'occurance':G.nodes[n1]['attr_dict']['occurance']})
          post_graph.add_node(n2, attr_dict = {'time':G.nodes[n2]['attr_dict']['time'], 
                                                'country':G.nodes[n2]['attr_dict']['country'], 
                                                'occurance':G.nodes[n2]['attr_dict']['occurance']})
          post_graph.add_edge(n1, n2, attr_dict={'similarity': fading_similarity})
  return post_graph

def calculate_sum(post_graph, t):
  #cluster_df = trim_skill_names_map(post_graph)
  for n in post_graph.nodes():
    result = 0
    neighborset = []
    for neighbor in post_graph.neighbors(n):
      attributes = post_graph.get_edge_data(n,neighbor)
      weight_from_kg = get_weight_from_KG(n, neighbor)
      result = result + attributes['attr_dict']['similarity'] + weight_from_kg
      neighborset.append(neighbor)
      #print(n,neighbor,result)
    time_n = post_graph.nodes[n]['attr_dict']['time']
    weight = result/(math.exp(abs(t - time_n)))
    #print(n, result, len(neighborset), weight)
    post_graph.nodes[n]['attr_dict']['sum'] = result
    post_graph.nodes[n]['attr_dict']['weight'] = weight
  return post_graph

def generate_skeletal_graph (post_graph):
  skeletal_graph = nx.Graph()
  for core in post_graph.nodes():
    #print(core, post_graph.nodes[core]['attr_dict']['weight'])
    if post_graph.nodes[core]['attr_dict']['weight'] >= 0.3:
      skeletal_graph.add_node(core, attr_dict = {'time':post_graph.nodes[core]['attr_dict']['time'], 
                                                  'country':post_graph.nodes[core]['attr_dict']['country'], 
                                                  'priority':post_graph.nodes[core]['attr_dict']['weight']})
      post_graph.nodes[core]['attr_dict']['core'] = 1
    else :
      post_graph.nodes[core]['attr_dict']['core'] = 0

  for border in post_graph.nodes():
    if post_graph.nodes[border]['attr_dict']['weight'] <  0.3:
      for neighbor in post_graph.neighbors(border):
        if skeletal_graph.has_node(neighbor):
          post_graph.nodes[border]['attr_dict']['border'] = 1
          break
        else :
          post_graph.nodes[border]['attr_dict']['border'] = 0
    else:
      post_graph.nodes[border]['attr_dict']['border'] = 0
      post_graph.nodes[border]['attr_dict']['noise'] = 1
  return post_graph , skeletal_graph

def get_clusters_new (skeletal_graph, post_graph):
  s = {}
  for n in skeletal_graph.nodes():
    cluster_graph = nx.Graph()
    cluster_graph.add_node(n, attr_dict = {'time':post_graph.nodes[n]['attr_dict']['time'], 
                                            'priority':post_graph.nodes[n]['attr_dict']['weight']})
    for border in post_graph.neighbors(n):
      cluster_graph.add_node(border, attr_dict = {'time':post_graph.nodes[border]['attr_dict']['time'], 
                                              'priority':post_graph.nodes[border]['attr_dict']['weight']})
      cluster_graph.add_edge(n, border)
    s[n] = cluster_graph
  return s

def get_time_window_clusters(s):
  s_old = {}
  s_t = {}
  s_new = {}
  for key, value in s.items():
    if post_graph.nodes[key]['attr_dict']['time'] == 1:
      s_old[key] = value
    elif post_graph.nodes[key]['attr_dict']['time'] == 2:
      s_t[key] = value
    else:
      s_new[key] = value
  return s_old, s_t, s_new

def graph_minus (G1, G2):
  for key in list(G2.nodes().keys()):
    if G1.has_node(key):
      G1.remove_node(key)
  return G1

def graph_minus_recalc (G1, G2, end_date):
  G = nx.Graph()
  for key in list(G2.nodes().keys()):
    if G1.has_node(key):
      G1.remove_node(key)
  #print(G1.number_of_nodes())
  G = calculate_sum (G1, end_date)
  return G

def calculate_s_plus (G_t1, G_new, end_date):
  G1 = nx.Graph()
  G2 = nx.Graph()

  G1 = graph_minus (G_t1, G_new)
  G2 = graph_minus_recalc (G_t1, G_new, end_date)
  #return G1 , G2
  get_s_plus_clusters(G1, G2)

def get_s_plus_clusters (G1, G2):
  s_plus_graph = nx.Graph()
  skeltal_s_plus = nx.Graph()
  s_plus = {}

  s_plus_graph = graph_minus(G1, G2)
  s_plus_graph , skeltal_s_plus = generate_skeletal_graph (s_plus_graph)
  s_plus = get_clusters (s_plus_graph)

  return s_plus

def calculate_s_minus (G_t, G_old, end_date):
  G1 = nx.Graph()
  G2 = nx.Graph()
  s_minus_graph = nx.Graph()
  skeletal_s_minus = nx.Graph()
  s_minus = {}

  G1 = graph_minus (G_t, G_old)
  G2 = graph_minus_recalc (G_t, G_old, end_date)
  #return G1, G2
  get_s_minus_clusters(G1, G2)

def get_s_minus_clusters (G1, G2):
  s_minus_graph = nx.Graph()
  skeletal_s_minus = nx.Graph()
  s_minus = {}
  s_minus_graph = graph_minus (G1, G2)
  s_minus_graph , skeletal_s_minus = generate_skeletal_graph (s_minus_graph)
  s_minus = get_clusters (s_minus_graph)

  return s_minus

def calculate_s_dot (G_t, G_old, G_t1, G_new, end_date):
  G1 = nx.Graph()
  G2 = nx.Graph()

  G1 = graph_minus_recalc (G_t, G_old, end_date)
  G2 = graph_minus_recalc (G_t1, G_new, end_date)
  #return G1, G2
  get_s_dot_clusters(G1, G2)

def get_s_dot_clusters (G1, G2):
  s_dot_graph = nx.Graph()
  skeletal_s_dot = nx.Graph()
  s_dot = {}
  s_dot_graph = graph_minus (G1, G2)
  s_dot_graph , skeletal_s_dot = generate_skeletal_graph (s_dot_graph)
  s_dot = get_clusters (s_dot_graph)

  return s_dot

def get_neighbour_clusters(head, cluster, post_graph):
  Nc = {}
  N_cluster = {}
  for n in cluster.nodes():
    count = 0 
    neighbor_cluster = {}
    nodes = []
    if post_graph.has_node(n):
      #print('illi')
      for node in post_graph.neighbors(n):
        #print(node)
        if post_graph.nodes[n]['attr_dict']['core'] == 1 :
          count = count + 1
          nodes.append(node)
      #neighbor_cluster['count'] = count
    Nc[n] = count
    N_cluster[n] =nodes
    #print(N_cluster)
  return Nc, N_cluster

def incremental_cluster (s_t, s_old, s_new, s_minus, s_plus, s_dot, post_graph):
  s_t1 = {}
  s_t1.update(s_t)
  #number_of_clusters = len(s_old) + len(s_minus) + len(s_dot)
  union_minus = {}
  if s_minus is None and s_dot is None:
    union_minus = {**s_old}
  elif s_minus is None:
    union_minus = {**s_old, **s_dot}
  elif s_dot is None:
    union_minus = {**s_old, **s_minus}
  else :
    union_minus = {**s_old, **s_minus, **s_dot}
  for head, cluster in union_minus.items():
    Nc, N_cluster =  get_neighbour_clusters(head, cluster, post_graph)
    if Nc[head] == 0:
      if head in s_t1.keys():
        s_t1.pop(head)  
    #elif Nc[head] <= 2:
      #N_cluster[head].remove(head)
     # s_t1.pop(head)
    else:
      if head in s_t1.keys():
        s_t1.pop(head)
      for h, lists in N_cluster.items():
        for core in lists:
          if core in s_old.keys() and h in s_old.keys():
            s_t1[h] = nx.compose(union_minus[h], union_minus[core]) 
  union_add = {}
  if s_plus is None:
    union_add = {**s_new}
  else :
    union_add = {**s_new, **s_plus}
  for head, cluster in union_add.items():
    Nc, N_clusters =  get_neighbour_clusters(head, cluster, post_graph)
    if Nc[head] == 0:
      s_t1[head] = cluster
    elif Nc[head] == 1:
      if str(N_clusters[head]) in union_add.keys():
        s_t1[head] = nx.compose(union_add[head], cluster)
    else:
      for h, lists in N_clusters.items():
        for core in lists:
          if core in union_add.keys():
            s_t1[h] = nx.compose(union_add[h], union_add[core])
          if core in s_t1.keys():
            s_t1.pop(core)
  return s_t1

def process_s_t1 (s_t1):
  s_t2 = {}
  s_t2.update(s_t1)
  for head, cluster in s_t2.items():
    if cluster.number_of_nodes() <= 3 :
      s_t1.pop(head)
  return s_t1

def pre_processing (G_old, G_t, G_new, G_t1):
  post_graph_t = nx.Graph()
  post_graph_old = nx.Graph()
  post_graph_new = nx.Graph()
  post_graph_t1 = nx.Graph()

  post_graph_t = generate_post_graph(G_t)
  post_graph_t = calculate_sum(post_graph_t, end_date_t)
  post_graph_t, skeletal_graph_t = generate_skeletal_graph(post_graph_t)
  #print(skeletal_graph_t.number_of_nodes())

  post_graph_old = generate_post_graph(G_old)
  post_graph_old = calculate_sum(post_graph_old, end_date_old)
  post_graph_old, skeletal_graph_old = generate_skeletal_graph(post_graph_old)
  #print(skeletal_graph_old.number_of_nodes())

  post_graph_new = generate_post_graph(G_new)
  post_graph_new = calculate_sum(post_graph_new, end_date_new)
  post_graph_new, skeletal_graph_new = generate_skeletal_graph(post_graph_new)

  post_graph_t1 = generate_post_graph(G_t1)
  post_graph_t1 = calculate_sum(post_graph_t1, end_date_t1)
  post_graph_t1, skeletal_graph_t1 = generate_skeletal_graph(post_graph_t1)
  #print(skeletal_graph_t1.number_of_nodes())
  print('Skeletal Graph generated')
  return post_graph_old, post_graph_t, post_graph_new, post_graph_t1, skeletal_graph_t, skeletal_graph_old, skeletal_graph_new, skeletal_graph_t1

#NEW!!!
def post_graph_processing_new (post_graph_old, post_graph_t, post_graph_new, post_graph_t1, skeletal_graph_old, skeletal_graph_t, skeletal_graph_new, skeletal_graph_t1):
  s_old = {}
  s_t = {}
  s_new = {}
  s_plus = {}
  s_minus = {}
  s_dot = {}

  s_t = get_clusters_new(skeletal_graph_t,post_graph_t)
  s_old = get_clusters_new(skeletal_graph_old, post_graph_old)
  s_new = get_clusters_new(skeletal_graph_new, post_graph_new)

  #s_plus = calculate_s_plus(post_graph_t1, post_graph_new, end_date_t)
  #s_minus = calculate_s_minus (post_graph_t, post_graph_old,end_date_t)
  #s_dot = calculate_s_dot (post_graph_t, post_graph_old, post_graph_t1, post_graph_new, end_date_t)

  return s_old, s_t, s_new, s_plus, s_minus, s_dot

def eTrack(G_old, G_t, G_new, G_t1):
  post_graph_old, post_graph_t, post_graph_new, post_graph_t1, skeletal_graph_t, skeletal_graph_old, skeletal_graph_new, skeletal_graph_t1 = pre_processing(G_old, G_t, G_new, G_t1)
  post_graph_t1_bk = post_graph_t1
  s_old, s_t, s_new, s_plus, s_minus, s_dot = post_graph_processing_new(post_graph_old, post_graph_t, post_graph_new, post_graph_t1, skeletal_graph_old, skeletal_graph_t, skeletal_graph_new, skeletal_graph_t1)
  
  if post_graph_t1_bk.number_of_nodes == 0:
    post_graph_t1 = generate_post_graph(G_t1)
    post_graph_t1 = calculate_sum(post_graph_t1, end_date_t1)
    post_graph_t1, skeletal_graph_t1 = generate_skeletal_graph(post_graph_t1)

  #Calling ICM
  print('Calling Evolutionary Clustering Algorithm')
  s_t1 = incremental_cluster(s_t, s_old, s_new, s_minus, s_plus, s_dot, post_graph_t1_bk)
  print(s_t1)
  #Tracking the Evolution of Clusters
  return s_t1

def process_clusters(s_t1):
  s_t1_bk = {}
  s_t1_bk.update(s_t1)
  print(len(s_t1_bk))
  for head, cluster in s_t1.items():
    for h, c in s_t1.items():
      if head != h:
        intersection_set = set(c.nodes()).intersection(set(cluster.nodes()))
        #print(intersection_set)
        if intersection_set == set(c.nodes()):
          if h in s_t1_bk.keys():
            s_t1_bk.pop(head)
            break
  print(len(s_t1_bk))
  return s_t1_bk

def get_weight_from_KG(n, neighbor):
  n = n[n.rfind('/')+1:]
  neighbor = neighbor[neighbor.rfind('/')+1:]
  skills = map_skills([n, neighbor])
  clusterPeiLee1 = []
  clusterPeiLee2 = []
  clusterPeiLee1.append(skills[0].strip())
  clusterPeiLee2.append(skills[1].strip())
  print(skills[0]+ ' & '+skills[1])
  similarity = calculate_similarity(clusterPeiLee1, clusterPeiLee2, skills[0], skills[1])
  #similarity = calculate_similarity(cluster_df, cluster_df, skills[0], skills[1])
  print(similarity)
  return similarity

def normalize_names(node):
  node = node.capitalize().strip()

  if node.find('-') != -1:
    node = node[0:node.find('-')] + '_'+ node[node.find('-')+1:]
  if node == 'Jquery':
    node = 'JQuery'
  if node == 'Xhtml':
    node = 'XHTML'
  if node == 'Php':
    node = 'PHP'
  if node == 'Angularjs':
    node = 'AngularJS'
  if node == 'Html5':
    node = 'HTML5'
  return node

def calculate_similarity(cluster1, cluster2, skill1, skill2):
  cluster1_df = getDbpediaTriplesOfCluster(cluster1)
  cluster2_df = getDbpediaTriplesOfCluster(cluster2)
  first_sim_score = firstRuleOfSimilarity(skill1, skill2, cluster1_df, cluster2_df)
  second_sim_score = secondRuleOfSimilarity(skill1, skill2, cluster1_df, cluster2_df)
  third_sim_score = thirdRuleOfSimilarity(skill1, skill2, cluster1_df, cluster2_df)
  total_sim_score = float("{:.4f}".format((first_sim_score + second_sim_score + third_sim_score)))
  return total_sim_score

def trim_skill_names_map(skill_graph):
  node_list = []
  for node in skill_graph.nodes():
    n = node[node.rfind('/')+1:]
    node_list.append(n)
  cluster_skills = map_skills(node_list)
  cluster_df = getDbpediaTriplesOfCluster(cluster_skills)
  return cluster_df

def map_skills(skills_to_be_mapped):
# skills_to_be_mapped = ['mysql','oracle','postgresql','database']
  cluster = []
  for skill in skills_to_be_mapped:
    link = annotate_with_Dbpedia_spotlight(skill, 0.5)
    if link == 0:
      confidence = 0.4
      while confidence >= 0:
        link = annotate_with_Dbpedia_spotlight(skill, confidence)
        confidence = confidence - 0.1
    if link == 0:
      skill = normalize_names(skill)
      link = 'http://dbpedia.org/resource/'+skill
    cluster.append(link)
  return cluster


def annotate_with_Dbpedia_spotlight(text, confidence):
  # text preprocessing
  text = text.replace("_", " ").replace("-", " ")
  URL = "https://api.dbpedia-spotlight.org/en/annotate?text=" + text + "&confidence=" + str(confidence) + ""
  HEADERS = {'Accept': 'application/json'}
  response = requests.get(URL, headers=HEADERS)
  if response.status_code != 200:
    return 0
  
  json_obj = response.json()
  if "Resources" in json_obj:
    return json_obj["Resources"][0]['@URI']
  else:
    return 0

def getTriples(A): 
  url = 'http://dbpedia.org/sparql/'
  query = """
  SELECT *
  WHERE
  {
    {
    <""" + A + """>  ?r1 ?n2 .
    }
  }
  """
  r = requests.get(url, params = {'format': 'json', 'query': query})
  data = r.json()

  subgraph = []
  for item in data['results']['bindings']:
      if item['n2']['value'].startswith('http://dbpedia.org'):
        subgraph.append(OrderedDict({
          'source_node': A, 
          'r1': item['r1']['value'],
          'target_node': item['n2']['value']
        }))

  df = pd.DataFrame(subgraph)
  return df

def getConnectingRelation(node):
  url = 'http://dbpedia.org/sparql/'
  query = """
  SELECT *
  WHERE
  {
    {
    <""" + node + """>  ?r1 ?n2 .
    }
  }
  """
  r = requests.get(url, params = {'format': 'json', 'query': query})
  data = r.json()

  relations = []
  for item in data['results']['bindings']:
    relations.append(item['r1']['value'])

  relations = list(set(relations))
  return relations

def getDbpediaTriplesOfCluster(cluster):
  frames = []
  for item in cluster:
    df = getTriples(item)
    frames.append(df)
  result = pd.concat(frames)
  result = result.drop_duplicates()
  return result

def firstRuleOfSimilarity(s1, s2, s1_triples, s2_triples):
  # If two distinct subjects share the same predicate, and for that predicate the same object, then both are given weight as 'similar'
  df1 = s1_triples.query("source_node == '" + s1 + "'")
  df2 = s2_triples.query("source_node == '" + s2 + "'")
  score = 0
  # find common items in df1 and df2
  df = df1.merge(df2, how = 'inner' ,indicator=False)
  
  if not df.empty:
    unique_predicates = list(df.r1.unique())
    for pred in unique_predicates:
      common_rows = df.query("r1 == '" + pred + "'").shape[0]
      df1_pred_rows = df1.query("r1 == '" + pred + "'").shape[0]
      df2_pred_rows = df2.query("r1 == '" + pred + "'").shape[0]
      score = score + (common_rows / (df1_pred_rows + df2_pred_rows - common_rows))
  return score

def secondRuleOfSimilarity(s1, s2, s1_triples, s2_triples):
  # If two distinct subjects have similar direct neighbor nodes, 
  # then they are considered similar (for this we can give a threshold for the number of direct neighbor nodes that are similar)
  node_list1 = s1_triples.query("source_node == '" + s1 + "'")["target_node"].tolist()
  node_list2 = s2_triples.query("source_node == '" + s2 + "'")["target_node"].tolist()
  node_set1 = set(node_list1)
  common_items = list(node_set1.intersection(node_list2))
  if len(common_items) > 0:
    result = len(common_items) / (len(node_list1) + len(node_list2) - len(common_items))
    return result
  else:
    return 0

def thirdRuleOfSimilarity(s1, s2, s1_triples, s2_triples):
  excluded_predicates_list = ['http://www.w3.org/1999/02/22-rdf-syntax-ns#type']
  relation_list1 = s1_triples.query("source_node == '" + s1 + "'")["r1"].tolist()
  relation_list2 = s2_triples.query("source_node == '" + s2 + "'")["r1"].tolist()
  relation_set1 = set(relation_list1)
  common_relations = list(relation_set1.intersection(relation_list2))
  common_relations = list(set(common_relations) - set(excluded_predicates_list))
  # print(common_relations)
  if len(common_relations) > 0:
    result = len(common_relations) / (len(relation_list1) + len(relation_list2) - len(common_relations))
    return result
  else:
   return 0

#Main
start_time = time.time()
window_length = 3 # 1,2 or 3 as discussed
total_data = 24 #Give in Months
start = '2016-01-01' 
increment_cluster = {}
increment_cluster_old = {}
for i in range(int(total_data/window_length)-3):
  start_date = datetime.strptime(start.strip(), '%Y-%m-%d')
  start_date = start_date +  relativedelta(months =+ window_length*i)
  print('Iteration: '+str(i))
  #countries = ['at', 'be', 'ch', 'cz', 'de', 'dk', 'es', 'fr', 'gb', 'hu', 'ie', 'it', 'nl', 'pl', 'pt', 'ro', 'se']
  countries = ['de']
  for country in countries:
    G_t = nx.Graph()
    G_old = nx.Graph()
    G_new = nx.Graph()
    G_t1 = nx.Graph()
    nodes_path = '/content/drive/My Drive/dataset/PeiLee/nodes_'+country+'.csv'
    edges_path = '/content/drive/My Drive/dataset/PeiLee/'+country+'.csv'
    node_df , edge_df = read_from_path(nodes_path, edges_path)
    G_t, end_date_t = read_Gt_graph(node_df, edge_df, window_length, start_date)
    G_old, end_date_old = get_G_old(node_df, edge_df, window_length, start_date)
    G_new, end_date_new = get_G_new(node_df, edge_df, window_length, start_date)
    G_t1, end_date_t1 = read_Gt1_graph(node_df, edge_df, window_length, start_date)
    print('Reading of Graphs Completed')
    s_t1 = eTrack(G_old, G_t, G_new, G_t1)
    s_t1_new = process_clusters(s_t1)
    increment_cluster[i] = s_t1_new
    increment_cluster_old[i] = s_t1
end_time = time.time()
print(end_time - start_time)
print(increment_cluster)
np.save('/content/drive/My Drive/Thesis/output_peiLee_3w15fthresholdDe3_24_KG_new.npy', increment_cluster)