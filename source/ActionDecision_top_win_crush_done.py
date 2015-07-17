from ActionDecision_final_spurs_6 import *
from ActionDecision_final_spurs_1v1 import *

def ActionDecision(prob, money, jetton, bet, totalPot, stage, playerNum, currentGameNum, oppHisWinProbAllIn, oppHisWinProbRaise, isButton, raiseInfo, totalNum, ACIB, smallBlind, initialJetton, initialMoney, MoneyJettonSB, blindInfo, checkEnable,jettonWF): 
#def ActionDecision(prob, money, jetton, bet, totalPot, stage, playerNum, currentGameNum, isButton, raiseInfo, totalNum, ACIB, smallBlind, initialJetton, initialMoney, MoneyJettonSB, blindInfo, checkEnable, jettonWF): 

    if playerNum == 1:
        return "all_in"
    
    if totalNum == 2:
        if blindInfo == 1:
            blindInfo = 2
        else:
            pass
    else:
        pass

    # checkEnable = 1
    # learnAdjustRate = 0                    
##    if stage >= 2:
##        pAllInMax = 0
##        pAllInMin = 1
##        sampleAllInMax = 1
##        sampleAllInMin = 1
##        for pAllIn in oppHisWinProbAllIn.keys():
##            if pAllInMax<max(oppHisWinProbAllIn[pAllIn]):
##                pAllInMax = max(oppHisWinProbAllIn[pAllIn])
##                sampleAllInMax = len(oppHisWinProbAllIn[pAllIn])
##            if pAllInMin>min(oppHisWinProbAllIn[pAllIn]):
##                pAllInMin = min(oppHisWinProbAllIn[pAllIn])
##                sampleAllInMin = len(oppHisWinProbAllIn[pAllIn])
##
##        pRaiseMax = 0
##        pRaiseMin = 1
##        sampleRaiseMax = 1
##        sampleRaiseMin = 1
##        for pRaise in oppHisWinProbRaise.keys():
##            if pRaiseMax<max(oppHisWinProbRaise[pRaise]):
##                pRaiseMax = max(oppHisWinProbRaise[pRaise])
##                sampleRaiseMax = len(oppHisWinProbRaise[pRaise])
##            if pRaiseMin>min(oppHisWinProbRaise[pRaise]):
##                pRaiseMin = min(oppHisWinProbRaise[pRaise])
##                sampleRaiseMin = len(oppHisWinProbRaise[pRaise])
##
##        if prob > (pAllInMax+0.1/sampleAllInMax) and sampleAllInMax > 5:
##            learnAdjustRate = 2
##        elif prob > (pAllInMax+0/sampleAllInMax) and sampleAllInMax > 5:
##            learnAdjustRate = 1
##        elif prob < (sampleAllInMin - 0.1/sampleAllInMin) and sampleAllInMin > 5:
##            return 'fold'
##
##        if prob > (pRaiseMax+0.1/sampleRaiseMax) and sampleRaiseMax > 5:
##            learnAdjustRate = 2
##        elif prob > (pRaiseMax+0/sampleRaiseMax) and sampleRaiseMax > 5:
##            learnAdjustRate = 1
##        elif prob < (pRaiseMin - 0.1/sampleRaiseMin) and sampleRaiseMin > 5:
##            return 'fold'
##    else:
##        pass

    SBRate   = 20.0 / smallBlind
    money    = [i * SBRate for i in money]
    jetton   = [i * SBRate for i in jetton]
    bet      = [i * SBRate for i in bet]
    totalPot = totalPot * SBRate
    if SBRate == 2:
	smallBlind =smallBlind*2
##    if jetton[-1] >= 6000:
##        ActionMsg = ActionDecisionBottomOverwhelm(prob, money, jetton, bet, totalPot, stage, playerNum, currentGameNum, isButton, raiseInfo, totalNum, ACIB, learnAdjustRate, smallBlind, blindInfo)
##    else:
##        if MoneyJettonSB == 3:
##            ActionMsg = ActionDecisionBottomGuard(prob, money, jetton, bet, totalPot, stage, playerNum, currentGameNum, isButton, raiseInfo, totalNum, ACIB, learnAdjustRate, smallBlind, blindInfo)
##        else:
##            if (currentGameNum <= 60) or (currentGameNum > 160 and currentGameNum <= 220) or (currentGameNum > 320 and currentGameNum <= 380) or (currentGameNum > 480 and currentGameNum <= 540):
##                ActionMsg = ActionDecisionBottomAggressive(prob, money, jetton, bet, totalPot, stage, playerNum, currentGameNum, isButton, raiseInfo, totalNum, ACIB, learnAdjustRate, smallBlind, blindInfo)
##            else:
##                ActionMsg = ActionDecisionBottomGuard(prob, money, jetton, bet, totalPot, stage, playerNum, currentGameNum, isButton, raiseInfo, totalNum, ACIB, learnAdjustRate, smallBlind, blindInfo)
##

    if totalNum == 2:
        ActionMsg = ActionDecisionBottomSpursOneonone(prob, money, jetton, bet, totalPot, stage, playerNum, currentGameNum, isButton, raiseInfo, totalNum, ACIB, smallBlind, blindInfo, checkEnable)
    else:
        ActionMsg = ActionDecisionBottomSpurs(prob, money, jetton, bet, totalPot, stage, playerNum, currentGameNum, isButton, raiseInfo, totalNum, ACIB, smallBlind, blindInfo, checkEnable)

    if ActionMsg.find('raise') >= 0:
        if playerNum <= 3:
            if playerNum == 3:
                maxJetton = max((jettonWF[0] + bet[0]),(jettonWF[1] + bet[1]))
                jettonRate = (jettonWF[-1] + bet[-1]) / maxJetton
            else:
                jettonRate = (jettonWF[-1] + bet[-1]) / (jettonWF[0] + bet[0])
            
            if jettonRate >= 15:
                if (jettonWF[-1] + bet[-1]) >= 8000:
                    ActionMsg = 'raise ' + str(5 * int(int(ActionMsg[6:]) / SBRate))
                else:
                    ActionMsg = 'raise ' + str(int(int(ActionMsg[6:]) / SBRate))

            elif jettonRate >= 8:
                if (jettonWF[-1] + bet[-1]) >= 9000:
                    ActionMsg = 'raise ' + str(4 * int(int(ActionMsg[6:]) / SBRate))
                elif (jettonWF[-1] + bet[-1]) >= 7000:
                    ActionMsg = 'raise ' + str(2.5 * int(int(ActionMsg[6:]) / SBRate))
                else:
                    ActionMsg = 'raise ' + str(int(int(ActionMsg[6:]) / SBRate))

            elif jettonRate >= 6:
                if (jettonWF[-1] + bet[-1]) >= 10000:
                    ActionMsg = 'raise ' + str(4 * int(int(ActionMsg[6:]) / SBRate))
                elif (jettonWF[-1] + bet[-1]) >= 8000:
                    ActionMsg = 'raise ' + str(2.5 * int(int(ActionMsg[6:]) / SBRate))
                else:
                    ActionMsg = 'raise ' + str(int(int(ActionMsg[6:]) / SBRate))

            elif jettonRate >= 4:
                if (jettonWF[-1] + bet[-1]) >= 12000:
                    ActionMsg = 'raise ' + str(4 * int(int(ActionMsg[6:]) / SBRate))
                elif (jettonWF[-1] + bet[-1]) >= 10000:
                    ActionMsg = 'raise ' + str(2.5 * int(int(ActionMsg[6:]) / SBRate))
                else:
                    ActionMsg = 'raise ' + str(int(int(ActionMsg[6:]) / SBRate))

            else:
                ActionMsg = 'raise ' + str(int(int(ActionMsg[6:]) / SBRate))

        else:            
            ActionMsg = 'raise ' + str(int(int(ActionMsg[6:]) / SBRate))
    
    return ActionMsg

if __name__=="__main__":
    prob=0.8065
    money=[0, 0, 0, 2000, 2000, 2000, 0, 2000]
    jetton=[3294, 1960, 2220, 624, 3840, 4589, 214, 2781]
    jettonwf=[214, 2781]
    bet=[1040, 278]
    totalpot=4478
    stage=2
    validplayer=2
    totalplayer=2
    GAME=27
    isButton=101.02
    ACIB=0
    raiseinfo=1.9
    checkenable=0

    smallBlind = 20
    initialJetton = 2000
    initialMoney = 4000
    blindInfo = 3
    MoneyJettonSB = 1
    msg = ActionDecision(prob, money, jetton, bet, totalpot, stage, validplayer, GAME, isButton, raiseinfo, totalplayer, ACIB, smallBlind, initialJetton, initialMoney, MoneyJettonSB, blindInfo, checkenable, jettonwf)
    print msg
     
