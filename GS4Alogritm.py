def Super_node_generator(v):
    num_v, adj_v, deg_v = gs.vertex(v)
    label_v = {}
    
    for l in label_kind:
        label_v[l] = 0
        
    if v in label_dict:
        for ld_v in label_v:
            if ld_v == label_dict[v]:
                label_v[ld_v] = 1

    superNode[v] = [num_v, deg_v, adj_v, label_v]
    
    return superNode[v]

def Super_node_similarity(v, u, n):
    ew_v = superNode[v][2][u]/superNode[v][1]

    if n != 'None' and (v not in superNode[u][2] or n in superNode[u][2]):
        save_val = superNode[u][2][n]
        del superNode[u][2][n]
        superNode[u][2][v] = save_val
    
    ew_u = superNode[u][2][v]/superNode[u][1]
    n_max = max(superNode[v][0], superNode[u][0])
    d_max = max(superNode[v][1], superNode[u][1])

    lm_v = sum(list(map(int, superNode[v][3].values())))
    lm_u = sum(list(map(int, superNode[u][3].values())))
    dis_att = 0
    
    dis_st = ((abs(superNode[v][0]-superNode[u][0])/n_max) + (abs(superNode[v][1]-superNode[u][1])/d_max) + abs(ew_v - ew_u))/3

    for vl in superNode[v][3]:
        dis_att += abs(superNode[v][3][vl]/lm_v - superNode[u][3][vl]/lm_u)/2

    dis = (dis_st + dis_att)/2
    sim = 1 - dis
    return sim

def Merged_super_node(v, u):
    num_v = superNode[v][0] + superNode[u][0]
    adj_v = {}
    label_v = {}
    for adj in superNode[v][2]:
        if adj == u:
            continue
        if adj in superNode[u][2]:
            adj_v[adj] = superNode[v][2][adj] + superNode[u][2][adj]
        else:
            adj_v[adj] = superNode[v][2][adj]
            
    for adj in superNode[u][2]:
        if adj == v:
            continue
        if adj not in superNode[v][2]:
            adj_v[adj] = superNode[u][2][adj]
            
    if v in adj_v:
        del adj_v[v]
        
    if u in adj_v:
        del adj_v[u]
        
    deg_v = sum(list(map(int, adj_v.values())))
    
    for lab in superNode[v][3]:
        if lab in superNode[u][3]:
            label_v[lab] = superNode[v][3][lab] + superNode[u][3][lab]
            
    superNode[v] = [num_v, deg_v, adj_v, label_v]
    del(superNode[u])

        
class Graph:
    def __init__(self):
        self.adj_dict = {}
        self.node_dict = {}
        self.edge_list = []
        
    def add_edge(self, v, u, pattern):
        if v not in self.adj_dict:
            self.adj_dict[v] = {u:pattern}
        else:
            self.adj_dict[v][u] = pattern
            
        if u not in self.adj_dict:
            self.adj_dict[u] = {v:pattern}
        else:
            self.adj_dict[u][v] = pattern
            
        if v not in self.node_dict:
            self.node_dict[v] = v
            
        if u not in self.node_dict:
            self.node_dict[u] = u
        
        self.edge_list.append([v,u])
        
    def del_edge(self, v, u):
        if u in self.adj_dict[v]:
            del(self.adj_dict[v][u])
            
        if v in self.adj_dict[u]:
            del(self.adj_dict[u][v])
            
    def del_uedge(self, v, u):
        if v in self.adj_dict[u]:
            del(self.adj_dict[u][v])
            
    def edge_l(self):
        return self.edge_list
        
    def adj_d(self, v):
        return self.adj_dict[v]
    
    def vertex(self, v):
        if v not in self.adj_dict:
            return 0, 0, {}
        self.adj_list = self.adj_dict[v]
        self.deg = len(self.adj_dict[v])
        self.vertex_num = 1
        
        return self.vertex_num, self.deg, self.adj_list