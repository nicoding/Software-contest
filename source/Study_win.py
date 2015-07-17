from Evaluate import EvaluateMyCard
from random import randint
import copy
import sys
import thread
import traceback



opponentInfoAll = {}
opponentInfoAllCache1 = {}
opponentInfoAllCache2 = {}
##opponentInfoRecent20 = {}
#{'111':[2,3,1,2,3]}
oppStage2Live = {}
oppStage2Raise = {}
oppStage2LiveC1 = {}
oppStage2RaiseC1 = {}
oppStage2LiveC2 = {}
oppStage2RaiseC2 = {}


oppHisWinProb = {}


#{'111':{'all_in':[0.7,0.8,0.95...],'raise':[0.4,0.6]},'222':{'raise':[0.5,0.6]}}

oppActionTmp = {}
oppActionTmpFormer = {}
#{'111':{'all_in':cardNum,'raise':cardNum}}
#cardNum:2,5,6,7

##all_in:1
##raise:2
##call:3
##check:4
##fold:5

BID=0
bets = {}
#{ '111':1000, '222':2000, 'my': 40}


markFold = {}


IDs_An ={}
colors_An = []
points_An = []
pubCol_An = []
pubPot_An = []


analyzeRecDoneMark = False
#one rec duiying one analyze




actionDic = {'all_in':1,
             'raise':2,
             'call':3,
             'check':4,
             'fold':5,
             'blind':6,
             'raise_500':7,
             'raise_1000':8,
             'raise_40000':9}

buttonDic = {0:{0:1.000, 1:0.998, 2:0.990, 3:0.982, 4:0.974, 5:0.966, 6:0.958, 7:0.950},
	      1:{0:1.020, 1:1.000, 2:0.998, 3:0.990, 4:0.982, 5:0.974, 6:0.966},
	      2:{0:1.030, 1:1.020, 2:1.000, 3:0.998, 4:0.990, 5:0.982},
	      3:{0:1.045, 1:1.030, 2:1.020, 3:1.000, 4:0.998},
	      4:{0:1.064, 1:1.045, 2:1.030, 3:1.020},
	      5:{0:1.080, 1:1.064, 2:1.045},
	      6:{0:1.095, 1:1.080},
	      7:{0:1.110}}

# raiseDogDic = {2 : 1.075,
#                5 : 1.255,
#                6 : 1.291,
#                7 : 1.469}

#raiseReduceDic = {2 : 0.9553,
#                  5 : 0.9316,
#                  6 : 0.9210,
#                  7 : 0.8776}


tmpDFixConst = {1000:1000,
           600 :600,
           500 :500,
           400 :400,
           300 :300,
           120 :120}
tmpDFix = {1000:1000,
           600 :600,
           500 :500,
           400 :400,
           300 :300,
           120 :120}

### 7_11
BBBLF={}
SBBLF={}
BBAC={}
SBAC={}




gameformer = 0
def zhstest(f,game):
       try:
              global gameformer
              if game!=gameformer:
                     gameformer = game 
                     global oppStage2Live
                     global oppStage2Raise

                     global opponentInfoAll
                     global oppHisWinProb

                     
                     global BBBLF
                     global SBBLF
                     global BBAC
                     global SBAC

                     
                     f.write('\n----------------------'+str(game)+'-------------------\n')
                     for ID in oppStage2Live.keys():
                            f.write(str(ID)+':\n')
                            f.write('\toppStage2Live:\t'+str(len(oppStage2Live[ID]))+'\n')
                            f.write('\toppStage2Raise:\t'+str(len(oppStage2Raise[ID]))+'\n')
                            if len(oppStage2Live[ID])!=0:
                                   f.write('\tstage2raiserate:\t'+str(float(len(oppStage2Raise[ID]))/len(oppStage2Live[ID]))+'\n')
                            f.write('\traiseRate:\t'+str((opponentInfoAll[ID].count(2)+opponentInfoAll[ID].count(1))/float(game))+'\n')
                            f.write('\tBBAC:\t'+str(BBAC[ID])+'\n')
                            f.write('\tBBBLF:\t'+str(BBBLF[ID])+'\n')
                            f.write('\tSBAC:\t'+str(SBAC[ID])+'\n')
                            f.write('\tSBBLF:\t'+str(SBBLF[ID])+'\n')
                            f.write('\toppHisWinProb:\n')
                            for action in oppHisWinProb[ID].keys():
                                   f.write('\t\taction:\t'+str(action)+':'+str(oppHisWinProb[ID][action])+'\n')
                                   
                            


                     f.write('\n')
       except:
              print '***********************error in zhstest*******************'




def opponentInfoInitial(IDs):
       global opponentInfoAll
       global opponentInfoAllCache1
       global opponentInfoAllCache2
       global oppHisWinProb
       global oppActionTmp
       
       global oppStage2Live
       global oppStage2Raise
       
       global oppStage2LiveC1
       global oppStage2RaiseC1
       
       global oppStage2LiveC2
       global oppStage2RaiseC2

       
       global BBBLF
       global SBBLF

       global BBAC
       global SBAC
       
       for ID in IDs:
              opponentInfoAll[ID]=[]
              opponentInfoAllCache1[ID]=[]
              opponentInfoAllCache2[ID]=[]
              oppHisWinProb[ID] = {}
              oppActionTmp[ID] = {}
              oppStage2Live[ID] = []
              oppStage2Raise[ID] = []
              oppStage2LiveC1[ID] = []
              oppStage2RaiseC1[ID] = []
              oppStage2LiveC2[ID] = []
              oppStage2RaiseC2[ID] = []
              
              BBBLF[ID]=0
              SBBLF[ID]=0
              BBAC[ID]=0
              SBAC[ID]=0

              
def opponentInfoUpdataRepair(buttonID):
       global opponentInfoAll
       global oppActionTmp
       global markFold
       global bets
       global BID

       global oppStage2LiveC1
       global oppStage2RaiseC1
       
       BID = buttonID
       for ID in opponentInfoAll.keys():
              oppActionTmp[ID]={}
              markFold[ID]=0
              bets[ID] = 0
              opponentInfoAllCache1[ID] = []
              oppStage2LiveC1[ID]=[]
              oppStage2RaiseC1[ID]=[]


def fixSB(SB):
       global tmpDFix
       global tmpDFixO
       
       try:
              for i in tmpDFix.keys():
                     tmpDFix[i]= tmpDFixConst[i]*(float(SB)/20.0)
       except:
              tmpDFix = tmpDFixConst
              print '****************error**************'
              print 'tmpDFix = tmpDFixConst in opponentInfoUpdataRepair'
              print '******************************'


def oppoAnalyzeRec(IDs, colors, points, pubCol, pubPot):
       global IDs_An
       global colors_An
       global points_An
       global pubCol_An
       global pubPot_An
       global analyzeRecDoneMark
       
       IDs_An = copy.deepcopy(IDs)
       colors_An = copy.deepcopy(colors)
       points_An = copy.deepcopy(points)
       pubCol_An = copy.deepcopy(pubCol)
       pubPot_An = copy.deepcopy(pubPot)
       analyzeRecDoneMark = True


markFoldFormer = {}
betsFormer = {}

IDSFormers = []
actionFormers = []
nowBetsFormers = []
cardNumFormers = []
playerNumFormers = []
numFormer = 0


def startRec():
       global oppActionTmpFormer
       global oppActionTmp
       oppActionTmpFormer = copy.deepcopy(oppActionTmp)

       global markFoldFormer
       global markFold
       markFoldFormer = copy.deepcopy(markFold)

       global betsFormer
       global bets
       betsFormer = copy.deepcopy(bets)

       global opponentInfoAllCache1
       global opponentInfoAllCache2
       opponentInfoAllCache2 = copy.deepcopy(opponentInfoAllCache1)

       global oppStage2LiveC1
       global oppStage2RaiseC1
       global oppStage2LiveC2
       global oppStage2RaiseC2
       oppStage2LiveC2 = copy.deepcopy(oppStage2LiveC1)
       oppStage2RaiseC2 = copy.deepcopy(oppStage2RaiseC1)


def startRecNoNotify():
       global oppActionTmpFormer
       global oppActionTmp
       oppActionTmpFormer = copy.deepcopy(oppActionTmp)

     
  
def endRec():
       global opponentInfoAll
       global opponentInfoAllCache2
       for ID in opponentInfoAll.keys():
              if opponentInfoAllCache2.has_key(ID):
                     if opponentInfoAllCache2[ID]:
                            opponentInfoAll[ID].append(opponentInfoAllCache2[ID][0])
                     else:
                            opponentInfoAll[ID].append(5)


       global oppStage2Live
       global oppStage2Raise
       global oppStage2LiveC1
       global oppStage2RaiseC1
       global oppStage2LiveC2
       global oppStage2RaiseC2

       for ID in oppStage2Live.keys():
              if oppStage2RaiseC2.has_key(ID):
                     if len(oppStage2RaiseC2[ID])!=0:
                            oppStage2Raise[ID].append(oppStage2RaiseC2[ID][0])
                            del oppStage2RaiseC2[ID][0]
              if oppStage2LiveC2.has_key(ID):
                     if len(oppStage2LiveC2[ID])!=0:
                            oppStage2Live[ID].append(oppStage2LiveC2[ID][0])
                            del oppStage2LiveC2[ID][0]

       global IDSFormers
       global actionFormers
       global nowBetsFormers
       global cardNumFormers
       global playerNumFormers

       IDSFormers = []
       actionFormers = []
       nowBetsFormers = []
       cardNumFormers = []
       playerNumFormers = []


def endRecNoNotify():
       global opponentInfoAll
       global opponentInfoAllCache1
       for ID in opponentInfoAll.keys():
              if opponentInfoAllCache1.has_key(ID):
                     if opponentInfoAllCache1[ID]:
                            opponentInfoAll[ID].append(opponentInfoAllCache1[ID][0])
                     else:
                            opponentInfoAll[ID].append(5)

       global oppStage2Live
       global oppStage2Raise
       global oppStage2LiveC1
       global oppStage2RaiseC1

       for ID in oppStage2Live.keys():
              if oppStage2RaiseC1.has_key(ID):
                     if len(oppStage2RaiseC1[ID])!=0:
                            oppStage2Raise[ID].append(oppStage2RaiseC1[ID][0])
              if oppStage2LiveC1.has_key(ID):
                     if len(oppStage2LiveC1[ID])!=0:
                            oppStage2Live[ID].append(oppStage2LiveC1[ID][0])



def opponentInfoUpdataRec(IDs, action, nowBets, cardNum, playerNum, num):

       global IDSFormers
       global actionFormers
       global nowBetsFormers
       global cardNumFormers
       global playerNumFormers
       global numFormer


       IDSFormers.append(IDs)
       actionFormers.append(action)
       nowBetsFormers.append(nowBets)
       cardNumFormers.append(cardNum)
       playerNumFormers.append(playerNum)
       numFormer = num


def  oppoAnalyzeThread():
       pass
##       global analyzeRecDoneMark
##       if analyzeRecDoneMark:
##              analyzeRecDoneMark = False
##              thread.start_new_thread(oppoAnalyze, (1,))
##       else:
##              pass



def oppoAnalyze(noUse):  #when showdown, do it
       global oppHisWinProb
       oppHisWinProb_bak = copy.deepcopy(oppHisWinProb)

       global IDs_An
       global colors_An
       global points_An
       global pubCol_An
       global pubPot_An
       global oppActionTmpFormer
       
       IDs = IDs_An
       colors = colors_An
       points = points_An
       pubCol = pubCol_An
       pubPot = pubPot_An
       oppActionTmp = oppActionTmpFormer


       
       try:
              for i,ID in enumerate(IDs):
                     if oppActionTmp.has_key(ID):
                            if oppActionTmp[ID].has_key(actionDic['all_in']):
                                   cardNum = (oppActionTmp[ID][actionDic['all_in']])%10
                                   playerNum = (oppActionTmp[ID][actionDic['all_in']])/10
                                   if cardNum in [5,6,7] and playerNum in range(2,9):
                                          p = EvaluateMyCard(colors[i]+pubCol[:cardNum-2],points[i]+pubPot[:cardNum-2],playerNum)
                     ##                     print '****************************************************'
                     ##                     print p
                     ##                     print colors[i]+pubCol[:cardNum-2]
                     ##                     print points[i]+pubPot[:cardNum-2]
                     ##                     print '****************************************************'
                                          if oppHisWinProb[ID].has_key(actionDic['all_in']):
                                                 oppHisWinProb[ID][actionDic['all_in']].append(p)
                                          else:
                                                 oppHisWinProb[ID][actionDic['all_in']]=[p]

                            if oppActionTmp[ID].has_key(actionDic['raise']):
                                   for playerCardNum in oppActionTmp[ID][actionDic['raise']]:
                                          cardNum = playerCardNum%10
                                          playerNum = playerCardNum/10
                                          if cardNum in [5,6,7] and playerNum in range(2,9):
                                                 p = EvaluateMyCard(colors[i]+pubCol[:cardNum-2],points[i]+pubPot[:cardNum-2],playerNum)
                                                 if oppHisWinProb[ID].has_key(actionDic['raise']):
                                                        oppHisWinProb[ID][actionDic['raise']].append(p)
                                                 else:
                                                        oppHisWinProb[ID][actionDic['raise']]=[p]

                            if oppActionTmp[ID].has_key(actionDic['raise_500']):
                                   for playerCardNum in oppActionTmp[ID][actionDic['raise_500']]:
                                          cardNum = playerCardNum%10
                                          playerNum = playerCardNum/10
                                          if cardNum in [5,6,7] and playerNum in range(2,9):
                                                 p = EvaluateMyCard(colors[i]+pubCol[:cardNum-2],points[i]+pubPot[:cardNum-2],playerNum)
                                                 if oppHisWinProb[ID].has_key(actionDic['raise_500']):
                                                        oppHisWinProb[ID][actionDic['raise_500']].append(p)
                                                 else:
                                                        oppHisWinProb[ID][actionDic['raise_500']]=[p]

                            if oppActionTmp[ID].has_key(actionDic['raise_1000']):
                                   for playerCardNum in oppActionTmp[ID][actionDic['raise_1000']]:
                                          cardNum = playerCardNum%10
                                          playerNum = playerCardNum/10
                                          if cardNum in [5,6,7] and playerNum in range(2,9):
                                                 p = EvaluateMyCard(colors[i]+pubCol[:cardNum-2],points[i]+pubPot[:cardNum-2],playerNum)
                                                 if oppHisWinProb[ID].has_key(actionDic['raise_1000']):
                                                        oppHisWinProb[ID][actionDic['raise_1000']].append(p)
                                                 else:
                                                        oppHisWinProb[ID][actionDic['raise_1000']]=[p]

                            if oppActionTmp[ID].has_key(actionDic['raise_40000']):
                                   for playerCardNum in oppActionTmp[ID][actionDic['raise_40000']]:
                                          cardNum = playerCardNum%10
                                          playerNum = playerCardNum/10
                                          if cardNum in [5,6,7] and playerNum in range(2,9):
                                                 p = EvaluateMyCard(colors[i]+pubCol[:cardNum-2],points[i]+pubPot[:cardNum-2],playerNum)
                                                 if oppHisWinProb[ID].has_key(actionDic['raise_40000']):
                                                        oppHisWinProb[ID][actionDic['raise_40000']].append(p)
                                                 else:
                                                        oppHisWinProb[ID][actionDic['raise_40000']]=[p]
       except:
              print '***************************************************************'
              print '***************************************************************'
              print 'hello~~zhs~~error~~in oppoAnalyze~~'
              print '***************************************************************'
              print '***************************************************************'
              oppHisWinProb = oppHisWinProb_bak

       thread.exit_thread()





formerIsBigBlind={}
# {1:349}
formerIsSmallBlind={}
# {1:349}




def opponentInfoUpdataFormer():
       global opponentInfoAllCache2
       global oppActionTmpFormer

       global markFoldFormer
       global betsFormer

       global actionFormers
       global IDSFormers
       global nowBetsFormers
       global cardNumFormers
       global playerNumFormers
       global tmpDFix

       global numFormer
              
       global oppStage2LiveC2
       global oppStage2RaiseC2

       ###    7_11  BBBLF recognize ###
       global formerIsBigBlind
       # {1:349}
       global formerIsSmallBlind
       # {1:349}
       
       bigBlindID = -1
       smallBlindID = -1

       global BBBLF
       global SBBLF
       global BBAC
       global SBAC
       if formerIsBigBlind.has_key(numFormer):
              bigBlindID = formerIsBigBlind[numFormer]
       if formerIsSmallBlind.has_key(numFormer):
              smallBlindID = formerIsSmallBlind[numFormer]
       guoLeSmallBlind_7_11 = False
       guoLeBigBlind_7_11 = False

       restBBCheck = True
       restSBCheck = True

       BBRaise = False
       SBRaise = False
       


##       print '##############################################'
##       print  opponentInfoAllCache2
##       print  oppActionTmpFormer
##       print  markFoldFormer
##       print betsFormer
##       print actionFormers
##       print IDSFormers
##       print nowBetsFormers
##       print cardNumFormers
##       print playerNumFormers
##       print '##############################################'

       while IDSFormers:
              actionFormer = actionFormers.pop(0)
              IDSFormer = IDSFormers.pop(0)
              nowBetsFormer = nowBetsFormers.pop(0)
              cardNumFormer = cardNumFormers.pop(0)
              playerNumFormer = playerNumFormers.pop(0)

              if not oppActionTmpFormer:
                     for ID in opponentInfoAllCache2.keys():
                            oppActionTmpFormer[ID] = {}


##########################   hit kb   part1    #########################
              firstRaiseID = 'zhsInitial'
              for i,ID in enumerate(IDSFormer):
                     if opponentInfoAllCache2.has_key(ID):
                            if actionFormer[i]=='raise' or actionFormer[i]=='all_in':
                                   firstRaiseID = ID

              guoLeFirstRaiseID = False
##########################    end 1    #########################
              

              for i,ID in enumerate(IDSFormer):
                     if opponentInfoAllCache2.has_key(ID):
                            ###############  7_11 #############  BBBLF


                            if guoLeBigBlind_7_11 and (actionFormer[i]=='raise' or actionFormer[i]=='all_in'):
                                   restBBCheck = False
                            if guoLeSmallBlind_7_11 and (actionFormer[i]=='raise' or actionFormer[i]=='all_in'):
                                   restSBCheck = False

                                   
                            if ID == bigBlindID :
                                   guoLeBigBlind_7_11 = True
                                   if actionFormer[i] == 'raise' or actionFormer[i] == 'all_in':
                                          BBRaise = True
                            if ID == smallBlindID :
                                   guoLeSmallBlind_7_11 = True
                                   if actionFormer[i] == 'raise' or actionFormer[i] == 'all_in':
                                          SBRaise = True

                            tmpD = nowBetsFormer[i] - betsFormer[ID]
                            if  tmpD <= tmpDFix[400] and tmpD > 0 and actionFormer[i] == 'all_in':
                                   if nowBetsFormer[i+1] < nowBetsFormer[i]:
                                          actionFormer[i] = 'raise'
                                   else:
                                          actionFormer[i] = 'call'              
                            betsFormer[ID] =  nowBetsFormer[i]


                            ##########################   hit kb   part2    #########################
                            if actionFormer[i]!='fold':
                                   if cardNumFormer==5:
                                          if oppStage2LiveC2[ID].count(numFormer)==0:
                                                 oppStage2LiveC2[ID].append(numFormer)
                                          if actionFormer[i]=='raise' and oppStage2RaiseC2[ID].count(numFormer)==0:
                                                 oppStage2RaiseC2[ID].append(numFormer)
                            else:
                                   if cardNumFormer==5 and firstRaiseID != 'zhsInitial':
                                          if guoLeFirstRaiseID == False and markFoldFormer[ID]==0:
                                                 if oppStage2LiveC2[ID].count(numFormer)==0:
                                                        oppStage2LiveC2[ID].append(numFormer)

                            if firstRaiseID==ID:
                                   guoLeFirstRaiseID = True
                            ##########################    end 2    #########################
                                   
                            if not opponentInfoAllCache2[ID]:
                                   opponentInfoAllCache2[ID].append(actionDic[actionFormer[i]])
                                   if actionFormer[i] =='fold':
                                         markFoldFormer[ID]=1 
                            else:
                                   if opponentInfoAllCache2[ID][-1] !=  1 and opponentInfoAllCache2[ID][-1] !=  5 :
                                          if opponentInfoAllCache2[ID][-1] !=  2:
                                                 opponentInfoAllCache2[ID][-1] = actionDic[actionFormer[i]]
                                          else:
                                                 if actionDic[actionFormer[i]] == 2:
                                                        opponentInfoAllCache2[ID][-1] = actionDic[actionFormer[i]]
                                                        
                                   if actionFormer[i] =='fold':
                                          if markFoldFormer[ID]==0:
                                                 markFoldFormer[ID]=1
                                          elif markFoldFormer[ID]==1:
                                                 markFoldFormer[ID]=2


                                   
                            if actionFormer[i]=='all_in':
                                   
                                   if not oppActionTmpFormer[ID].has_key(actionDic['all_in']):
                                          tmp = 0
                                          for j,act in enumerate(actionFormer[:i]):
                                                 if act == 'fold' and markFoldFormer[IDSFormer[j]]!=2:
                                                        tmp+=1
                                          oppActionTmpFormer[ID][actionDic['all_in']]=(playerNumFormer+tmp)*10+cardNumFormer
               

                                                 
                            elif actionFormer[i] == 'raise': 
                            
	                           if tmpD > tmpDFix[1000] :
                                          tmpR = 40000
	                           elif tmpD > tmpDFix[500] :
                                          tmpR = 1000
	                           else :
                                          tmpR = 500
                                                 
                                   tmp = 0
                                   for j,act in enumerate(actionFormer[:i]):
                                          if act == 'fold' and markFoldFormer[IDSFormer[j]]!=2:
                                                 tmp+=1
                                                 
                                   if not oppActionTmpFormer[ID].has_key(actionDic['raise_'+str(tmpR)]):
                                          oppActionTmpFormer[ID][actionDic['raise_'+str(tmpR)]]=[(playerNumFormer+tmp)*10+cardNumFormer]
                                   else:
                                          oppActionTmpFormer[ID][actionDic['raise_'+str(tmpR)]].append((playerNumFormer+tmp)*10+cardNumFormer)

              if bigBlindID!=-1 :
                     if restBBCheck:
                            BBAC[bigBlindID] +=1
                            if BBRaise:
                                   BBBLF[bigBlindID] +=1
                     try:
                            del formerIsBigBlind[numFormer]
                     except:
                            pass
              if smallBlindID !=-1:
                     if restSBCheck:
                            SBAC[smallBlindID] +=1
                            if SBRaise: 
                                   SBBLF[smallBlindID] +=1
                     try:
                            del formerIsSmallBlind[numFormer]
                     except:
                            pass









#only action no us
def opponentInfoUpdata(IDs, action, jetton ,nowBets, num, cardNum, playerNum, playerNumWithFold, prob):
       global opponentInfoAllCache1
       global opponentInfoAll
       global oppActionTmp
       global markFold
       global oppHisWinProb
       global bets
       global BID
 #      global raiseDogDic
 #      global raiseReduceDic
       global tmpDFix


       
       global oppStage2LiveC1
       global oppStage2RaiseC1



       
       oppHisWinProbTmpAllIn={}
       #{'111':[0.7,0.6],'222':[0.8,0.9]}
       oppHisWinProbTmpRaise={}
       allCheck = True
       a = 1
       isButton = False
       betWithOutFold =[]
       jettonWithoutFold = []
       alla = [1]
       
       checkEnable= 0
       IDBehindMe = []
       IDFrontMe = []

       global formerIsBigBlind
       # {1:349}
       global formerIsSmallBlind
       # {1:349}

       IDBlind = []
       #first is big blind
       # if i'm not big blind and not small blind
       # len(IDBlind)==2
       # if i'm big blind
       # len(IDBlind)==0
       # if i'm small blind
       # len()==1
       # if two people
       # hehe
       bigBlindID = -1
       smallBlindID = -1

       global BBBLF
       global SBBLF
       global BBAC
       global SBAC

       if formerIsBigBlind.has_key(num):
              bigBlindID = formerIsBigBlind[num]
       if formerIsSmallBlind.has_key(num):
              smallBlindID = formerIsSmallBlind[num]

       guoLeSmallBlind_7_11 = False
       guoLeBigBlind_7_11 = False

       restBBCheck = True
       restSBCheck = True

       BBRaise = False
       SBRaise = False

       raiseRatioNP = 0.21 # raise: nomal people
       raiseRatioLR = 0.25 # raise: like raise people
       rasieRatioSRD = 0.30 # raise: small rasie dog
       raiseRatioMRD = 0.35 # raise: mid raise dog
       
       opponentInfoAllCache1_bak = copy.deepcopy(opponentInfoAllCache1)
       oppActionTmp_bak = copy.deepcopy(oppActionTmp)
       markFold_bak = copy.deepcopy(markFold)

       if not cardNum in [2,5,6,7]:
              cardNum = 2

       if not oppActionTmp:
              for ID in opponentInfoAllCache1.keys():
                     oppActionTmp[ID] = {}

       try:
              try:
                     front = 0
                     behind = 0
                     guoLeWo = False
                     if BID in IDs:
                            indexOfNow = IDs.index(BID)
                            for i in range(len(IDs)):
                                   if opponentInfoAllCache1.has_key(IDs[indexOfNow]):
                                          if action[indexOfNow] != 'fold':
                                                 if guoLeWo:
                                                        front += 1
                                                        IDFrontMe.append(IDs[indexOfNow])
                                                 else :
                                                        behind += 1
                                                        IDBehindMe.append(IDs[indexOfNow])
                                   else:
                                          guoLeWo = True

                                   indexOfNow +=1
                                   if indexOfNow == len(IDs):
                                          indexOfNow =0
                            if cardNum ==2:
                                   if BID == IDs[-1]:
                                          front = max([front-action.count('blind'),0])
                                          behind = max(min(behind + 2, playerNum - 1 - front), 0)
                                   elif BID == IDs[0]:
                                          front = max([len(action) - action.count('fold') - action.count('blind'),0])
                                          behind = max(min(1, playerNum - 1 - front), 0)
                                   elif BID == IDs[1]:
                                          front = len(action) - action.count('fold')
                                          behind = 0
                     else:
                            front = len(action) - 2 - action.count('fold')
                            behind = playerNum- 1 - front
              except:
                     print '***************************************************************'
                     print '***************************************************************'
                     info=sys.exc_info()
                     print info[0],":",info[1]
                     print 'hello~~zhs~~error~~in opponentInfoUpdata button hehe~~'
                     print '***************************************************************'
                     print '***************************************************************'

##########################   hit kb   part1    #########################
              firstRaiseID = 'zhsInitial'
              for i,ID in enumerate(IDs):
                     if opponentInfoAllCache1.has_key(ID):
                            if action[i]=='raise' or action[i]=='all_in':
                                   firstRaiseID = ID

              guoLeFirstRaiseID = False
##########################    end 1    #########################

              for i,ID in enumerate(IDs):
                     if opponentInfoAllCache1.has_key(ID):
                            ############ 7_11 blind bullf #############


                            if guoLeBigBlind_7_11 and (action[i]=='raise' or action[i]=='all_in'):
                                   restBBCheck = False
                            if guoLeSmallBlind_7_11 and (action[i]=='raise' or action[i]=='all_in'):
                                   restSBCheck = False
                                   
                            if ID == bigBlindID :
                                   guoLeBigBlind_7_11 = True
                                   if action[i] == 'raise' or action[i] == 'all_in':
                                          BBRaise = True
                            if ID == smallBlindID :
                                   guoLeSmallBlind_7_11 = True
                                   if action[i] == 'raise' or action[i] == 'all_in':
                                          SBRaise = True
                                   
              ##              print '***********************************************'
              ##              print bets
              ##              print nowBets
              ##              print '***********************************************'

                            tmpD = nowBets[i] - bets[ID]
                            if  tmpD <= tmpDFix[400] and tmpD > 0 and action[i] == 'all_in':
                                   if nowBets[i+1] < nowBets[i]:
                                          action[i] = 'raise'
                                   else:
                                          action[i] = 'call'
                            #################  7_7 ##################
                            if tmpD == 0 and action[i]=='raise':
                                   action[i]='call'

                            #################  end ##################
                                          
                            bets[ID] =  nowBets[i]

                            
                            ##########################   hit kb   part2    #########################
                            if action[i]!='fold':
                                   betWithOutFold.append(nowBets[i])
                                   jettonWithoutFold.append(jetton[i])
                                   if cardNum==5:
                                          if oppStage2LiveC1[ID].count(num)==0:
                                                 oppStage2LiveC1[ID].append(num)
                                          if action[i]=='raise' and oppStage2RaiseC1[ID].count(num)==0:
                                                 oppStage2RaiseC1[ID].append(num)
                            else:
                                   if cardNum==5 and firstRaiseID != 'zhsInitial':
                                          if guoLeFirstRaiseID == False and markFold[ID]==0:
                                                 if oppStage2LiveC1[ID].count(num)==0:
                                                        oppStage2LiveC1[ID].append(num)

                            if firstRaiseID==ID:
                                   guoLeFirstRaiseID = True
                            ##########################    end 2    #########################

                                   
                                   
                            if not opponentInfoAllCache1[ID]:
                                   opponentInfoAllCache1[ID].append(actionDic[action[i]])
                                   if action[i] =='fold':
                                         markFold[ID]=1 
                            else:
                                   if opponentInfoAllCache1[ID][-1] !=  1 and opponentInfoAllCache1[ID][-1] !=  5 :
                                          if opponentInfoAllCache1[ID][-1] != 2:
                                                 opponentInfoAllCache1[ID][-1] = actionDic[action[i]]
                                          else:
                                                 if actionDic[action[i]] == 2:
                                                        opponentInfoAllCache1[ID][-1] = actionDic[action[i]]
                                                        
                                   if action[i] =='fold':
                                          if markFold[ID]==0:
                                                 markFold[ID]=1
                                          elif markFold[ID]==1:
                                                 markFold[ID]=2


                            # # there maybe some problems, but it's never mind to button
                            if action[i] != 'check':
                                   allCheck = False
                                   
                            if action[i]=='all_in':
                                   if oppHisWinProb.has_key(ID):
                                          if oppHisWinProb[ID].has_key(actionDic['all_in']):
                                                 oppHisWinProbTmpAllIn[ID]=oppHisWinProb[ID][actionDic['all_in']]

                                   
                                   if not oppActionTmp[ID].has_key(actionDic['all_in']):
                                          tmp = 0
                                          for j,act in enumerate(action[:i]):
                                                 if act == 'fold' and markFold[IDs[j]]!=2:
                                                        tmp+=1
                                          oppActionTmp[ID][actionDic['all_in']]=(playerNum+tmp)*10+cardNum

                                   raiseAllRatio = (opponentInfoAll[ID].count(2)+opponentInfoAll[ID].count(1))/float(num)
                                   if raiseAllRatio <raiseRatioNP  or num <10:
                                          if tmpD > tmpDFix[1000]:
                                                 a=0.1
                                                 alla.append(a)
                                          elif tmpD > tmpDFix[400]:
                                                 a=0.4
                                                 alla.append(a)
                                   elif raiseAllRatio <raiseRatioLR:
                                          if tmpD > tmpDFix[1000]:
                                                 a=0.3
                                                 alla.append(a)
                                          elif tmpD > tmpDFix[400]:
                                                 a=0.6
                                                 alla.append(a)
                                   elif raiseAllRatio <rasieRatioSRD:
                                          if tmpD > tmpDFix[1000]:
                                                 a=0.4
                                                 alla.append(a)
                                          elif tmpD > tmpDFix[400]:
                                                 a=0.7
                                                 alla.append(a)
                                   elif raiseAllRatio <raiseRatioMRD:
                                          if tmpD > tmpDFix[1000]:
                                                 a=0.5
                                                 alla.append(a)
                                          elif tmpD > tmpDFix[400]:
                                                 a=0.8
                                                 alla.append(a)
                                   else:
                                          alla.append(0.9)
                                                 
                            elif action[i] == 'raise':

                                   hellozhs = True

                                   if cardNum==5 and len(oppStage2Live[ID])>=3:
                                          zhstmp = float(len(oppStage2Raise[ID]))/len(oppStage2Live[ID])
                                          if zhstmp>=0.85:
                                                 alla.append(1.6 + randint(1,4)/10.0)
                                                 hellozhs = False
                                          elif zhstmp>=0.75:
                                                 alla.append(1.3 + randint(1,4)/10.0)
                                                 hellozhs = False
                                          elif zhstmp>=0.65:
                                                 alla.append(1 + randint(1,4)/10.0)
                                                 hellozhs = False
                                                 
                                   if hellozhs:
                                          if tmpD > tmpDFix[1000] :
                                                 tmpR = 40000
                                          elif tmpD > tmpDFix[500] :
                                                 tmpR = 1000
                                          else :
                                                 tmpR = 500

                                          if oppHisWinProb.has_key(ID):
                                                 if oppHisWinProb[ID].has_key(actionDic['raise_'+str(tmpR)]):
                                                        oppHisWinProbTmpRaise[ID]=oppHisWinProb[ID][actionDic['raise_'+str(tmpR)]]
                                                        
                                          tmp = 0
                                          for j,act in enumerate(action[:i]):
                                                 if act == 'fold' and markFold[IDs[j]]!=2:
                                                        tmp+=1
                                              
                                          if not oppActionTmp[ID].has_key(actionDic['raise_'+str(tmpR)]):
                                                 oppActionTmp[ID][actionDic['raise_'+str(tmpR)]]=[(playerNum+tmp)*10+cardNum]
                                          else:
                                                 oppActionTmp[ID][actionDic['raise_'+str(tmpR)]].append((playerNum+tmp)*10+cardNum)

                                          raiseAllRatio = (opponentInfoAll[ID].count(2)+opponentInfoAll[ID].count(1))/float(num)
                                          
                                          if raiseAllRatio <raiseRatioNP or num<10:  # nomarl people
                                                 if tmpD > tmpDFix[600]:
                                                        a = 0.2
                                                        alla.append(a)
                                                 elif tmpD > tmpDFix[300]:
                                                        a = 0.5
                                                        alla.append(a)
                                                 elif tmpD > tmpDFix[120]:
                                                        a = 0.7
                                                        alla.append(a)
                                                 else:
                                                        a = 0.9
                                                        alla.append(a)
                                          elif raiseAllRatio <=raiseRatioLR:  # like rasie people
                                                 if tmpD > tmpDFix[600]:
                                                        a = 0.8
                                                        alla.append(a)
                                                 elif tmpD > tmpDFix[300]:
                                                        a = 0.85
                                                        alla.append(a)
                                                 elif tmpD > tmpDFix[120]:
                                                        a = 0.9
                                                        alla.append(a)
                                                 else:
                                                        a = 0.95
                                                        alla.append(a)
                                          elif raiseAllRatio >raiseRatioMRD and num>20:  # big raise dog
                                                 alla.append(1.6 + randint(1,4)/10.0)
                                          elif raiseAllRatio >rasieRatioSRD and num>20:  # mid raise dog
                                                 alla.append(1.3 + randint(1,4)/10.0)
                                          else:  # small raise dog or (num 10-20 and big raise dog)
                                                 alla.append(1 + randint(1,4)/10.0)
                            elif action[i]=='blind':
                                   ########################## recognize big blind #################
                                   if cardNum==2 and len(alla)==1 and playerNumWithFold>2:
                                          IDBlind.append(ID)
                                          

              betWithOutFold.append(nowBets[-1])
              jettonWithoutFold.append(jetton[-1])

              if bigBlindID!=-1 :
                     if restBBCheck:
                            BBAC[bigBlindID] +=1
                            if BBRaise:
                                   BBBLF[bigBlindID] +=1
                     try:
                            del formerIsBigBlind[num]
                     except:
                            pass
              if smallBlindID !=-1:
                     if restSBCheck:
                            SBAC[smallBlindID] +=1
                            if SBRaise: 
                                   SBBLF[smallBlindID] +=1
                     try:
                            del formerIsSmallBlind[num]
                     except:
                            pass
              

              if len(IDBlind)==2:
                     formerIsBigBlind[num] = IDBlind[0]
                     formerIsSmallBlind[num] = IDBlind[1]
              elif len(IDBlind)==1:
                     formerIsBigBlind[num] = IDBlind[0]
              else:
                     pass

              if min(alla) >=1:
                     if max(alla)>1:
                            alla.remove(1)
                            raiseInfo = min(alla)
                     else:
                            raiseInfo = 1
              else:
                     raiseInfo = min(alla)

              a = buttonDic[front][behind]

              if (raiseInfo==1) and (behind ==0):
                     ACIB = 1
              else:
                     ACIB = 0

              ## when cardNum ==2 ,we use this way to decide checkEnble

              if cardNum ==2:
                     if formerIsBigBlind.has_key(num):
                            if BBAC[formerIsBigBlind[num]]>0:
                                   if BBBLF[formerIsBigBlind[num]]/float(BBAC[formerIsBigBlind[num]])>=0.7 and BBBLF[formerIsBigBlind[num]]>=3:
                                          checkEnable = 1
                     if formerIsSmallBlind.has_key(num):
                            if SBAC[formerIsSmallBlind[num]]>0:
                                   if SBBLF[formerIsSmallBlind[num]]/float(SBAC[formerIsSmallBlind[num]])>=0.7 and SBBLF[formerIsSmallBlind[num]]>=3:
                                          checkEnable = 1
                            
                                   

                     
              ## when cardNum >2, we use this way to decide checkEnable
              if (raiseInfo==1) and (playerNum<=4) and cardNum>2:
                     for i,ID in enumerate(IDBehindMe):
                            raiseAllRatio = (opponentInfoAll[ID].count(2)+opponentInfoAll[ID].count(1))/float(num)
                            if raiseAllRatio>raiseRatioNP:
                                   checkEnable = 1
                     
              return a,raiseInfo,oppHisWinProbTmpAllIn,oppHisWinProbTmpRaise,front*100+behind*10+buttonDic[front][behind],jettonWithoutFold,betWithOutFold,ACIB,checkEnable
       except:
              opponentInfoAllCache1 = opponentInfoAllCache1_bak
              oppActionTmp = oppActionTmp_bak
              markFold = markFold_bak
              print '***************************************************************'
              print '***************************************************************'
              info=sys.exc_info()
              print info[0],":",info[1]
              print 'hello~~zhs~~error~~in opponentInfoUpdata~~'
              traceback.print_exc(file=sys.stdout)
              print '***************************************************************'
              print '***************************************************************'
              betWithOutFold = []
              jettonWithoutFold = []
              for i,ID in enumerate(IDs):
                     if opponentInfoAllCache1.has_key(ID):
                            if action [i]!='fold':
                                   jettonWithoutFold.append(jetton[i])
                                   betWithOutFold.append(nowBets[i])
              betWithOutFold.append(nowBets[-1])
              jettonWithoutFold.append(jetton[-1])
                            
              return 0.98,1,{},{},1,jettonWithoutFold,betWithOutFold,0,0








                            








                     
def GetOppoHis():
       global oppHisWinProb
       return oppHisWinProb











              
##              if ID in finishedIDs:
##                     pass
##              else:
##                     if action[i] == 'all_in':
##                            opponentInfoAll[ID]['all_in']+=1
##                            finishedIDs.append(ID)
##                            if opponentInfoAll[ID]['all_in']/float(num) <0.1:
##                                   a = 0.8
##                                   if opponentInfoAll[ID]['fold']/float(num) >0.7:
##                                          a=0.5
##                     elif action[i] == 'fold':
##                            opponentInfoAll[ID]['fold']+=1
##                            finishedIDs.append(ID)
##                     elif action[i] == 'raise':
##                            opponentInfoAll[ID]['raise']+=1
##                            if opponentInfoAll[ID]['raise']/float(num) <0.1:
##                                   a = 0.9
##                                   if opponentInfoAll[ID]['fold']/float(num) >0.7:
##                                          a=0.7
##
##       return a



