class Pattern:
    def __init__(self, FPMT, DxMtrix, ExceptionList, th, psize):
        self.NhP = {}
        self.NhP.update(FPMT)
        self.th = th
        self.psize = psize
        self.ExceptionList = ExceptionList
        self.updatePattern(FPMT, self.ExceptionList, DxMtrix, 0)
        
    def pattern_gen(self, ptternFrequency, ExceptionList, DxMtrix, patternSize):
        add_pt = {}
        
        for pt1 in ptternFrequency:
            pt_tgt = pt1.split('/')
            for pt2 in ptternFrequency:
                pt_scr = pt2.split('/')
                between_len = len(pt_tgt)
                if len(pt_tgt) != len(pt_scr):
                    continue
                if between_len == 2:
                    if pt_tgt[0] == pt_scr[0]:
                        pt = pt_scr[1] + '/' + pt1
                    elif pt_tgt[0] == pt_scr[1]:
                        pt = pt_scr[0] + '/' + pt1
                    elif pt_tgt[1] == pt_scr[0]:
                        pt = pt1 + '/' + pt_scr[1]
                    elif pt_tgt[1] == pt_scr[1]:
                        pt = pt1 + '/' + pt_scr[0]
                    else:
                        continue
                else:
                    between_len = between_len//2
                    if pt_tgt[:-1] == pt_scr[1:]: #앞, 뒤
                        pt = pt_scr[0] + '/' + pt1
                    elif pt_tgt[1:] == pt_scr[:-1]: #뒤, 앞
                        pt = pt1 + '/' + pt_scr[-1]
                    else:
                        continue
                
                ptlist = pt.split('/')
                ptlist.reverse()
                ptRe = '/'.join(ptlist)
                
                if pt in ExceptionList or ptRe in ExceptionList:
                    continue
                
                minlist2 = []
                if pt not in add_pt and ptRe not in add_pt:
                    if pt1 in DxMtrix and pt2 in DxMtrix:
                        for i in range(len(DxMtrix[pt1])):
                            minlist = []
                            for j in range(len(DxMtrix[pt1][i])):
                                minlist.append(min(DxMtrix[pt1][i][j], DxMtrix[pt2][i][j]))
                            minlist2.append(sum(minlist))
                                
                        minlist2.append(sum(minlist2))
                        if minlist2[-1] <= int(self.th*0.4):
                            minlist2.append(-1)
                        elif minlist2[-1] >= int(self.th*0.8):
                            minlist2.append(1)
                        else:
                            minlist2.append(0)
                        
                    else:
                        for i in range(len(ptternFrequency[pt1])):
                            minlist2.append(min(ptternFrequency[pt1][i], ptternFrequency[pt2][i]))
                        minlist2[-2] = sum(minlist2[:-2])
                            
                        if minlist2[-2] <= int(self.th*0.4):
                            minlist2[-1] = -1
                        elif minlist2[-2] >= int(self.th*0.8):
                            minlist2[-1] = 1
                        else:
                            minlist2[-1] = 0

                    if minlist2[-1] > 0:
                        add_pt[pt] = minlist2
                    
                    if patternSize + len(add_pt) >= self.psize:
                        return add_pt
        return add_pt

    def updatePattern(self, updateDict, ExceptionList, DxMtrix, recursionlimit):
        patternSize = len(self.NhP)
        if patternSize >= self.psize:
            update_dict = []
        else:
            update_dict = self.pattern_gen(updateDict, ExceptionList, DxMtrix, patternSize)

        if len(update_dict) != 0:
            recursionlimit += 1
            self.NhP.update(update_dict)
            if recursionlimit < 10:
                self.updatePattern(update_dict, ExceptionList, DxMtrix, recursionlimit)
            
