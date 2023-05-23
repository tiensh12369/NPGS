def p(integer):
    if integer == 1:
        return 0.5
    elif integer == 2:
        return 1
    
def neighPath(graph, vNeigh, t):
    vNeighList = []
    for n in vNeigh:
        vNeighList.extend(list(graph.vertex(n)[2].keys()))
        
    if t > 1:
        vNeighList2 = neighPath(graph, vNeighList, t-1)
        return vNeighList2
        
    return vNeighList

def swappingEdge(E):
    import random
    randomIndex1 = random.randrange(0, len(E))
    randomIndex2 = random.randrange(0, len(E))
    E[randomIndex1], E[randomIndex2] = E[randomIndex2], E[randomIndex1]
    return E

def Basic(G, t, E):
    import InitialGraphs
    
    cGraph = InitialGraphs.Graph()
    aGraph = InitialGraphs.Graph()
    
    for v, u in E:
        aGraph.add_edge(v,u,None)
        vNeigh1a = list(aGraph.vertex(v)[2].keys())
        uNeigh1a = list(aGraph.vertex(u)[2].keys())

        insert = False
        
        for i in range(1, t+1):
            
            vNeighc = list(cGraph.vertex(v)[2].keys())
            uNeighc = list(cGraph.vertex(u)[2].keys())
            
            if i != 1:
                vNeighc = neighPath(cGraph, vNeighc, i)
                uNeighc = neighPath(cGraph, uNeighc, i)

            if len(list(set(vNeighc) & set(vNeigh1a))) < p(i) * len(vNeigh1a) or len(list(set(uNeighc) & set(uNeigh1a))) < p(i) * len(uNeigh1a):
                insert = True
                break
            
        if insert:
            cGraph.add_edge(v,u,None)
            
    return cGraph

def GreedyLP(G, t, E):
    Ego = []
    for v,u in E:
        xel = []
        scorexe = 0
        for i in range(1, t+1):
            vNeigh = list(G.vertex(v)[2].keys())
            vNeigh.remove(u)
            xe = 1
            if i != 1:
                vNeigh = neighPath(G, vNeigh, t)
                for w in vNeigh:
                    if w == u:
                        xe = 0
            xel.append(xe)
            
        scorexe = sum(xel)/t
        Ego.append([v,u,scorexe])

    Ego.sort(key=lambda x:x[2], reverse=True)
    
    for edge in Ego:
        del edge[2]
        
    return Ego

def GreedyEC(G, t, E):
    Ego = []
    for v,u in E:
        edgeCount = 0
        for i in range(1, t+1):
            vNeigh = list(G.vertex(v)[2].keys())
            if i != 1:
                vNeigh = neighPath(G, vNeigh, t)
                
            for w in vNeigh:
                if w == u:
                    edgeCount += 1

        Ego.append([v,u,edgeCount])

    Ego.sort(key=lambda x:x[2], reverse=True)
    
    for edge in Ego:
        del edge[2]
        
    return Ego

def GreedySA(G, t, E, N, T0, alpha):
    import random
    import math
    
    S = E
    T = T0
    Gt = Basic(G, t, S)
    Cbest = len(Gt.edge_list)
    Cs = len(Gt.edge_list)
    COSTs = 0
    Ebest = S
    print(f'init: {Cbest}')
    for i in range(1, N+1):
        S2 = swappingEdge(S)
        Gt = Basic(G, t, S2)
        
        if len(Gt.edge_list) < Cbest:
            Ebest = S
            Cbest = len(Gt.edge_list)
            print(f'if1: {Cbest}')
        
        if len(Gt.edge_list) < COSTs:
            S = S2
            Cs = len(Gt.edge_list)
            print(f'if2: {Cs}')
            
        else:
            r = random.randint(0, 1)
            d = Cs-len(Gt.edge_list)
            probability = (d/T)
            if math.exp(probability) > r:
                S = S2
                COSTs = len(Gt.edge_list)
                print(i, COSTs)
        T = alpha * T
        
    Gc = Basic(G, t, Ebest)
    return Gc