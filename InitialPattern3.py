class Pattern:
    def __init__(self, OhP, ExceptionList, pers, psize):
        self.NhP = {}
        self.NhP.update(OhP)
        self.psize = psize
        self.ExceptionList = ExceptionList
        ohpValue = list(set(OhP.values()))
        ohpValue.sort(reverse=True)
        part_v = len(ohpValue)*pers//100
        self.Threshold = ohpValue[part_v]
        # self.Threshold = self.Top_nPercent(OhP, pers)
        self.updatePattern(OhP, self.ExceptionList, self.Threshold)
        
    def pattern_gen(self, ptternFrequency, ExceptionList, Threshold, patternSize):
        add_pt = {}
        
        if Threshold < 0:
            return {}
        
        for pt1 in ptternFrequency:
            if ptternFrequency[pt1] >= Threshold:
                pt_tgt = pt1.split('/')
                for pt2 in ptternFrequency:
                    if ptternFrequency[pt2] >= Threshold:
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
                        print(ptRe)
                        if pt not in add_pt and ptRe not in add_pt:
                            
                            if pt1 == pt2:
                                PFA = ptternFrequency[pt1] - ptternFrequency[pt1]//len(pt_scr) #Same Pattern Frequent Attenuation
                                if PFA >= Threshold:
                                    add_pt[pt] = PFA
                                
                            else:
                                add_pt[pt] = min(ptternFrequency[pt1], ptternFrequency[pt2])

                        if patternSize + len(add_pt) >= self.psize:
                            return add_pt
        
        return add_pt

    def updatePattern(self, updateDict, ExceptionList, Threshold):
        patternSize = len(self.NhP)
        if patternSize >= self.psize:
            update_dict = []
        else:
            update_dict = self.pattern_gen(updateDict, ExceptionList, Threshold, patternSize)
        if len(update_dict) != 0:
            self.NhP.update(update_dict)
            self.updatePattern(update_dict, ExceptionList, Threshold)
            
