# -*- coding: cp936 -*-

def isMoneyEnough(myJetton, needToBet):
    if myJetton >= needToBet:
        return True
    else: 
        return False

def calMaxBet(bet):
    if len(bet) == 0:
        return 0
    elif len(bet) == 1:
        return max(bet)
    else:
        tempBet = []
        for i in range(1, len(bet)):
            tempBet.append(abs(bet[i] - bet[i - 1])) 
        return max(tempBet)

def calMoney(totalNum,money,jetton):
    totalMoney = []
    if len(money) <= 1:
        return 0,0 
    else:
        for i in range(0,len(money)-1):
            totalMoney.append(money[i] + jetton[i])  
        moneyMin = min(totalMoney)
        moneyMax = max(totalMoney)
    return moneyMin,moneyMax

def FindInterval(prob, thresholdList):
    regularizedList = [round((i - prob),4) for i in thresholdList]
    valueFirstPos = regularizedList[0]

    count = 0
    for value in regularizedList:
        if(value > 0):
            valueFirstPos = value
            break
        else:
            count += 1
            
    if count == 0:                         #  prob is too small
        indexFirstPos = 0
        valueFirstPos = thresholdList[0]
        indexLastNeg = 0
        valueLastNeg = thresholdList[0]    
    elif count == len(regularizedList):    # prob is too large
        indexFirstPos = len(regularizedList)-1
        valueFirstPos = thresholdList[indexFirstPos]
        indexLastNeg = len(regularizedList)-1
        valueLastNeg = thresholdList[indexLastNeg]
    else:
        indexFirstPos = regularizedList.index(valueFirstPos)
        valueFirstPos = thresholdList[indexFirstPos]
        indexLastNeg = indexFirstPos - 1
        valueLastNeg = thresholdList[indexLastNeg]
    
    return indexLastNeg, valueLastNeg, indexFirstPos, valueFirstPos

def MapProb(prob, thresholdList):
    if prob < thresholdList[0]:
        return 0
    elif prob >= thresholdList[0] and prob < thresholdList[1]:
        return 1
    elif prob >= thresholdList[1] and prob < thresholdList[2]:
        return 2
    elif prob >= thresholdList[2] and prob < thresholdList[3]:
        return 3
    elif prob >= thresholdList[3] and prob < thresholdList[4]:
        return 4
    elif prob >= thresholdList[4] and prob < thresholdList[5]:
        return 5
    elif prob >= thresholdList[5] and prob < thresholdList[6]:
        return 6
    elif prob >= thresholdList[6] and prob < thresholdList[7]:
        return 7
    elif prob >= thresholdList[7] and prob < thresholdList[8]:
        return 8
    elif prob >= thresholdList[8]:
        return 9


def CalEffectiveProb(prob, stage, playerNum, raiseInfo, ACIB):
    import math
    if stage == 2:
        if playerNum == 2:
            threshold1 = 0.5586
            threshold11 = 0.5966
            threshold12 = 0.6795
            threshold13 = 0.7485
            threshold2 = 0.7825
            threshold21 = 0.8140
            threshold22 = 0.8422
            threshold23 = 0.8839
            threshold3 = 0.9441
        elif playerNum == 3:
            threshold1 = 0.3820
            threshold11 = 0.4256
            threshold12 = 0.5280
            threshold13 = 0.6194
            threshold2 = 0.6668
            threshold21 = 0.7120
            threshold22 = 0.7530
            threshold23 = 0.8154
            threshold3 = 0.9092
        elif playerNum == 4:
            threshold1 = 0.2900
            threshold11 = 0.3340
            threshold12 = 0.4400
            threshold13 = 0.5404
            threshold2 = 0.5942
            threshold21 = 0.6460
            threshold22 = 0.6945
            threshold23 = 0.7693
            threshold3 = 0.8850
        elif playerNum == 5:
            threshold1 = 0.2363
            threshold11 = 0.2780
            threshold12 = 0.3835
            threshold13 = 0.4877
            threshold2 = 0.5450
            threshold21 = 0.6000
            threshold22 = 0.6533
            threshold23 = 0.7364
            threshold3 = 0.8671
        elif playerNum == 6:
            threshold1 = 0.2010
            threshold11 = 0.2410
            threshold12 = 0.3448
            threshold13 = 0.4501
            threshold2 = 0.5090
            threshold21 = 0.5670
            threshold22 = 0.6229
            threshold23 = 0.7116
            threshold3 = 0.8534
        elif playerNum == 7:
            threshold1 = 0.1756
            threshold11 = 0.2137
            threshold12 = 0.3150
            threshold13 = 0.4210
            threshold2 = 0.4810
            threshold21 = 0.5410
            threshold22 = 0.5986
            threshold23 = 0.6916
            threshold3 = 0.8421
        else :
            threshold1 = 0.1568
            threshold11 = 0.1934
            threshold12 = 0.2920
            threshold13 = 0.3977
            threshold2 = 0.4584
            threshold21 = 0.5195
            threshold22 = 0.5790
            threshold23 = 0.6752
            threshold3 = 0.8327


    elif stage == 3:
        if playerNum == 2:
            threshold1 = 0.5292
            threshold11 = 0.5710
            threshold12 = 0.6560
            threshold13 = 0.7300
            threshold2 = 0.7687
            threshold21 = 0.8128
            threshold22 = 0.8562
            threshold23 = 0.9500
            threshold3 = 0.9784
        elif playerNum == 3:
            threshold1 = 0.3490
            threshold11 = 0.3960
            threshold12 = 0.4980
            threshold13 = 0.5940
            threshold2 = 0.6472
            threshold21 = 0.7095
            threshold22 = 0.7736
            threshold23 = 0.9187
            threshold3 = 0.9645
        elif playerNum == 4:
            threshold1 = 0.2586
            threshold11 = 0.3040
            threshold12 = 0.4084
            threshold13 = 0.5122
            threshold2 = 0.5720
            threshold21 = 0.6436
            threshold22 = 0.7189
            threshold23 = 0.8967
            threshold3 = 0.9547
        elif playerNum == 5:
            threshold1 = 0.2064
            threshold11 = 0.2493
            threshold12 = 0.3517
            threshold13 = 0.4580
            threshold2 = 0.5210
            threshold21 = 0.5980
            threshold22 = 0.6810
            threshold23 = 0.8806
            threshold3 = 0.9473
        elif playerNum == 6:
            threshold1 = 0.1730
            threshold11 = 0.2134
            threshold12 = 0.3130
            threshold13 = 0.4200
            threshold2 = 0.4843
            threshold21 = 0.5645
            threshold22 = 0.6520
            threshold23 = 0.8682
            threshold3 = 0.9416
        elif playerNum == 7:
            threshold1 = 0.1492
            threshold11 = 0.1874
            threshold12 = 0.2838
            threshold13 = 0.3905
            threshold2 = 0.4557
            threshold21 = 0.5380
            threshold22 = 0.6286
            threshold23 = 0.8579
            threshold3 = 0.9368
        else :
            threshold1 = 0.1319
            threshold11 = 0.1680
            threshold12 = 0.2614
            threshold13 = 0.3670
            threshold2 = 0.4330
            threshold21 = 0.5170
            threshold22 = 0.6105
            threshold23 = 0.8494
            threshold3 = 0.9329

    elif stage == 4:
        if playerNum == 2:
            threshold1 = 0.5159
            threshold11 = 0.5693
            threshold12 = 0.6670
            threshold13 = 0.7558
            threshold2 = 0.8205
            threshold21 = 0.8602
            threshold22 = 0.8965
            threshold23 = 0.9417
            threshold3 = 0.9764
        elif playerNum == 3:
            threshold1 = 0.3347
            threshold11 = 0.3940
            threshold12 = 0.5120
            threshold13 = 0.6294
            threshold2 = 0.7219
            threshold21 = 0.7796
            threshold22 = 0.8347
            threshold23 = 0.9054
            threshold3 = 0.9613
        elif playerNum == 4:
            threshold1 = 0.2451
            threshold11 = 0.3022
            threshold12 = 0.4230
            threshold13 = 0.5517
            threshold2 = 0.6570
            threshold21 = 0.7262
            threshold22 = 0.7930
            threshold23 = 0.8802
            threshold3 = 0.9505
        elif playerNum == 5:
            threshold1 = 0.1938
            threshold11 = 0.2474
            threshold12 = 0.3665
            threshold13 = 0.4996
            threshold2 = 0.6125
            threshold21 = 0.6885
            threshold22 = 0.7627
            threshold23 = 0.8616
            threshold3 = 0.9425
        elif playerNum == 6:
            threshold1 = 0.1614
            threshold11 = 0.2117
            threshold12 = 0.3280
            threshold13 = 0.4623
            threshold2 = 0.5800
            threshold21 = 0.6604
            threshold22 = 0.7400
            threshold23 = 0.8474
            threshold3 = 0.9363
        elif playerNum == 7:
            threshold1 = 0.1384
            threshold11 = 0.1858
            threshold12 = 0.2988
            threshold13 = 0.4333
            threshold2 = 0.5540
            threshold21 = 0.6380
            threshold22 = 0.7216
            threshold23 = 0.8357
            threshold3 = 0.9311
        else :
            threshold1 = 0.1217
            threshold11 = 0.1665
            threshold12 = 0.2760
            threshold13 = 0.4102
            threshold2 = 0.5330
            threshold21 = 0.6196
            threshold22 = 0.7070
            threshold23 = 0.8260
            threshold3 = 0.9268    
    else:
            threshold1 = 0.1217
            threshold11 = 0.1665
            threshold12 = 0.2760
            threshold13 = 0.4102
            threshold2 = 0.5330
            threshold21 = 0.6196
            threshold22 = 0.7070
            threshold23 = 0.8260
            threshold3 = 0.9268  

    if stage == 1 :
        return prob, raiseInfo, ACIB
    else:
        thresholdList = [threshold1, threshold11, threshold12, threshold13, \
                        threshold2, threshold21, threshold22, threshold23,threshold3]

        indexLastNeg, valueLastNeg, indexFirstPos, valueFirstPos = FindInterval(prob, thresholdList)

        if indexFirstPos == indexLastNeg:
            if indexFirstPos == 0:
                probMapped = 0
            elif indexFirstPos == (len(thresholdList)-1):
                probMapped = 9
        else:
            raiseInfoReg = raiseInfo - 1
            if(raiseInfoReg == 0):
                probMapped = MapProb(prob, thresholdList)
            elif(raiseInfoReg > 0):
                if (raiseInfoReg > 0) and (raiseInfoReg < 1):
                    prob = prob + (valueFirstPos - valueLastNeg) * raiseInfoReg
                    probMapped = MapProb(prob, thresholdList)
                elif (raiseInfoReg >= 1):
                    raiseinfoFraction = raiseInfoReg - int(raiseInfoReg)
                    prob = prob + (valueFirstPos - valueLastNeg) * raiseinfoFraction
                    probMapped = MapProb(prob, thresholdList)
                    if probMapped <= 7:
                        probMapped = probMapped + int(raiseInfoReg)
                    else:
                        pass
            elif(raiseInfoReg < 0):
                raiseInfoReg = abs(raiseInfoReg)
                if (raiseInfoReg > 0) and (raiseInfoReg < 1):
                    prob = prob - (valueFirstPos - valueLastNeg) * raiseInfoReg
                    probMapped = MapProb(prob, thresholdList)
                elif (raiseInfoReg >= 1):
                    raiseinfoFraction = raiseInfoReg - int(raiseInfoReg)
                    prob = prob - (valueFirstPos - valueLastNeg) * raiseinfoFraction
                    probMapped = MapProb(prob, thresholdList)
                    if (probMapped < 9):
                        probMapped = probMapped - int(raiseInfoReg)
                        if probMapped < 0:
                            probMapped = 0
                        else:
                            pass
                    else:
                        pass
                        
            if ACIB == 1:
                if stage == 2:
                    if playerNum <= 3:
                        if probMapped >= 5:
                            probMapped += 2
                        else:
                            pass
                    elif playerNum <= 5:
                        if probMapped >= 5:
                            probMapped += 1
                        else:
                            pass
                    else:
                        pass
                else:
                    if playerNum <= 3:
                        if probMapped >= 5:
                            probMapped += 1
                        else:
                            pass
                    else:
                        pass
            else:
                pass

            if probMapped > 9:
                probMapped = 9
            else:
                pass
	#f.write('\n probMapped='+str(probMapped)+'\n')
        return probMapped, raiseInfo, ACIB
