class PatternMarge:
    def __init__(self, IG, NhP, lbDict, nList):
        self.IG = IG # Initial Graph
        self.NhP = NhP # N-hop pattern
        self.lbDict = lbDict # label dict
        self.cnDict = {} # changed node dict
        self.nList = nList # node lisst
        self.pidDict = {} # pattern id dict {Marge pattern : Pattern ID}
        self.pCont = {}
        
        pDict = {} # pattern dict {Marge pattern : Marge node}
        eDict = {} # edge dict {Marge Node : Edge List}
        nopDict = {} # number of patterns dict

        while(True):
            eList = [] # edge list
            non = len(self.nList) # number of nodes

            if non <= 0:
                break
            
            node = self.nList[0]
            
            mn, mp = self.OPatternMarge(node) #marge node, marge pattern, one-hop pattern marge
                
            if mn == 0:
                eDict[node] = list(self.IG.vertex(node)[2].keys())
                self.nList.remove(node)
                continue

            b = 1 #boolean
            while (b > 0):
                mn, mp, b = self.NPatternMarge(mn, mp) #N-hop pattern marge
            
            mpRe = mp.split('/')
            mpRe.reverse()
            mpReverse = '/'.join(mpRe)
            
            if mpReverse in self.NhP.keys():
                mnRe = mn.split('/')
                mnRe.reverse()
                mn = '/'.join(mnRe)
                mp = mpReverse
            
            dList = mn.split('/') #delete list
            for dValue in dList:
                self.nList.remove(dValue)
                degList = list(self.IG.vertex(dValue)[2].keys()) ##degree List
                eList.extend(degList)
                self.cnDict[dValue] = mn
                
            eDict[mn] = eList
            
            if mp not in pDict:
                pDict[mp] = [mn]
                nopDict[mp] = len(eList)
            else:
                pDict[mp].append(mn)
                nopDict[mp] = nopDict[mp] + len(eList)
        
        pList = list(sorted(nopDict.items(), key = lambda item: item[1], reverse = True)) #pattern list
        prList = [] #pattern rank list
        
        for pl in pList:
            prList.append(pl[0])
        
        c0 = 0
        for prValue in prList:
            P0 = "P" + str(c0)
            self.pidDict[prValue] = P0
            c0 += 1
        
        mn_pidnDict = {} # PatternID-Number {Marge Node : PatternID-Number}
        pidn_pidDict = {} # {PatternID-Number : PatternID}
        self.pidn_mnDict = {} # {PatternID-Number : Marge Node}
        
        for mp in pDict:
            PID = self.pidDict[mp] # Pattern ID
            c1 = 0
            for mn in pDict[mp]:
                PIDN = PID + '-' + str(c1) # Pattern ID Number
                mn_pidnDict[mn] = PIDN
                self.pidn_mnDict[PIDN] = mn
                pidn_pidDict[PIDN] = PID
                c1 += 1
                
            self.pCont[mp] = c1 #Pattern ID Count
        
        GSe = {} # summarized graph edge {SGn:SGlabel}

        for nValue in eDict:
            dList = []
            for eValue in eDict[nValue]:
                if eValue in self.cnDict:
                    dList.append(eValue)
                    eDict[nValue].append(self.cnDict[eValue])
                    
            for dValue in dList:
                eDict[nValue].remove(dValue)
            eDict[nValue] = list(set(eDict[nValue]))

            if nValue in mn_pidnDict:
                SGn = mn_pidnDict[nValue] # summarized graph node
            else:
                SGn = nValue

            for eValue in eDict[nValue]:
                if eValue in mn_pidnDict:
                    SGnn = mn_pidnDict[eValue] #summarized graph neigbor node
                else:
                    SGnn = eValue
                    
                if SGn not in GSe:
                    GSe[SGn] = [SGnn]
                else:
                    GSe[SGn].append(SGnn)
        
        self.SG = [] # output graph OR summarized graph
        self.SGnl = {} # summarized graph node label {nodes : label}
        for SGn in GSe:
            if SGn not in self.SGnl:
                if SGn in lbDict:
                    self.SGnl[SGn] = lbDict[SGn]
                elif SGn in pidn_pidDict:
                    self.SGnl[SGn] = pidn_pidDict[SGn]

            for SGnn in GSe[SGn]:
                if SGn == SGnn:
                    continue
                if [SGn, SGnn] not in self.SG and [SGnn, SGn] not in self.SG:
                    self.SG.append([SGn, SGnn])
                if SGnn not in self.SGnl:
                    if SGnn in lbDict:
                        self.SGnl[SGnn] = lbDict[SGnn]
                    elif SGnn in pidn_pidDict:
                        self.SGnl[SGnn] = pidn_pidDict[SGnn]
                        
    def neighborScore(self, v, u):
        degMax = self.IG.vertex(v)[1]
        degSame = len((self.IG.vertex(v)[2].keys() & self.IG.vertex(u)[2].keys()))
        degRatio = self.IG.vertex(u)[1]/self.IG.vertex(v)[1]
                
        score = (degSame/degMax) + degRatio
        
        return score

    def OPatternMarge(self, v):
        score = {}
        NeighborNode = self.IG.vertex(v)[2]
        
        for u in NeighborNode:
            if u in self.cnDict:
                continue
            
            nbRe = NeighborNode[u].split('/')
            nbRe.reverse()
            PatternRevers = '/'.join(nbRe)
            if NeighborNode[u] in self.NhP.keys() or PatternRevers in self.NhP.keys():
                score[u] = self.neighborScore(v, u)
        
        if score:
            su = list(sorted(score.items(), key = lambda item: item[1], reverse = True))[0]
            self.IG.del_edge(v, su[0])
            MargeNode = v + '/' + su[0]
            MargePattern = self.lbDict[v] + '/' + self.lbDict[su[0]]
            return MargeNode, MargePattern
        else:
            return 0, 0
        
    def NPatternMarge(self, MargeNode, MargePattern):
        MargeNodeList = MargeNode.split('/')
        frontNode = MargeNodeList[0]
        backNode = MargeNodeList[-1]
        frontMax = [0,0]
        backMax = [0,0]
        UnionPattern1 = {}
        UnionPattern2 = {}
        frontScore = {}
        backScore = {}

        for front in self.IG.vertex(frontNode)[2].keys():
            if front in self.cnDict or front in MargeNodeList:
                continue
            UnionPattern1[front] = self.lbDict[front] + '/' + MargePattern
            
        for back in self.IG.vertex(backNode)[2].keys():
            if back in self.cnDict or back in MargeNodeList:
                continue
            UnionPattern2[back] = MargePattern + '/' + self.lbDict[back]
                
        for union in UnionPattern1.keys():
            ptlist = UnionPattern1[union].split('/')
            ptlist.reverse()
            PatternRevers = '/'.join(ptlist)
            if UnionPattern1[union] in self.NhP.keys() or PatternRevers in self.NhP.keys():
                frontScore[union] = self.neighborScore(frontNode, union)
        
        for union in UnionPattern2.keys():
            ptlist = UnionPattern2[union].split('/')
            ptlist.reverse()
            PatternRevers = '/'.join(ptlist)
            if UnionPattern2[union] in self.NhP.keys() or PatternRevers in self.NhP.keys():
                backScore[union] = self.neighborScore(backNode, union)
        
        if frontScore:
            frontMax = list(sorted(frontScore.items(), key = lambda item: item[1], reverse = True))[0]

        if backScore:
            backMax = list(sorted(backScore.items(), key = lambda item: item[1], reverse = True))[0]
            
        if frontMax[1] >= backMax[1] and frontMax[1] != 0:
            self.IG.del_edge(frontNode, frontMax[0])
            MargeNode = frontMax[0] + '/' + MargeNode
            MargePattern = UnionPattern1[frontMax[0]]
            
        elif frontMax[1] < backMax[1] and backMax[1] != 0:
            self.IG.del_edge(backNode, backMax[0])
            MargeNode = MargeNode + '/' + backMax[0]
            MargePattern = UnionPattern2[backMax[0]]
            
        else:
            return MargeNode, MargePattern, 0
            
        return MargeNode, MargePattern, 1
            
