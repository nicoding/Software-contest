# -*- coding: cp936 -*-
# ---------------------------------------------
#  File: ActionDecision
#  Author: Derek Tian @SJTU
#  Date: July 3, 2015
#  Description: decide the money sizing to bet
#  --------------------------------------------
from CalEffectiveProb_spurs_oneonone import *

def ActionDecisionBottomSpursOneonone(prob, money, jetton, bet, totalPot, stage, playerNum, currentGameNum, isButton, raiseInfo, totalNum, ACIB, smallBlind, blindInfo, checkEnable): 
    import random
    maxBet = max(bet)                         # the current max bet available
    needToBet = maxBet - bet[-1]              # the bet you put in this round
    myJetton = jetton[-1]                     # the jetton you have now  
    bluffMoney = random.randint(200, 300)
    moneyEnough = 1

    bluffEnable = 0

    playerNumCall = 0
    thresholdFront = 0.99
    thresholdBack = 1.03
    
    if raiseInfo != 1:
        for i in bet:
            if i == maxBet:
                playerNumCall += 1
            else:
                pass
    else:
        pass
    
    numFront = int(isButton) / 100
    isButton = isButton % 100
    numBack = int(isButton) / 10
    isButton = isButton % 10

    prob, raiseInfo, ACIB = CalEffectiveProb(prob, stage, playerNum, raiseInfo, ACIB)
    SBAdjustRate = 1
    
    if stage == 1:
        if (totalNum == 2):
            myTotalMoney = money[-1] + jetton[-1]
            enemyTotalMin,enemyTotalMax = calMoney(totalNum, money, jetton)
            if (myTotalMoney - enemyTotalMax) > SBAdjustRate * (20 + 10 * (600 - currentGameNum)):
                return "fold"
            elif (enemyTotalMax - myTotalMoney) > SBAdjustRate * (20 + 10 * (600 - currentGameNum)):
                if prob >= 40 and prob <= 60:
                    prob += 20
                else:
                    pass
            elif (enemyTotalMax - myTotalMoney) > SBAdjustRate * (20 + 5 * (600 - currentGameNum)):
                if prob >= 40 and prob <= 70:
                    prob += 10
                else:
                    pass
            else:
                pass

        elif (totalNum == 3):
            myTotalMoney = money[-1] + jetton[-1]
            enemyTotalMin,enemyTotalMax = calMoney(totalNum, money, jetton)
            if (myTotalMoney - enemyTotalMax) > SBAdjustRate * (2000 + 20 * (600 - currentGameNum)):
                prob = prob - 20 
            elif (myTotalMoney - enemyTotalMax) > SBAdjustRate * (2000 + 12 * (600 - currentGameNum)):
                prob = prob - 10
            else:
                pass

        else:
            myTotalMoney = money[-1] + jetton[-1]
            enemyTotalMin,enemyTotalMax = calMoney(totalNum, money, jetton)
            if (myTotalMoney - enemyTotalMax) > SBAdjustRate * (2000 + 30 * (600 - currentGameNum)):
                prob = prob - 20
            elif (myTotalMoney - enemyTotalMax) > SBAdjustRate * (2000 + 20 * (600 - currentGameNum)):
                prob = prob - 10
            else:
                pass

    else:
        if (totalNum == 2):
            myTotalMoney = money[-1] + jetton[-1]
            enemyTotalMin,enemyTotalMax = calMoney(totalNum, money, jetton)
            if (myTotalMoney - enemyTotalMax) > SBAdjustRate * (20 + 10 * (600 - currentGameNum)):
                return "fold"
            elif (enemyTotalMin - myTotalMoney) > SBAdjustRate * (20 + 10 * (600 - currentGameNum)):
                if prob >= 1 and prob <= 6:
                    prob += 2
                else:
                    pass
            elif (enemyTotalMin - myTotalMoney) > SBAdjustRate * (20 + 5 * (600 - currentGameNum)):
                if prob >= 1 and prob <= 7:
                    prob += 1
                else:
                    pass
            else:
                pass

        elif (totalNum == 3):
            myTotalMoney = money[-1] + jetton[-1]
            enemyTotalMin,enemyTotalMax = calMoney(totalNum, money, jetton)
            if (myTotalMoney - enemyTotalMin) < 0 and currentGameNum > 500:
                if prob >= 1:
                    prob = prob + 1
                else:
                    prob = prob + 0
            else:
                pass
        else:
            myTotalMoney = money[-1] + jetton[-1]
            enemyTotalMin,enemyTotalMax = calMoney(totalNum, money, jetton)
            if (myTotalMoney - enemyTotalMin) < 0 and currentGameNum > 500:
                if prob >= 1:
                    prob = prob + 1
                else:
                    prob = prob + 0
            else:
                pass
        
    if stage == 1:
        if needToBet == 0:      
            if prob >= 100:
                betNum = max(calMaxBet(bet), random.randint(200, 300))
                if isMoneyEnough(myJetton, (needToBet + betNum)):
                    actionMsg = "raise %d" % betNum
                else:
                    actionMsg = "check"

            elif prob >= 90:
                betNum = max(calMaxBet(bet), random.randint(90, 100))
                if isMoneyEnough(myJetton, (needToBet + betNum)):
                    actionMsg = "raise %d" % betNum
                else:
                    actionMsg = "check"

            elif prob >= 80:
                betNum = max(calMaxBet(bet), random.randint(75, 85))
                if isMoneyEnough(myJetton, (needToBet + betNum)):
                    actionMsg = "raise %d" % betNum
                else:
                    actionMsg = "check"

            elif prob >= 70:
                betNum = max(calMaxBet(bet), random.randint(65, 75))
                if isMoneyEnough(myJetton, (needToBet + betNum)):
                    actionMsg = "raise %d" % betNum
                else:
                    actionMsg = "check"

            elif prob >= 50:
                actionMsg = "check"

            elif prob > 0:
                if ACIB == 1 and playerNum <= 3:
                    betNum = max(calMaxBet(bet), random.randint(bluffMoney, bluffMoney + 40))
                    if isMoneyEnough(myJetton, betNum):
                        actionMsg = "raise %d" % betNum
                    else:
                        actionMsg = "all_in"
                else:
                    actionMsg = "check"
            else:
                actionMsg = "check"

        elif needToBet == smallBlind and totalNum > 2:
            if prob >= 100:
                if checkEnable:
                    actionMsg = "call"
                else:
                    betNum = max(calMaxBet(bet), random.randint(200, 300))
                    if isMoneyEnough(myJetton, (needToBet + betNum)):
                        actionMsg = "raise %d" % betNum
                    else:
                        actionMsg = "call"

            elif prob >= 90:
                if checkEnable:
                    actionMsg = "call"
                else:
                    betNum = max(calMaxBet(bet), random.randint(90, 100))
                    if isMoneyEnough(myJetton, (needToBet + betNum)):
                        actionMsg = "raise %d" % betNum
                    else:
                        actionMsg = "call"

            elif prob >= 80:
                if checkEnable:
                    actionMsg = "call"
                else:
                    betNum = max(calMaxBet(bet), random.randint(75, 85))
                    if isMoneyEnough(myJetton, (needToBet + betNum)):
                        actionMsg = "raise %d" % betNum
                    else:
                        actionMsg = "call"

            elif prob >= 70:
                betNum = max(calMaxBet(bet), random.randint(65, 75))
                if isMoneyEnough(myJetton, (needToBet + betNum)):
                    actionMsg = "raise %d" % betNum
                else:
                    actionMsg = "call"

            elif prob >= 50:
                actionMsg = "call"

            else:
                if playerNum == 2:
                    betNum = 40
                    actionMsg = "raise %d" % betNum
                else:
                    actionMsg = "fold"
        
        else:
            moneyEnough = isMoneyEnough(myJetton, needToBet)
            needToBet = min(needToBet, jetton[-1]) 
            if playerNum > 4:
                if prob >= 100:
                    if checkEnable:
                        actionMsg = "call"
                    else:
                        if needToBet > 200:
                            actionMsg = "call"
                        else:
                            betNum = max(calMaxBet(bet), random.randint(250, 300))
                            if isMoneyEnough(myJetton, (needToBet + betNum)):
                                actionMsg = "raise %d" % betNum
                            else:
                                actionMsg = "call"

                elif prob >= 90:
                    if checkEnable:
                        actionMsg = "call"
                    else:
                        if needToBet > 600:
                            if bet[-1] >= (0.05 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        
                        elif needToBet > 85:
                            actionMsg = "call"

                        else:
                            betNum = max(calMaxBet(bet), random.randint(90,100))
                            if isMoneyEnough(myJetton, (needToBet + betNum)):
                                actionMsg = "raise %d" % betNum
                            else:
                                actionMsg = "call"

                elif prob >= 80:
                    if (raiseInfo < 1):
                        if (isButton <= thresholdFront):
                            if needToBet > 500:
                                if bet[-1] >= (0.08 * needToBet):
                                    actionMsg = "call"
                                else:
                                    actionMsg = "fold"
                            else:
                                actionMsg = "call"
                        else:
                            if needToBet > 500:
                                if bet[-1] >= (0.04 * needToBet):
                                    actionMsg = "call"
                                else:
                                    actionMsg = "fold"
                            elif needToBet > 70:
                                actionMsg = "call"
                            else:
                                betNum = max(calMaxBet(bet), random.randint(75, 85))
                                if isMoneyEnough(myJetton, (needToBet + betNum)):
                                    actionMsg = "raise %d" % betNum
                                else:
                                    actionMsg = "call"

                    elif raiseInfo == 1:
                        if checkEnable:
                            actionMsg = "call"
                        else:
                            if (isButton <= thresholdFront):
                                actionMsg = "call"
                            else:
                                if needToBet > 70:
                                    actionMsg = "call"
                                else:
                                    betNum = max(calMaxBet(bet), random.randint(75, 85))
                                    if isMoneyEnough(myJetton, (needToBet + betNum)):
                                        actionMsg = "raise %d" % betNum
                                    else:
                                        actionMsg = "call"

                    else:
                        if needToBet >= 500:
                            if bet[-1] >= (0.04 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        
                        elif needToBet > 60:
                            actionMsg = "call"

                        else:
                            betNum = max(calMaxBet(bet), random.randint(75, 85))
                            if isMoneyEnough(myJetton, (needToBet + betNum)):
                                actionMsg = "raise %d" % betNum
                            else:
                                actionMsg = "call"

                elif prob >= 70:
                    if (raiseInfo < 1):
                        if (isButton <= thresholdFront):
                            if needToBet > 350:
                                if bet[-1] > (0.15 * needToBet):
                                    actionMsg = "call"
                                else:
                                    actionMsg = "fold"
                            else:
                                actionMsg = "call"
                        else:
                            if needToBet > 350:
                                if bet[-1] > (0.10 * needToBet):
                                    actionMsg = "call"
                                else:
                                    actionMsg = "fold"
                            else:
                                actionMsg = "call"

                    elif raiseInfo == 1:
                        if (isButton <= thresholdBack):
                            actionMsg = "call"
                        else:
                            if needToBet > 45:
                                actionMsg = "call"
                            else:
                                betNum = max(calMaxBet(bet), random.randint(65, 75))
                                if isMoneyEnough(myJetton, (needToBet + betNum)):
                                    actionMsg = "raise %d" % betNum
                                else:
                                    actionMsg = "call"         

                    else:
                        if needToBet > 400:
                            if bet[-1] >= (0.10 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        elif needToBet > 60:
                            actionMsg = "call"
                        else:
                            betNum = max(calMaxBet(bet), random.randint(65, 75))
                            if isMoneyEnough(myJetton, (needToBet + betNum)):
                                actionMsg = "raise %d" % betNum
                            else:
                                actionMsg = "call"

                elif prob >= 60:
                    if (raiseInfo < 1):
                        if (isButton <= thresholdFront):
                            if needToBet > 250:
                                if bet[-1] >= (0.125 * needToBet):
                                    actionMsg = "call"
                                else:
                                    actionMsg = "fold"
                            else:
                                actionMsg = "call"
                        else:
                            if needToBet > 250:
                                if bet[-1] >= (0.08 * needToBet):
                                    actionMsg = "call"
                                else:
                                    actionMsg = "fold"
                            else:
                                actionMsg = "call"

                    elif raiseInfo == 1:
                        if(isButton <= thresholdFront):
                            actionMsg = "call"
                        else:
                            if needToBet > 250:
                                if bet[-1] >= (0.08 * needToBet):
                                    actionMsg = "call"
                                else:
                                    actionMsg = "fold"

                            elif needToBet > 45:
                                actionMsg = "call"
                            
                            else:
                                betNum = max(calMaxBet(bet), random.randint(50, 55))
                                if isMoneyEnough(myJetton, (needToBet + betNum)):
                                    actionMsg = "raise %d" % betNum
                                else:
                                    actionMsg = "call" 

                    else:
                        if needToBet > 300:
                            if bet[-1] >= (0.065 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        elif needToBet > 45:
                            actionMsg = "call"

                        else:
                            betNum = max(calMaxBet(bet), random.randint(50, 55))
                            if isMoneyEnough(myJetton, (needToBet + betNum)):
                                actionMsg = "raise %d" % betNum
                            else:
                                actionMsg = "call"

                elif prob >= 50:
                    if (raiseInfo < 1):
                        if (isButton < thresholdBack):
                            actionMsg = "fold"
                        else:
                            if needToBet > 160:
                                if bet[-1] >= (0.25 * needToBet):
                                    actionMsg = "call"
                                else:
                                    actionMsg = "fold"
                            else:
                                actionMsg = "call"

                    elif raiseInfo == 1:
                        if(isButton <= thresholdBack):
                            actionMsg = "call"
                        else:
                            if needToBet > 150:
                                if bet[-1] > (0.10 * needToBet):
                                    actionMsg = "call"
                                else:
                                    actionMsg = "fold"
                            else:
                                actionMsg = "call"         

                    else:
                        if (isButton <= thresholdBack):
                            if needToBet > 200:
                                if bet[-1] >= (0.15 * needToBet):
                                    actionMsg = "call"
                                else:
                                    actionMsg = "fold"
                            else:
                                actionMsg = "call"
                        else:
                            if needToBet > 200:
                                if bet[-1] >= (0.10 * needToBet):
                                    actionMsg = "call"
                                else:
                                    actionMsg = "fold"
                            else:
                                actionMsg = "call"

                elif prob >= 40:
                    if (raiseInfo < 1):
                        if (isButton < thresholdBack):
                            actionMsg = "fold"
                        else:
                            if needToBet > 100:
                                if bet[-1] >= (0.4 * needToBet):
                                    actionMsg = "call"
                                else:
                                    actionMsg = "fold"
                            else:
                                actionMsg = "call"

                    elif raiseInfo == 1:
                        if(isButton <= thresholdFront):
                            actionMsg = "fold"
                        else:
                            actionMsg = "call"         

                    else:
                        if needToBet > 160:
                            if bet[-1] >= (0.15 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        else:
                            actionMsg = "call"

                else:
                    actionMsg = "fold"

            else:
                if prob >= 100:
                    if needToBet > 200:
                        actionMsg = "call"
                    else:
                        betNum = max(calMaxBet(bet), random.randint(250, 300))
                        if isMoneyEnough(myJetton, (needToBet + betNum)):
                            actionMsg = "raise %d" % betNum
                        else:
                            actionMsg = "call"

                elif prob >= 90:
                    if needToBet > 600:
                        if bet[-1] >= (0.05 * needToBet):
                            actionMsg = "call"
                        else:
                            actionMsg = "fold"
                    
                    elif needToBet > 85:
                        actionMsg = "call"

                    else:
                        betNum = max(calMaxBet(bet), random.randint(90,100))
                        if isMoneyEnough(myJetton, (needToBet + betNum)):
                            actionMsg = "raise %d" % betNum
                        else:
                            actionMsg = "call"

                elif prob >= 80:
                    if (raiseInfo < 1):
                        if (isButton <= thresholdFront):
                            if needToBet > 500:
                                if bet[-1] >= (0.08 * needToBet):
                                    actionMsg = "call"
                                else:
                                    actionMsg = "fold"
                            else:
                                actionMsg = "call"
                        else:
                            if needToBet > 500:
                                if bet[-1] >= (0.04 * needToBet):
                                    actionMsg = "call"
                                else:
                                    actionMsg = "fold"
                            elif needToBet > 70:
                                actionMsg = "call"
                            else:
                                betNum = max(calMaxBet(bet), random.randint(75, 85))
                                if isMoneyEnough(myJetton, (needToBet + betNum)):
                                    actionMsg = "raise %d" % betNum
                                else:
                                    actionMsg = "call"

                    elif raiseInfo == 1:
                        if needToBet > 70:
                            actionMsg = "call"
                        else:
                            betNum = max(calMaxBet(bet), random.randint(75, 85))
                            if isMoneyEnough(myJetton, (needToBet + betNum)):
                                actionMsg = "raise %d" % betNum
                            else:
                                actionMsg = "call"

                    else:
                        if needToBet > 500:
                            if bet[-1] >= (0.04 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        
                        elif needToBet > 60:
                            actionMsg = "call"

                        else:
                            betNum = max(calMaxBet(bet), random.randint(75, 85))
                            if isMoneyEnough(myJetton, (needToBet + betNum)):
                                actionMsg = "raise %d" % betNum
                            else:
                                actionMsg = "call"

                elif prob >= 70:
                    if (raiseInfo < 1):
                        if needToBet > 350:
                            if bet[-1] > (0.10 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        else:
                            actionMsg = "call"

                    elif raiseInfo == 1:
                        if needToBet > 350:
                            if bet[-1] > (0.10 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        elif needToBet > 45:
                            actionMsg = "call"
                        else:
                            betNum = max(calMaxBet(bet), random.randint(65, 75))
                            if isMoneyEnough(myJetton, (needToBet + betNum)):
                                actionMsg = "raise %d" % betNum
                            else:
                                actionMsg = "call"        

                    else:
                        if needToBet > 400:
                            if bet[-1] >= (0.10 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        elif needToBet > 60:
                            actionMsg = "call"
                        else:
                            betNum = max(calMaxBet(bet), random.randint(65, 75))
                            if isMoneyEnough(myJetton, (needToBet + betNum)):
                                actionMsg = "raise %d" % betNum
                            else:
                                actionMsg = "call"

                elif prob >= 60:
                    if (raiseInfo < 1):
                        if needToBet > 250:
                            if bet[-1] >= (0.08 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        else:
                            actionMsg = "call"

                    elif raiseInfo == 1:
                        if(isButton <= thresholdFront):
                            actionMsg = "call"
                        else:
                            if needToBet > 250:
                                if bet[-1] >= (0.08 * needToBet):
                                    actionMsg = "call"
                                else:
                                    actionMsg = "fold"

                            elif needToBet > 45:
                                actionMsg = "call"
                            
                            else:
                                betNum = max(calMaxBet(bet), random.randint(50, 55))
                                if isMoneyEnough(myJetton, (needToBet + betNum)):
                                    actionMsg = "raise %d" % betNum
                                else:
                                    actionMsg = "call" 

                    else:
                        if needToBet > 300:
                            if bet[-1] >= (0.065 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        elif needToBet > 45:
                            actionMsg = "call"

                        else:
                            betNum = max(calMaxBet(bet), random.randint(50, 55))
                            if isMoneyEnough(myJetton, (needToBet + betNum)):
                                actionMsg = "raise %d" % betNum
                            else:
                                actionMsg = "call"

                elif prob >= 50:
                    if (raiseInfo < 1):
                        if needToBet > 160:
                            if bet[-1] >= (0.25 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        else:
                            actionMsg = "call"

                    elif raiseInfo == 1:
                        if(isButton <= thresholdFront):
                            actionMsg = "call"
                        else:
                            if needToBet > 150:
                                if bet[-1] > (0.10 * needToBet):
                                    actionMsg = "call"
                                else:
                                    actionMsg = "fold"
                            else:
                                actionMsg = "call"          

                    else:
                        if needToBet > 200:
                            if bet[-1] >= (0.10 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        else:
                            actionMsg = "call"

                elif prob >= 40:
                    if (raiseInfo < 1):
                        if needToBet > 100:
                            if bet[-1] >= (0.4 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        else:
                            actionMsg = "call"

                    elif raiseInfo == 1:
                        if(isButton <= thresholdFront):
                            actionMsg = "call"
                        else:
                            if needToBet > 120:
                                if bet[-1] > (0.10 * needToBet):
                                    actionMsg = "call"
                                else:
                                    actionMsg = "fold"
                            else:
                                actionMsg = "call"          

                    else:
                        if needToBet > 160:
                            if bet[-1] >= (0.15 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        else:
                            actionMsg = "call"

                else:
                    actionMsg = "fold"


    elif stage == 2:
        if needToBet == 0:
            if prob < 5 :
                if bluffEnable:
                    betNum = max(calMaxBet(bet), random.randint(bluffMoney, bluffMoney + 40))
                    if isMoneyEnough(myJetton, betNum):
                        actionMsg = "raise %d" % betNum
                    else:
                        actionMsg = "check"
                else:
                    actionMsg = "check"

            elif (prob >= 5) and (prob < 9):
                if prob == 5:
                    betNum = max(calMaxBet(bet), random.randint(40, 50))
                    if betNum > 80:
                        actionMsg = "check"
                    else :
                        if isMoneyEnough(myJetton, (needToBet + betNum)):
                            actionMsg = "raise %d" % betNum
                        else:
                            actionMsg = "all_in"
                      
                elif prob == 6:
                    if checkEnable:
                        actionMsg = "check"
                    else:
                        betNum = max(calMaxBet(bet), random.randint(75, 85))
                        if betNum > 120:
                            actionMsg = "check"
                        else :
                            if isMoneyEnough(myJetton, (needToBet + betNum)):
                                actionMsg = "raise %d" % betNum
                            else:
                                actionMsg = "all_in"

                elif prob == 7:
                    if checkEnable:
                        actionMsg = "check"
                    else:
	                    betNum = max(calMaxBet(bet), random.randint(120, 130))
	                    if betNum > 180:
	                        actionMsg = "check"
	                    else :
	                        if isMoneyEnough(myJetton, (needToBet + betNum)):
	                            actionMsg = "raise %d" % betNum
	                        else:
	                            actionMsg = "all_in"

                elif prob == 8:
                    if checkEnable:
                        actionMsg = "check"
                    else:
                        betNum = max(calMaxBet(bet), random.randint(175, 185))
                        if betNum > 240:
                            actionMsg = "check"
                        else :
                            if isMoneyEnough(myJetton, (needToBet + betNum)):
                                actionMsg = "raise %d" % betNum
                            else:
                                actionMsg = "all_in"

            elif prob == 9:
                if checkEnable:
                    actionMsg = "check"
                else:
                    betNum = max(calMaxBet(bet), random.randint(290, 310))
                    if isMoneyEnough(myJetton, (needToBet + betNum)):
                        actionMsg = "raise %d" % betNum
                    else:
                        actionMsg = "all_in"

            else:
                actionMsg = "check" 

        else:                
            moneyEnough = isMoneyEnough(myJetton, needToBet)
            needToBet = min(needToBet, jetton[-1])
            if prob == 0:
                if bet[-1] > (8 * needToBet):
                    actionMsg = "call"
                else:
                    actionMsg = "fold"

            elif (prob >= 1) and (prob < 5):
                if prob == 1:
                    if playerNumCall >= 3:
                        actionMsg = "fold"
                    else:
                        if needToBet > 80:
                            if bet[-1] > (0.75 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        else:
                            actionMsg = "call"

                elif prob == 2:
                    if playerNumCall >= 3:
                        actionMsg = "fold"
                    else:
                        if needToBet > 120:
                            if bet[-1] > (0.5 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        else:
                            actionMsg = "call"

                elif prob == 3:
                    if playerNumCall >= 3:
                        actionMsg = "fold"
                    else:
                        if needToBet > 160:
                            if bet[-1] > (0.4 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        else:
                            actionMsg = "call"

                else:
                    if playerNumCall >= 3:
                        actionMsg = "fold"
                    else:
                        if needToBet > 240:
                            if bet[-1] > (0.15 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        else:
                            actionMsg = "call"
                        
            elif (prob >= 5) and (prob < 9):
                if prob == 5:
                    if needToBet > 300:
                        if bet[-1] >= (0.125 * needToBet):
                            actionMsg = "call"
                        else:
                            actionMsg = "fold"
                    
                    elif needToBet > 55:
                        actionMsg = "call"

                    else:
                        betNum = max(calMaxBet(bet), random.randint(60, 65))
                        if isMoneyEnough(myJetton, (needToBet + betNum)):
                            actionMsg = "raise %d" % betNum
                        else:
                            actionMsg = "call"

                elif prob == 6:
                    if needToBet > 400:
                        if bet[-1] >= 0.05 * needToBet:
                            actionMsg = "call"
                        else:
                            actionMsg = "fold"
                    
                    elif needToBet > 75:
                        actionMsg = "call"

                    else:
                        betNum = max(calMaxBet(bet), random.randint(80, 85))
                        if isMoneyEnough(myJetton, (needToBet + betNum)):
                            actionMsg = "raise %d" % betNum
                        else:
                            actionMsg = "call"

                elif prob == 7:
                    if needToBet > 500:
                        if bet[-1] >= 0.04 * needToBet:
                            actionMsg = "call"
                        else:
                            actionMsg = "fold"
                    
                    elif needToBet > 100:
                        actionMsg = "call"

                    else:
                        betNum = max(calMaxBet(bet), random.randint(120, 130))
                        if isMoneyEnough(myJetton, (needToBet + betNum)):
                            actionMsg = "raise %d" % betNum
                        else:
                            actionMsg = "call"

                elif prob == 8:
                    if needToBet > 600:
                        if bet[-1] >= 0.01 * needToBet:
                            actionMsg = "call"
                        else:
                            actionMsg = "fold"
                    
                    else:
                        if bet[-1] <= 800:
                            betNum = max(calMaxBet(bet), random.randint(175, 185))
                            if isMoneyEnough(myJetton, (needToBet + betNum)):
                                actionMsg = "raise %d" % betNum
                            else:
                                actionMsg = "all_in"
                        else:
                            actionMsg = "call"

            elif prob == 9:
                betNum = max(calMaxBet(bet), random.randint(300, 400))
                if isMoneyEnough(myJetton, (needToBet + betNum)):
                    actionMsg = "raise %d" % betNum
                else:
                    actionMsg = "all_in"
                
            else:
                actionMsg = "fold"  

    elif stage == 3:
        if needToBet == 0:
            if prob == 0:
                actionMsg = "check"
            elif (prob >= 1) and (prob < 5):
                if random.randint(0,1):
                    betNum = max(calMaxBet(bet), random.randint(40,45))
                    if isMoneyEnough(myJetton, betNum):
                        actionMsg = "raise %d" % betNum
                    else:
                        actionMsg = "check"
                else:
                    actionMsg = "check"

            elif (prob >= 5) and (prob < 9):
                if prob == 5:
                    betNum = max(calMaxBet(bet), random.randint(75, 85))
                    if betNum > 120:
                        actionMsg = "check"
                    else :
                        if isMoneyEnough(myJetton, (needToBet + betNum)):
                            actionMsg = "raise %d" % betNum
                        else:
                            actionMsg = "check"
                      
                elif prob == 6:
                    if checkEnable:
                        actionMsg = "check"
                    else:
                        betNum = max(calMaxBet(bet), random.randint(155, 165))
                        if betNum > 220:
                            actionMsg = "check"
                        else :
                            if isMoneyEnough(myJetton, (needToBet + betNum)):
                                actionMsg = "raise %d" % betNum
                            else:
                                actionMsg = "check"

                elif prob == 7:
                    if checkEnable:
                        actionMsg = "check"
                    else:
	                    betNum = max(calMaxBet(bet), random.randint(245, 255))
	                    if betNum > 300:
	                        actionMsg = "check"
	                    else :
	                        if isMoneyEnough(myJetton, (needToBet + betNum)):
	                            actionMsg = "raise %d" % betNum
	                        else:
	                            actionMsg = "check"

                elif prob == 8:
                    if checkEnable:
                        actionMsg = "check"
                    else:
                        betNum = max(calMaxBet(bet), random.randint(315, 325))
                        if betNum > 360:
                            actionMsg = "check"
                        else:
                            if isMoneyEnough(myJetton, (needToBet + betNum)):
                                actionMsg = "raise %d" % betNum
                            else:
                                actionMsg = "all_in"

            elif prob == 9:
                if checkEnable:
                    actionMsg = "check"
                else:
                    betNum = max(calMaxBet(bet), random.randint(500, 520))
                    if isMoneyEnough(myJetton, (needToBet + betNum)):
                        actionMsg = "raise %d" % betNum
                    else:
                        actionMsg = "all_in"

            else:
                actionMsg = "check" 

        else:
            moneyEnough = isMoneyEnough(myJetton, needToBet)
            needToBet = min(needToBet, jetton[-1])
            if prob == 0:
                if bet[-1] > (8 * needToBet):
                    actionMsg = "call"
                else:
                    actionMsg = "fold"
            elif (prob >= 1) and (prob < 5):
                if prob == 1:
                    if playerNumCall >= 3:
                        actionMsg = "fold"
                    else:
                        if needToBet > 80:
                            if bet[-1] > (1 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        else:
                            actionMsg = "call"

                elif prob == 2:
                    if playerNumCall >= 3:
                        actionMsg = "fold"
                    else:
                        if needToBet > 120:
                            if bet[-1] > (0.75 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        else:
                            actionMsg = "call"

                elif prob == 3:
                    if playerNumCall >= 3:
                        actionMsg = "fold"
                    else:
                        if needToBet > 160:
                            if bet[-1] > (0.5 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        else:
                            actionMsg = "call"

                else:
                    if playerNumCall >= 3:
                        actionMsg = "fold"
                    else:
                        if needToBet > 240:
                            if bet[-1] > (0.25 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        else:
                            actionMsg = "call"
            
                            
            elif (prob >= 5) and (prob < 9):
                if prob == 5:
                    if needToBet > 300:
                        if bet[-1] >= (0.2 * needToBet):
                            actionMsg = "call"
                        else:
                            actionMsg = "fold"
                    
                    elif needToBet > 55:
                        actionMsg = "call"

                    else:
                        betNum = max(calMaxBet(bet), random.randint(75, 85))
                        if isMoneyEnough(myJetton, (needToBet + betNum)):
                            actionMsg = "raise %d" % betNum
                        else:
                            actionMsg = "call"

                elif prob == 6:
                    if needToBet > 400:
                        if bet[-1] >= (0.15 * needToBet):
                            actionMsg = "call"
                        else:
                            actionMsg = "fold"
                    
                    elif needToBet > 110:
                        actionMsg = "call"

                    else:
                        betNum = max(calMaxBet(bet), random.randint(155, 165))
                        if isMoneyEnough(myJetton, (needToBet + betNum)):
                            actionMsg = "raise %d" % betNum
                        else:
                            actionMsg = "call"

                elif prob == 7:
                    if needToBet > 500:
                        if bet[-1] >= (0.12 * needToBet):
                            actionMsg = "call"
                        else:
                            actionMsg = "fold"
                    
                    elif needToBet > 180:
                        actionMsg = "call"

                    else:
                        betNum = max(calMaxBet(bet), random.randint(245, 255))
                        if isMoneyEnough(myJetton, (needToBet + betNum)):
                            actionMsg = "raise %d" % betNum
                        else:
                            actionMsg = "call"
                    

                elif prob == 8:
                    if needToBet > 600:
                        if bet[-1] >= (0.02 * needToBet):
                            actionMsg = "call"
                        else:
                            actionMsg = "fold"

                    else:
                        if bet[-1] <= 1200:
                            betNum = max(calMaxBet(bet), random.randint(315, 325))
                            if isMoneyEnough(myJetton, (needToBet + betNum)):
                                actionMsg = "raise %d" % betNum
                            else:
                                actionMsg = "all_in"
                        else:
                            actionMsg = "call"

            elif prob == 9:
                betNum = max(calMaxBet(bet), random.randint(500, 520))
                if isMoneyEnough(myJetton, (needToBet + betNum)):
                    actionMsg = "raise %d" % betNum
                else:
                    actionMsg = "all_in"
        
            else:
                actionMsg = "fold"  
                                
    elif stage == 4:
        if needToBet == 0:
            if prob == 0:
                actionMsg = "check"
            elif (prob >= 1) and (prob < 5):
                if random.randint(0,1):
                    betNum = max(calMaxBet(bet), random.randint(40,45))
                    if isMoneyEnough(myJetton, betNum):
                        actionMsg = "raise %d" % betNum
                    else:
                        actionMsg = "check"
                else:
                    actionMsg = "check"

            elif (prob >= 5) and (prob < 9):
                if prob == 5:
                    betNum = max(calMaxBet(bet), random.randint(115, 125))
                    if betNum > 200:
                        actionMsg = "check"
                    else :
                        if isMoneyEnough(myJetton, (needToBet + betNum)):
                            actionMsg = "raise %d" % betNum
                        else:
                            actionMsg = "check"
                      
                elif prob == 6:
                    betNum = max(calMaxBet(bet), random.randint(195, 205))
                    if betNum > 300:
                        actionMsg = "check"
                    else :
                        if isMoneyEnough(myJetton, (needToBet + betNum)):
                            actionMsg = "raise %d" % betNum
                        else:
                            actionMsg = "check"

                elif prob == 7:
                    betNum = max(calMaxBet(bet), random.randint(265, 275))
                    if betNum > 360:
                        actionMsg = "check"
                    else :
                        if isMoneyEnough(myJetton, (needToBet + betNum)):
                            actionMsg = "raise %d" % betNum
                        else:
                            actionMsg = "check"

                elif prob == 8:
                    betNum = max(calMaxBet(bet), random.randint(375, 385))
                    if betNum > 480:
                        actionMsg = "check"
                    else :
                        if isMoneyEnough(myJetton, (needToBet + betNum)):
                            actionMsg = "raise %d" % betNum
                        else:
                            actionMsg = "all_in"

            elif prob == 9:
                betNum = 0.8 * jetton[-1]
                if betNum <= 320:
                    actionMsg = "all_in"
                else:
                    if isMoneyEnough(myJetton, (needToBet + betNum)):
                        actionMsg = "raise %d" % betNum
                    else:
                        actionMsg = "all_in"

            else:
                actionMsg = "check"  

        else:
            moneyEnough = isMoneyEnough(myJetton, needToBet)
            needToBet = min(needToBet, jetton[-1])
            if prob == 0:
                if bet[-1] > (8 * needToBet):
                    actionMsg = "call"
                else:
                    actionMsg = "fold"
            elif (prob >= 1) and (prob < 5):
                if prob == 1:
                    if playerNumCall >= 3:
                        actionMsg = "fold"
                    else:
                        if needToBet > 80:
                            if bet[-1] > (1 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        else:
                            actionMsg = "call"

                elif prob == 2:
                    if playerNumCall >= 3:
                        actionMsg = "fold"
                    else:
                        if needToBet > 140:
                            if bet[-1] > (0.75 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        else:
                            actionMsg = "call"

                elif prob == 3:
                    if playerNumCall >= 3:
                        actionMsg = "fold"
                    else:
                        if needToBet > 200:
                            if bet[-1] > (0.5 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        else:
                            actionMsg = "call"

                else:
                    if playerNumCall >= 3:
                        actionMsg = "fold"
                    else:
                        if needToBet > 300:
                            if bet[-1] > (0.25 * needToBet):
                                actionMsg = "call"
                            else:
                                actionMsg = "fold"
                        else:
                            actionMsg = "call"
                    
            elif (prob >= 5) and (prob < 9):
                if prob == 5:
                    if needToBet > 400:
                        if bet[-1] >= (0.185 * needToBet):
                            actionMsg = "call"
                        else:
                            actionMsg = "fold"
                    
                    elif needToBet > 90:
                        actionMsg = "call"

                    else:
                        betNum = max(calMaxBet(bet), random.randint(95, 105))
                        if isMoneyEnough(myJetton, (needToBet + betNum)):
                            actionMsg = "raise %d" % betNum
                        else:
                            actionMsg = "call"

                elif prob == 6:
                    if needToBet > 450:
                        if bet[-1] >= (0.15 * needToBet):
                            actionMsg = "call"
                        else:
                            actionMsg = "fold"
                  
                    elif needToBet > 160:
                        actionMsg = "call"

                    else:
                        betNum = max(calMaxBet(bet), random.randint(190, 210))
                        if isMoneyEnough(myJetton, (needToBet + betNum)):
                            actionMsg = "raise %d" % betNum
                        else:
                            actionMsg = "call"

                elif prob == 7:
                    if needToBet > 500:
                        if bet[-1] >= (0.12 * needToBet):
                            actionMsg = "call"
                        else:
                            actionMsg = "fold"
                    
                    elif needToBet > 260:
                        actionMsg = "call"

                    else:
                        betNum = max(calMaxBet(bet), random.randint(290, 310))
                        if isMoneyEnough(myJetton, (needToBet + betNum)):
                            actionMsg = "raise %d" % betNum
                        else:
                            actionMsg = "call"

                elif prob == 8:
                    if needToBet > 600:
                        if bet[-1] >= (0.05 * needToBet):
                            actionMsg = "call"
                        else:
                            actionMsg = "fold"
                    
                    else:
                        if bet[-1] <= 1400:
                            betNum = max(calMaxBet(bet), random.randint(390, 410))
                            if isMoneyEnough(myJetton, (needToBet + betNum)):
                                actionMsg = "raise %d" % betNum
                            else:
                                actionMsg = "all_in"
                        else:
                            actionMsg = "call"

            elif prob == 9:
                betNum = 0.8 * jetton[-1]
                if isMoneyEnough(myJetton, (needToBet + betNum)):
                    actionMsg = "raise %d" % betNum
                else:
                    actionMsg = "call" 
        
            else:
                actionMsg = "fold"  

    else :
        actionMsg = "fold"

    if actionMsg == "fold":
        if myJetton < 40:
            actionMsg = "all_in"
        else:
            pass
    elif actionMsg == "call":
        if (myJetton - needToBet) < 40:
            actionMsg = "all_in"
        else:
            pass
    elif actionMsg.find('raise') >= 0:
        if (myJetton - needToBet - int(actionMsg[6:])) < 40:
            actionMsg = "all_in"

    if moneyEnough:
        pass
    else:
        if actionMsg == "fold":
            pass
        else:
            actionMsg = "all_in"

    return actionMsg
