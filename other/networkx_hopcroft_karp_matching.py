from collections import OrderedDict
import json
import networkx as nx

nodes_y = list(range(18))
nodes_x = [str(y) for y in nodes_y]
connections = {"0":[12],"1":[0,2,12],"2":[0,4],"3":[2,4],"4":[2,11],"5":[2,4],"6":[8,9,2,4,10],"7":[16,9,6],"8":[9],"9":[17,10],"10":[0,1,2,11,13,14],"11":[10],"12":[6],"13":[12],"14":[13,15],"15":[10],"16":[15],"17":[15]}

edges = list()
for node in connections:
  for connection in connections[node]:
    edges.append((node,connection))

nodes_x_b = [x for x,_ in edges if x in nodes_x]
nodes_y_b  = [y for _,y in edges if y in nodes_y]

B = nx.Graph()
B.add_nodes_from(nodes_x_b, bipartite=0)
B.add_nodes_from(nodes_y_b, bipartite=1)
B.add_edges_from(edges)
result = nx.bipartite.hopcroft_karp_matching(B)

cleaned_result = {x:y for x,y in result.items() if isinstance(x,str)}

print(json.dumps(OrderedDict(sorted(cleaned_result.items(), key=lambda t: t[0]))))