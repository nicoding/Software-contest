
##colours: SPADES->0; HEARTS->1; CLUBS->2; DIAMONDS->3
##define A->14

colDic = {0:'SPADES', 1:'HEARTS', 2:'CLUBS', 3:'DIAMONDS'}

# if not, return 0, or return the first point of the straight
def JudgeStraight(setPot):
    #insure that is daoxu
    setPot.sort()
    setPot.reverse()
    if 14 in setPot:
        setPot.append(1)
    count = 0
    pointPre = setPot[0]
    for i,point in enumerate(setPot[1:]):
        if pointPre -point==1:
            count+=1
            if count==4:
                return setPot[i+1]
        else:
            count=0
        pointPre = point
    return 0


#card num must be [3,7]
def BestCard(colors,points):
    lenOrigin = len(colors)
    setCol = sorted(set(colors))
    setPot = sorted(set(points),reverse=True) 
    lenSetedCol = len(setCol)
    lenSetedPot = len(setPot)    

    freqCol = []
    freqPot = []
    for i in setCol:
        freqCol.append(colors.count(i))
    for i in setPot:
        freqPot.append(points.count(i))

    #FLUSH
    #only this pay attention to the order of the colors and points
    if max(freqCol)>=5:
        colFreqMax = setCol[freqCol.index(max(freqCol))]
        pot_ = []
        for i,c in enumerate(colors):
            if c==colFreqMax:
                pot_.append(points[i])
        pot_.sort(reverse=True)
        jS = JudgeStraight(pot_)
        if jS:
            return [9,[jS]]
        else:
            #if it's level_6, it will impossible to be level_8,7
            return [6,pot_[:5]]

    #FOUR_OF_A_KIND
    if max(freqPot)==4:
        four = setPot[freqPot.index(4)]
        setPot.remove(four)
        return [8,[four,setPot[0]]]
    #Three
    elif max(freqPot)==3:
        point_3_1 = setPot[freqPot.index(3)]
        if 2 in freqPot:
            point_2_1 = setPot[freqPot.index(2)]
            return [7,[point_3_1,point_2_1]]
        else:
            freqPot.remove(3)
            if max(freqPot)==3:
                point_3_2 = setPot[freqPot.index(3)+1]
                return [7,[point_3_1,point_3_2]]
            else:
                jS = JudgeStraight(setPot)
                if jS:
                    return [5,[jS]]
                else:
                    setPot.remove(point_3_1)
                    return [4,[point_3_1]+setPot[:2]]
    
    #Every point is different
    jS = JudgeStraight(setPot)
    if jS:
        return [5,[jS]]

    #Two
    if max(freqPot)==2:
        point_2_1 = setPot[freqPot.index(2)]
        freqPot.remove(2)
        if max(freqPot)==2:
            point_2_2 = setPot[freqPot.index(2)+1]
            setPot.remove(point_2_1)
            setPot.remove(point_2_2)
            return [3,[point_2_1,point_2_2]+setPot[:1]]
        else:
            setPot.remove(point_2_1)
            return [2,[point_2_1]+setPot[:3]]


    
    points.sort(reverse=True)
    return [1,points[0:min(5,lenOrigin)]]




if __name__=="__main__":

    testType = 'STRAIGHT_FLUSH'
    testCards = {'HIGH_CARD':       [[0,2,3,1,2,3,1],[2,4,6,7,8,9,11]],
                 'ONE_PAIR':        [[0,2,1,1,2,3,1],[2,2,3,4,5,7,10]],
                 'TWO_PAIR':        [[0,1,2,3,1,2,3],[4,4,2,10,2,11,3]],
                 'THREE_OF_A_KIND': [[0,1,2,3,1,2,2],[5,3,4,5,7,8,5]],
                 'STRAIGHT':        [[0,1,2,3,3,2,1],[2,5,4,5,6,7,8]],
                 'STRAIGHT_2':      [[0,1,2,3,3,2,1],[2,14,4,5,3,11,8]],
                 'FLUSH':           [[0,1,1,3,1,1,1],[9,2,13,7,3,5,6]],
                 'FLUSH_2':         [[1,1,1,1,1,1,1],[9,2,13,10,3,4,5]],
                 'FULL_HOUSE':      [[1,2,3,1,2,3,0],[10,2,3,3,2,10,10]],
                 'FOUR_OF_A_KIND':  [[2,3,1,3,2,1,0],[9,6,9,9,7,9,14]],
                 'STRAIGHT_FLUSH':  [[0,2,1,1,1,1,1],[2,3,10,11,12,13,14]],
                 '5_card_ONE_PAIR': [[1,2,3,0,1],[2,3,5,5,6]]}

    #for testType in ['STRAIGHT_FLUSH']:
    for testType in testCards.keys():
        print '========================='
        print 'input cards is:'
        for i in range(len(testCards[testType][0])):
            print colDic.get(testCards[testType][0][i])+'\t'+str(testCards[testType][1][i])
        print '-------------------------'
        print BestCard(testCards[testType][0],testCards[testType][1])
        print '========================='


