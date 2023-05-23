class saveGraph:
    def __init__(self, edges_path, label_path, Separator):
        self.label_dict = {}
        self.label_kind = []
        self.nodeList = []
        self.pt_fq = {}
        self.gs = Graph()

        label_f = open(label_path, 'r')
        while True:
            line = label_f.readline().replace('\n', Separator).strip()
            if not line:
                break
            
            node = line.split(Separator)[0]
            label = line.split(Separator)[1]

            self.label_dict[str(node)] = label
            self.label_kind.append(label)

        label_f.close

        self.label_kind = list(set(self.label_kind))
        
        edge_f = open(edges_path, 'r')
        while True:
            line = edge_f.readline().replace('\n', '').strip()
            if not line:
                break
            
            v = line.split(',')[0]
            u = line.split(',')[1]
            
            if v == u:
                continue
            
            if v not in self.label_dict:
                self.label_dict[v] = '0'
                
            if u not in self.label_dict:
                self.label_dict[u] = '0'
            
            self.nodeList.append(v)
            self.nodeList.append(u)

            pt = self.label_dict[v] + '/' + self.label_dict[u]
            
            re_pt = ''.join(reversed(pt))
            
            if pt not in self.pt_fq and re_pt not in self.pt_fq:
                self.pt_fq[pt] = 1
                self.gs.add_edge(v,u,pt)
                
            elif re_pt in self.pt_fq:
                self.pt_fq[re_pt] = self.pt_fq[re_pt] + 1
                self.gs.add_edge(v,u,re_pt)
                
            elif pt in self.pt_fq:
                self.pt_fq[pt] = self.pt_fq[pt] + 1
                self.gs.add_edge(v,u,pt)

        edge_f.close
        self.nodeList = list(set(self.nodeList))
        
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
        self.adj_list = self.adj_dict[v]
        self.deg = len(self.adj_dict[v])
        self.vertex_num = 1
        
        return self.vertex_num, self.deg, self.adj_list