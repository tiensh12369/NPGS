class Graphdata:
    def __init__(self, IGPath, lbPath, Separator):
        self.lbDict = {}
        self.lbKindList = []
        self.nList = []
        self.OhP = {}
        self.IG = Graph()
        nDict = {}
        lineIndex = 0
        
        lbFile = open(lbPath, 'r')
        while True:
            line = lbFile.readline().replace('\n', '').strip()
            if not line:
                break
            
            lineArray = line.split(Separator)
 
            if len(lineArray) == 1:
                lineIndex += 1
                node = lineIndex
                label = lineArray[0]
            else:
                node = lineArray[0]
                label = lineArray[1]
            self.lbDict[str(node)] = label
            self.lbKindList.append(label)

        lbFile.close

        self.lbKindList = list(set(self.lbKindList))
        
        IGFile = open(IGPath, 'r')
        while True:
            line = IGFile.readline().replace('\n', '').strip()
            if not line:
                break
            
            v = line.split(Separator)[0]
            u = line.split(Separator)[1]
            
            if v == u:
                continue
            
            if v not in self.lbDict:
                self.lbDict[v] = 'n'
                
            if u not in self.lbDict:
                self.lbDict[u] = 'n'
            
            self.nList.append(v)
            self.nList.append(u)

            pt = self.lbDict[v] + '/' + self.lbDict[u]
            re_pt = self.lbDict[u] + '/' + self.lbDict[v]
            
            if pt not in self.OhP and re_pt not in self.OhP:
                self.OhP[pt] = 1
                self.IG.add_edge(v,u,pt)
                
            elif re_pt in self.OhP:
                self.OhP[re_pt] = self.OhP[re_pt] + 1
                self.IG.add_edge(v,u,re_pt)
                
            elif pt in self.OhP:
                self.OhP[pt] = self.OhP[pt] + 1
                self.IG.add_edge(v,u,pt)

        IGFile.close
        self.nList = list(set(self.nList))
        
        for n in self.nList:
            nDict[n] = self.IG.vertex(n)[1]
        sortList = sorted(nDict.items(), key = lambda item: item[1], reverse = True)
        self.nList = []
        for sk, sv in sortList:
            self.nList.append(sk)
            
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