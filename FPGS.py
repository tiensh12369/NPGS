from InitialGraphs import Graphdata
from InitialPattern2 import Pattern
from GraphPattern import PatternMarge
import NPGSAlgorithm as na
import time
import os
import math
import sys

fileName = sys.argv[1]
pers = int(sys.argv[2]) # N-hop Pattern Filtering Ratio
psize = int(sys.argv[3]) # 𝐹𝑟𝑒𝑞𝑢𝑒𝑛𝑡 𝑃𝑎𝑡𝑡𝑒𝑟𝑛 𝑀𝑎𝑛𝑎𝑔𝑚𝑒𝑛𝑡 Table Size
batchsize = int(sys.argv[4])
windowsize = int(sys.argv[5])
DxMtrix = {}
ExceptionList = {}
iterations = 0
iterations2 = 0
FPMT = {}
th2 = batchsize * windowsize

def Top_nPercent(dict, n):
    if len(dict) == 0:
        return 0
    part_v = len(dict)*n//100
    value = list(sorted(dict.items(), key = lambda item: item[1], reverse = True))[part_v][1]
    return value

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

print('start')
for i in range(1):
    s1 = time.time()
    # IGPath = './Gen_Evolution_set/' + fileName + '/' + fileName + '_' + str(i) + '.edges'
    # lbPath = './dataset/' + fileName + '/' + fileName + '.node_labels'
    IGPath = './dataset/' + fileName + '/' + fileName + '.edges' #sys.argv[1]
    lbPath = './dataset/' + fileName + '/' + fileName + '.node_labels' #sys.argv[2]
    Separator = ','

    DataT0 = Graphdata(IGPath, lbPath, Separator)
    Th1 = Top_nPercent(DataT0.OhP, pers)
    iterations = i%batchsize
    
    if iterations < batchsize:
        FP = DataT0.OhP

        for ohp in FP.keys():
            ohpRe = ohp.split('/')
            ohpRe.reverse()
            ohpReverse = '/'.join(ohpRe)
            
            if ohp not in DxMtrix or ohpReverse not in DxMtrix:
                Raw = [[0 for col in range(batchsize)] for row in range(windowsize)]
                if FP[ohp] >= Th1:
                    Raw[iterations2][iterations] = 1
                    DxMtrix[ohp] = Raw
            else:
                if FP[ohp] >= Th1:
                    if ohpReverse in DxMtrix:
                        DxMtrix[ohpReverse][iterations2][iterations] = 1
                    else:
                        DxMtrix[ohp][iterations2][iterations] = 1
        
        if iterations == batchsize-1:
            for ohp in DxMtrix:
                if ohp not in FPMT:
                    Raw2 = [0 for col in range(windowsize+2)]
                    Raw2[iterations2] = sum(DxMtrix[ohp][iterations2])
                    FPMT[ohp] = Raw2
                else:
                    if i >= th2:
                        if FPMT[ohp][windowsize+1] == 0:
                            FPMT[ohp][iterations2] = sum(DxMtrix[ohp][iterations2])
                    else:
                        FPMT[ohp][iterations2] = sum(DxMtrix[ohp][iterations2])
                        
            for nhp in FPMT:
                if i >= th2:
                    if FPMT[nhp][windowsize+1] != 0:
                        FPMT[nhp][iterations2] = 0
                        FPMT[nhp][windowsize+1] = 0
                        FPMT[nhp][windowsize] = sum(FPMT[nhp][:windowsize])
                        ExceptionList[nhp] = FPMT[nhp]
                    else:
                        FPMT[nhp][windowsize] = sum(FPMT[nhp][:windowsize])
                        if FPMT[nhp][windowsize] <= int(th2*0.4):
                            FPMT[nhp][windowsize+1] = -1
                        elif FPMT[nhp][windowsize] >= int(th2*0.8):
                            FPMT[nhp][windowsize+1] = 1
                        else:
                            FPMT[nhp][windowsize+1] = 0
                else:
                    FPMT[nhp][windowsize] = sum(FPMT[nhp][:windowsize])
                    if FPMT[nhp][windowsize] <= int(th2*0.4):
                        FPMT[nhp][windowsize+1] = -1
                    elif FPMT[nhp][windowsize] >= int(th2*0.8):
                        FPMT[nhp][windowsize+1] = 1
                    else:
                        FPMT[nhp][windowsize+1] = 0

            iterations2 += 1
            
            if iterations2 == windowsize:
                iterations2 = 0
       
    updateWindow = (i+1)%th2
    delList = []
    if updateWindow == 0:
        for nhp in FPMT:
            if FPMT[nhp][windowsize] == 0:
                delList.append(nhp)
    
    for delOne in delList:
        del FPMT[delOne]
                
    if i >= th2-1:
        DataP0 = Pattern(FPMT, DxMtrix, ExceptionList, th2, psize)
        FPMT = DataP0.NhP
        ExceptionList = {}
        PM = PatternMarge(DataT0.IG, FPMT, DataT0.lbDict, DataT0.nList)
        Ge = PM.SG
        P_id_list = list(sorted(PM.pidDict.items(), key = lambda item: item[1], reverse = True))
        Gp = P_id_list
        Gl = list(sorted(PM.SGnl.items()))
        
        
        savefile = './Result/FPGS/'+ fileName + '/' + fileName + '_' + str(len(FPMT)) + '_' + str(pers) + '_' + str(i)
        savedata = [Ge, Gl, Gp]
        extension = ['.edges', '.node_labels', '.pattern']
        
        for sd in range(len(savedata)):
            f = open(savefile + extension[sd], 'w')
            for e in savedata[sd]:
                str_e = e[0] + ',' + e[1] + '\n'
                f.write(str_e)
        f.close()

        FPMTs = len(FPMT)
        NLs = len(PM.SGnl)
        Es = len(PM.SG)
        
        file_size = 0
        for e in extension:
            file_size = file_size + os.path.getsize(savefile + e) 
            print(e.split('.')[1], convert_size(os.path.getsize(savefile + e)))
        print('OutPut File Size:', convert_size(file_size), 'bytes')

        input_file = [IGPath, lbPath]
        file_size1 = 0
        for ip in input_file:
            file_size1 = file_size1 + os.path.getsize(ip)
            print(ip.split('.')[2], convert_size(os.path.getsize(savefile + e)))
        print('InPut File Size:', convert_size(file_size1), 'bytes')
        e1 = time.time() - s1
        print(f'Th : {Th1}, FPMTs: {FPMTs}, NLs: {NLs}, Es: {Es}, Time: {e1}')
        
        IGPath2 = savefile + '.edges' #sys.argv[1]
        lbPath2 = savefile + '.node_labels' #sys.argv[2]
        Separator = ','
        t = 2

        G = Graphdata(IGPath2, lbPath2, Separator).IG
        E = G.edge_list
        Gc = na.Basic(Ge, t, E)
        print(len(Gc.edge_list))
        