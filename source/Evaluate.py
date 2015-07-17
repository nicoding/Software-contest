from GetBestCard import BestCard
import time
import sys
from random import sample
import linecache


#the formor two rand cards are your cards, others are on the desk

def NumToCard(num):
    return [num/13,num%13+2]

def CardToNum(color,point):
    return color*13+point-2

def PairToCard(pair):
    card_1_Num = pair/52
    card_0_Num = pair%52
    if card_1_Num == card_0_Num:
        print 'error,the same card'
        sys.exit()
    else:
        card1 = NumToCard(card_1_Num)
        card0 = NumToCard(card_0_Num)
        return [[card0[0],card1[0]], [card0[1],card1[1]]]

# must be two cards
def CardsToLine(colors, points):
    num1 = CardToNum(colors[0],points[0])
    num2 = CardToNum(colors[1],points[1])
    return num2*52 + num1 + 1


def CompareEval(myEval, tmpEval):
    if myEval[0]>tmpEval[0]:
        return 1
    elif myEval[0]<tmpEval[0]:
        return -1
    else:
        for i,m in enumerate(myEval[1]):
            if m>tmpEval[1][i]:
                return 1
            elif m<tmpEval[1][i]:
                return -1
        return 0
            

def TwoCardsEvaluate(colors,points,playerNum):
    linecache.clearcache()
    return linecache.getline('./TwoCardEval/playerNum_'+str(playerNum)+'.txt',
                            CardsToLine(colors,points))
    



def FiveOrSixCardsEvaluate(colors,points):
    allCards = range(0,52)  
    for i,p in enumerate(points):
        allCards.remove(CardToNum(colors[i],p))

    length = len(colors)
    extraNum = 9-length
    extMyNum = 7-length
    win = 0
    lose = 0
    
    for i in range(4000):
        tmpCards = sample(allCards,extraNum)
        c = []
        p = []
        for j in range(extraNum):
            c.append(NumToCard(tmpCards[j])[0])
            p.append(NumToCard(tmpCards[j])[1])
        myEval = BestCard(colors+c[:extMyNum],points+p[:extMyNum])
        tmpEval = BestCard(colors[2:]+c, points[2:]+p)
        result = CompareEval(myEval,tmpEval)
        if result ==1:
            win+=1
        elif result ==-1:
            lose+=1
        else:
            win+=0.5

    return float(win)/(win+lose)

        
def SevenCardsEvaluate(colors,points):
    allCards = range(0,52)

    for i,p in enumerate(points):
        allCards.remove(CardToNum(colors[i],p))

    myEval = BestCard(colors,points)
    win = 0
    lose = 0
    
    for i in range(44,0,-1):
        for j in range(i-1,-1,-1):
            c1 = NumToCard(allCards[i])
            c2 = NumToCard(allCards[j])

            tmpEval = BestCard(colors[2:]+[c1[0],c2[0]], points[2:]+[c1[1],c2[1]])
            result = CompareEval(myEval,tmpEval)
            if result ==1 :
                win+=1
            elif result ==-1:
                lose+=1
            else:
                win+=0.5
            
    return float(win)/(win+lose)





colDic = {'SPADES':0, 'HEARTS':1, 'CLUBS':2, 'DIAMONDS':3}
potDic = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10,
          'J':11, 'Q':12, 'K':13, 'A':14}

def transformColors(colors):
    cols = []
    for c in colors:
        cols.append(colDic[c])
    return cols

def transformPoints(points):
    pots = []
    for p in points:
        pots.append(potDic[p])
    return pots



#pay attention to that (win+lose) may be 0
def EvaluateMyCard(colors_,points_,playerNum):
    if playerNum == 1:
	return 1
    paraDic = {2: 1,
               3: 0.726,
               4: 0.686,
               5: 0.655,
               6: 0.630,
               7: 0.611,
               8: 0.595}
    colors = transformColors(colors_)
    points = transformPoints(points_)
    length = len(colors)
    if length == 7:
        p = SevenCardsEvaluate(colors,points)
    elif length ==2:
        return float(TwoCardsEvaluate(colors,points,playerNum))
    else:
        p = FiveOrSixCardsEvaluate(colors,points)
    
    p= p**((playerNum-1)**paraDic[playerNum])
    p=float('%0.4f'%p)
    return p


####if __name__ == "__main__":
####    testType = 'HIGH_CARD'
####    testCards = {'HIGH_CARD':       [[0,2,3,1,2,3,1],[2,4,6,7,8,9,11]],
####                 'ONE_PAIR':        [[0,2,1,1,2,3,1],[2,2,3,4,5,7,10]],
####                 'TWO_PAIR':        [[0,1,2,3,1,2,3],[4,4,2,10,2,11,3]],
####                 'THREE_OF_A_KIND': [[0,1,2,3,1,2,2],[5,3,4,5,7,8,5]],
####                 'STRAIGHT':        [[0,1,2,3,3,2,1],[2,5,4,5,6,7,8]],
####                 'STRAIGHT_2':      [[0,1,2,3,3,2,1],[2,14,4,5,3,11,8]],
####                 'FLUSH':           [[0,1,1,3,1,1,1],[9,2,13,2,3,5,6]],
####                 'FULL_HOUSE':      [[1,2,3,1,0,3,0],[10,2,3,3,2,10,10]],
####                 'FOUR_OF_A_KIND':  [[2,3,1,3,2,0,0],[9,6,9,9,7,9,14]],
####                 'STRAIGHT_FLUSH':  [[1,2,1,1,1,1,3],[14,3,10,11,12,13,2]],
####                 '5_card_ONE_PAIR': [[1,2,3,0,1],[2,3,5,5,6]],
####                 '6_card_ONE_PAIR': [[0,1,2,3,1,2],[2,3,3,4,6,7]],
####                 '5_card':          [[0,1,2,3,1],[2,3,5,7,8]],
####                 '2_card':          [[2,0],[2,7]]}
####
####    for testType in testCards.keys():
####    time.clock()
####    for testType in ['5_card']:
####        print testType
####        print EvaluateMyCard(testCards[testType][0],testCards[testType][1],8)
####        print '=============================='
####    print time.clock()


##############################################################################
##    time.clock()
##    for playerNum in [7]:
##        ti = time.time()
##        f = open('TwoCardsEval\\playerNum_'+str(playerNum)+'.txt','w')
##        for i in range(52):
##            for j in range(52):
##                #line:i*52+j+1
##                if i==j:
##                    f.write(str(-1)+'\n')
##                else:
##                    a=NumToCard(i)
##                    b=NumToCard(j)
##                    p = MutiPlayerEvaluate([a[0],b[0]],[a[1],b[1]],playerNum)
##                    p = float('%0.4f'%p)
####                    #####TEST SATRT#######
####                    f.write(str(PairToCard(i*52+j))+'\t')
####                    #####TEST END#########
##                    
##                    f.write(str(p)+'\n')
##        f.close()
##        print playerNum
##        print time.time()-ti
##############################################################################



############################################################################
####    f = open('test.txt','w')
####    for i in range(52):
####        for j in range(52):
####            if i==j:
####                f.write(str(-1)+'\n')
####            else:
####                cards = PairToCard(i*52+j)
####                f.write(str(cards)+'\t')
####                p = TwoCardsEvaluate(cards[0],cards[1],8)
####                f.write(str(p)+'')
####    f.close()
############################################################################








    
