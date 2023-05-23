class Graph:
    def __init__(self):
        self.adj_dict = {}
        
    def add_edge(self, v, u) :
        if v not in self.adj_dict:
            self.adj_dict[v] = {u:1}
        else:
            self.adj_dict[v][u] = 1
            
        if u not in self.adj_dict:
            self.adj_dict[u] = {v:1}
        else:
            self.adj_dict[u][v] = 1
        
    def adj(self, v):
        return self.adj_dict[v]
    
    def vertex(self, v):
        self.adj_list = self.adj_dict[v]
        self.deg = sum(list(map(int, self.adj_list.values())))
        self.vertex_num = 1
        
        return self.vertex_num, self.adj_list, self.deg
    
import sys
import time

edges_path = './dataset/soc-YouTube-ASU/soc-YouTube-ASU.edges' #sys.argv[1]
label_path = './dataset/soc-YouTube-ASU/soc-YouTube-ASU.node_labels' #sys.argv[2]
# k = 7 #sys.argv[3]
label_dict = {}
graph_sort = []
label_kind = []
superNode = {}
label_f = open(label_path, 'r')
while True:
    line = label_f.readline().replace('\n', '').strip()
    if not line:
        label_kind.append('0')
        break
    node = line.split(',')[0]
    label = line.split(',')[1]
    label_dict[node] = [label]
    label_kind.append(label)
label_f.close

label_kind = list(set(label_kind))

edge_f = open(edges_path, 'r')
gs = Graph()
while True:
    line = edge_f.readline().replace('\n', '').strip()
    if not line:
        break
    
    v = line.split(',')[0]
    u = line.split(',')[1]
    if v not in label_dict:
        label_dict[v] = ['0']
        
    if u not in label_dict:
        label_dict[u] = ['0']
    graph_sort.append([v,u])
    gs.add_edge(v,u)
edge_f.close

def Super_node_generator(v):
    num_v, adj_v, deg_v = gs.vertex(v)
    label_v = {}
    
    for l in label_kind:
        label_v[l] = 0

    if v in label_dict:
        for ld_v in label_dict[v]:
            label_v[ld_v] = label_v[ld_v] + 1
            
    Vi = [num_v, deg_v, adj_v, label_v]
    
    return Vi

def Super_node_similarity(v, Vi, u, Vj):

    ew_v = Vi[2][u]/Vi[1]
    ew_u = Vj[2][v]/Vj[1]
    n_max = max(Vi[0], Vj[0])
    d_max = max(Vi[1], Vj[1])

    lm_v = sum(list(map(int, Vi[3].values())))
    lm_u = sum(list(map(int, Vj[3].values())))
    dis_att = 0
    
    dis_st = (abs(Vi[0]-Vj[0])/n_max) + (abs(Vi[1]-Vj[1])/d_max) + abs((Vi[2][u]/Vi[1]) - (Vj[2][v]/Vj[1]))

    for vl in Vi[3]:
        dis_att += abs(Vi[3][vl]/lm_v - Vj[3][vl]/lm_u)/2

    dis = (dis_st + dis_att)/2
    sim = 1 - dis
    return sim

def Super_node_similarity2(v, Vi, u, Vj, n):
    
    ew_v = Vi[2][u]/Vi[1]
    
    if v not in Vj[2]:
        save_val = Vj[2][n]
        del Vj[2][n]
        Vj[2][v] = save_val
    
    ew_u = Vj[2][v]/Vj[1]
    n_max = max(Vi[0], Vj[0])
    d_max = max(Vi[1], Vj[1])

    lm_v = sum(list(map(int, Vi[3].values())))
    lm_u = sum(list(map(int, Vj[3].values())))
    dis_att = 0
    
    dis_st = (abs(Vi[0]-Vj[0])/n_max) + (abs(Vi[1]-Vj[1])/d_max) + abs((Vi[2][u]/Vi[1]) - (Vj[2][v]/Vj[1]))

    for vl in Vi[3]:
        dis_att += abs(Vi[3][vl]/lm_v - Vj[3][vl]/lm_u)/2

    dis = (dis_st + dis_att)/2
    sim = 1 - dis
    return sim

def Merged_super_node(v, u, Vi, Vj):
    num_v = Vi[0]+Vj[0]
    adj_v = {}
    label_v = {}
    for adj in Vi[2]:
        if adj == u:
            pass
        if adj in Vj[2]:
            adj_v[adj] = Vi[2][adj] + Vj[2][adj]
        else:
            adj_v[adj] = Vi[2][adj]
            
    for adj in Vj[2]:
        if adj == v:
            pass
        if adj not in Vi[2]:
            adj_v[adj] = Vj[2][adj]
    if v in adj_v:
        del adj_v[v]
        
    if u in adj_v:
        del adj_v[u]
    deg_v = sum(list(map(int, adj_v.values())))
    
    for lab in Vi[3]:
        if lab in Vj[3]:
            label_v[lab] = Vi[3][lab] + Vj[3][lab]
            
    nVi = [num_v, deg_v, adj_v, label_v]
    
    return nVi

for node in list(label_dict.keys()):
    superNode[node] = Super_node_generator(node)
    
sim_list = []

for v, u in graph_sort:
    sim_list.append([v, u, Super_node_similarity(v, superNode[v], u, superNode[u])]) #triple entry
   
sim_list.sort(reverse=True, key=lambda x:x[2])

print(len(sim_list))
while(True): #k
    v = sim_list[0][0]
    u = sim_list[0][1]
    s1 = time.time()
    if v in superNode and u in superNode:
        superNode[v] = Merged_super_node(v, u, superNode[v], superNode[u])
        del(superNode[u])
        del(sim_list[0])
        
        nei_e = list(superNode[v][2].keys())
        
        for sim_one in sim_list:
            if sim_one[0] == v or sim_one[0] == u or sim_one[1] == v or sim_one[1] == u:
                print(sim_one)
                sim_list.remove(sim_one) 
        
        for n in nei_e:
            sim_list.append([v, n, Super_node_similarity2(v, superNode[v], n, superNode[n], u)])

    else:
        del(sim_list[0])
        
    sim_list.sort(reverse=True, key=lambda x:x[2])
    
    sim_size = len(sim_list)
    e1 = time.time()
    d1 = e1-s1
    print(f'v: {v}, u: {u}, Size: {sim_size}, Time1: {d1}')
    
    if len(sim_list) <= 32:
        break

