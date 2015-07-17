#!/usr/bin/python
from Evaluate import *
from firstRound_new import *
from ActionDecision_top_win_crush_done import *
from Study_win import *
ROUND = 0
ROUNDTMP = 0
RESACT = ''
GAME = 0 #game number
GAMEB = 0 #temp game number
HOLD = []
FLOP = []
TURN = []
RIVER = []
OnlineNumA = 8 #the num of players online surviver
OnlineNumB = 8 #not fold
OnlineNumBTMP = 8
PROB = 0 #probability
MYJETTON = 0
MYMONEY = 0
MYBET = 0
CARDNUM = 0
hasNOTIFY = False
hasSHOWDOWN = False
TMPMSG = ''
smallBlind = 0
initialJetton = 0
initialMoney = 0 
MoneyJettonSB = 1
isBlind = 3
       
def getseatinfo(seatinfo):
    myjetton = seatinfo.split()[-2]
    mymoney = seatinfo.split()[-1]
    return [int(myjetton), int(mymoney)]

def getplayerid(seatinfo):
    seat = seatinfo.split(' \n')
    infolen = len(seat)-1
    ids = []
    for i in range(infolen):
        ids.append(seat[i].split()[-3])
    return ids
        
def getholdinfo(holdinfo):
    card1_color = holdinfo[0].split()[0]
    card1_point = holdinfo[0].split()[1]
    card2_color = holdinfo[1].split()[0]
    card2_point = holdinfo[1].split()[1]
    return [[card1_color, card2_color], [card1_point, card2_point]]

def getflopinfo(flopinfo):
    fcard1_color = flopinfo[0].split()[0]
    fcard1_point = flopinfo[0].split()[1]
    fcard2_color = flopinfo[1].split()[0]
    fcard2_point = flopinfo[1].split()[1]
    fcard3_color = flopinfo[2].split()[0]
    fcard3_point = flopinfo[2].split()[1]
    return [[fcard1_color, fcard2_color, fcard3_color], [fcard1_point, fcard2_point, fcard3_point]]

def getturninfo(turninfo):
    tcard_color = turninfo[0].split()[0]
    tcard_point = turninfo[0].split()[1]
    return [[tcard_color], [tcard_point]]

def getriverinfo(riverinfo):
    rcard_color = riverinfo[0].split()[0]
    rcard_point = riverinfo[0].split()[1]
    return [[rcard_color], [rcard_point]]

def getinquireinfo(inquireinfo):
    totalpot = int(inquireinfo[-2].split()[2])
    infolen = len(inquireinfo)-2
    jetton = []
    money = []
    bet = []
    for i in range(infolen):
        jetton.append(int(inquireinfo[i].split()[1]))
        money.append(int(inquireinfo[i].split()[2]))
        bet.append(int(inquireinfo[i].split()[3]))
    return [jetton, money, bet, totalpot]

def getnotifyinfo(notifyinfo):
    totalpot = int(notifyinfo[-2].split()[2])
    infolen = len(notifyinfo)-2
    jetton = []
    bet = []
    for i in range(infolen):
        jetton.append(int(notifyinfo[i].split()[1]))
        bet.append(int(notifyinfo[i].split()[3]))
    return [jetton, bet, totalpot]

def getopponentinfo(inquireinfo):
    global OnlineNumA
    action = []
    ids = []
    infolen = len(inquireinfo)-2
    if infolen == OnlineNumA:
        infolen -= 1
    for i in range(infolen):
        action.append(inquireinfo[i].split()[4])
        ids.append(inquireinfo[i].split()[0])
    return [ids,action]

def getshowdowninfo(showdowninfo):
    pubcol = []
    pubpot = []
    commoninfo = showdowninfo.split('common/ \n')[1].split('/common \n')[0].split(' \n')
    commonlen = len(commoninfo)-1
    for i in range(commonlen):
        pubcol.append(commoninfo[i].split()[0])
        pubpot.append(commoninfo[i].split()[1])
    playerid = []
    playercol = []
    playerpot = []
    playerdowninfo = showdowninfo.split('/common \n')[1].split(' \n')
    playerlen = len(playerdowninfo)-1
    for i in range(playerlen):
        playerid.append(playerdowninfo[i].split()[1])
        playercol.append([playerdowninfo[i].split()[2], playerdowninfo[i].split()[4]])
        playerpot.append([playerdowninfo[i].split()[3], playerdowninfo[i].split()[5]])
    return [playerid,playercol,playerpot,pubcol,pubpot]
            
def server_msg(msg, sock, playerid):
    global RESACT
    global HOLD
    global FLOP
    global TURN
    global RIVER
    global GAME
    global GAMEB
    global OnlineNumA
    global OnlineNumB
    global OnlineNumBTMP
    global PROB
    global ROUND
    global ROUNDTMP
    global MYJETTON
    global MYMONEY
    global MYBET
    global CARDNUM
    global hasNOTIFY
    global hasSHOWDOWN
    global TMPMSG
    global smallBlind
    global initialJetton
    global initialMoney
    global MoneyJettonSB
    global isBlind

    import random
    import traceback
    #import time

    #f.write(msg+'\n\n')
    #t1=time.time()
    while len(msg) != 0:
        try:
            if 'seat/' == msg[0:5]:#when arranging seat
                if -1 == msg.find('/seat \n'):
                    TMPMSG = msg
                    return True
                else:
                    seatinfo = msg.split('seat/ \n')[1].split('/seat \n')[0]
                    #myseatinfo = seatinfo.split(playerid+' ')[1].split(' \n')[0]
                    #[MYJETTON, MYMONEY] = getseatinfo(myseatinfo)
                    OnlineNumA = len(seatinfo.split(' \n'))-1
                    OnlineNumBTMP = OnlineNumA
                    seatID = getplayerid(seatinfo)
                    myindex = seatID.index(playerid)
                    if myindex == 1:
                        isBlind = 1
                    elif myindex == 2:
                        isBlind = 2
                    else:
                        isBlind = 3
                    myseatinfo = seatinfo.split(' \n')[myindex]
                    [MYJETTON, MYMONEY] = getseatinfo(myseatinfo)
                    buttonID = seatID[0]
                    seatID.remove(playerid)
                    GAME += 1
                    if GAME == 1:
                        initialMoney = MYMONEY + MYJETTON
                        initialJetton = MYJETTON
                        opponentInfoInitial(seatID)
                    opponentInfoUpdataRepair(buttonID)
                    msg = msg[msg.find('/seat \n')+7:]
                    continue
               
            if 'blind/' == msg[0:6]:
                if -1 == msg.find('/blind \n'):
                    TMPMSG = msg
                    return True
                else:
                    blindinfo = msg.split('blind/ \n')[1].split('/blind \n')[0]
                    smallBlind = int(blindinfo.split(' \n')[0].split()[1])
                    if -1 != blindinfo.find(playerid+':'):
                        MYBET = int(blindinfo.split(playerid+': ')[1].split(' \n')[0])
                        MYJETTON -= MYBET
                    else:
                        MYBET = 0  
                    if GAME == 1:
                        if float(initialMoney)/initialJetton == 2 and float(initialJetton)/smallBlind == 100:
                            MoneyJettonSB = 1
                        elif float(initialMoney)/initialJetton == 2 and float(initialJetton)/smallBlind > 100:
                            MoneyJettonSB = 2
                        elif float(initialMoney)/initialJetton < 2 and float(initialJetton)/smallBlind == 100:
                            MoneyJettonSB = 3
                        else:
                            MoneyJettonSB = 1
                    if MoneyJettonSB == 2:
                        fixSB(initialJetton/100)
                    else:
                        fixSB(smallBlind)
                    msg = msg[msg.find('/blind \n')+8:]
                    continue      

        ############################
            if 'hold/' == msg[0:5]:
                if -1 == msg.find('/hold \n'):
                    TMPMSG = msg
                    return True
                else:
                    holdinfo = msg.split('hold/ \n')[1].split('/hold \n')[0].split(' \n')
                    HOLD = getholdinfo(holdinfo)
                    ROUND = 1
                    ROUNDTMP = 1
                    CARDNUM = 2
                    msg = msg[msg.find('/hold \n')+7:]
                    continue 
                    
            

            if 'flop/' == msg[0:5]:
                if -1 == msg.find('/flop \n'):
                    TMPMSG = msg
                    return True
                else:
                    if RESACT == 'all_in' or RESACT == 'hold':
                        pass
                    else:
                        flopinfo = msg.split('flop/ \n')[1].split('/flop \n')[0].split(' \n')
                        FLOP = getflopinfo(flopinfo)
                    ROUND = 2
                    CARDNUM = 5
                    msg = msg[msg.find('/flop \n')+7:]
                    continue     

                
            
            if 'turn/' == msg[0:5]:
                if -1 == msg.find('/turn \n'):
                    TMPMSG = msg
                    return True
                else:
                    if RESACT == 'all_in' or RESACT == 'hold':
                        pass
                    else:
                        turninfo = msg.split('turn/ \n')[1].split('/turn \n')[0].split(' \n')
                        TURN = getturninfo(turninfo)
                    ROUND = 3
                    CARDNUM = 6
                    msg = msg[msg.find('/turn \n')+7:]
                    continue
                        

            if 'river/' == msg[0:6]:
                if -1 == msg.find('/river \n'):
                    TMPMSG = msg
                    return True
                else:
                    if RESACT == 'all_in' or RESACT == 'hold':
                        pass
                    else:
                        riverinfo = msg.split('river/ \n')[1].split('/river \n')[0].split(' \n')
                        RIVER = getriverinfo(riverinfo)
                    ROUND = 4
                    CARDNUM = 7
                    msg = msg[msg.find('/river \n')+8:]
                    continue    

                
        #############################################
            if 'inquire/' == msg[0:8]:
                if -1 == msg.find('/inquire \n'):
                    TMPMSG = msg
                    return True
                else:
                    if GAMEB != GAME:
                        inquireinfo = msg.split('inquire/ \n')[1].split('/inquire \n')[0].split(' \n')
                        inqinfo = msg.split('inquire/ \n')[1].split('/inquire \n')[0]
                        OnlineNumB = OnlineNumA - inqinfo.count('fold')
                        #PROB = EvaluateMyCard(HOLD[0], HOLD[1], OnlineNumB)
                        PROB = GetAction(HOLD[1],HOLD[0])
                        [sendjetton, sendmoney, sendbet, totalpot] = getinquireinfo(inquireinfo)
                        if len(sendjetton)<OnlineNumA:
                            sendjetton.append(MYJETTON)
                            sendmoney.append(MYMONEY)
                            sendbet.append(MYBET)
                        [ID , playeraction] = getopponentinfo(inquireinfo)
                        ID.append(playerid)
                        fix,allcheck,opphisallin,opphisraise,isButton,jettonwf,betwf,ACIB,checkenable = opponentInfoUpdata(ID, playeraction,sendjetton,sendbet, GAME, CARDNUM, OnlineNumB,OnlineNumA,PROB)
                        #f.write(' fix='+str(fix)+' prob='+str(PROB)+'\n money='+str(sendmoney)+'\n jetton='+str(sendjetton)+'\n jettonwf='+str(jettonwf)+'\n bet='+str(betwf)+'\n totalpot='+str(totalpot)+'\n stage='+str(ROUND)+'\n validplayer='+str(OnlineNumB)+'\n totalplayer='+str(OnlineNumA)+'\n GAME='+str(GAME)+'\n isButton='+str(isButton)+'\n ACIB='+str(ACIB)+'\n raiseinfo='+str(allcheck)+'\n checkenable='+str(checkenable)+'\n')
                        #f.write('-------------------------------------------\n')
                        RESACT = ActionDecision(PROB, sendmoney, sendjetton, betwf, totalpot, ROUND, OnlineNumB, GAME,opphisallin,opphisraise,isButton,allcheck,OnlineNumA,ACIB,smallBlind,initialJetton,initialMoney,MoneyJettonSB,isBlind,checkenable,jettonwf)
                        try:
                            sock.send(RESACT)
                            #f.write(RESACT+str(GAME)+str(GAMEB)+'\n\n')
                        except socket.error, e:
                            pass
                        if GAME!=1 and hasNOTIFY==True:
                            opponentInfoUpdataFormer()
                            if hasSHOWDOWN == True:
                                oppoAnalyzeThread()
                                hasSHOWDOWN = False
                            else:
                                pass
                            endRec() 
                        if hasNOTIFY == False and hasSHOWDOWN == True:
                            oppoAnalyzeThread()
                            hasSHOWDOWN = False                         
                        if (RESACT == 'fold' or RESACT == 'all_in') and OnlineNumB != 2:
                            hasNOTIFY = True
                        else:
                            hasNOTIFY = False
                        if hasNOTIFY == True:
                            startRec()
                        OnlineNumBTMP = OnlineNumB
                        GAMEB = GAME
                    else:
                        inquireinfo = msg.split('inquire/ \n')[1].split('/inquire \n')[0].split(' \n')
                        inqinfo = msg.split('inquire/ \n')[1].split('/inquire \n')[0]
                        OnlineNumB = OnlineNumA - inqinfo.count('fold')
                        if OnlineNumB == OnlineNumBTMP and ROUND == ROUNDTMP:
                            pass
                        else:
                            if ROUND == 1:
                                PROB = GetAction(HOLD[1], HOLD[0])
                            elif ROUND == 2:
                                PROB = EvaluateMyCard(HOLD[0]+FLOP[0],HOLD[1]+FLOP[1],OnlineNumB)
                            elif ROUND == 3:
                                PROB = EvaluateMyCard(HOLD[0]+FLOP[0]+TURN[0],HOLD[1]+FLOP[1]+TURN[1],OnlineNumB)
                            else:
                                PROB = EvaluateMyCard(HOLD[0]+FLOP[0]+TURN[0]+RIVER[0],HOLD[1]+FLOP[1]+TURN[1]+RIVER[1],OnlineNumB)
                        [sendjetton, sendmoney, sendbet, totalpot] = getinquireinfo(inquireinfo)
                        [ID , playeraction] = getopponentinfo(inquireinfo)
                        ID.append(playerid)
                        fix,allcheck,opphisallin,opphisraise,isButton,jettonwf,betwf,ACIB,checkenable = opponentInfoUpdata(ID, playeraction,sendjetton,sendbet, GAME, CARDNUM, OnlineNumB,OnlineNumA,PROB)
                        #f.write(str(fix)+' '+str(PROB)+' '+str(sendmoney)+str(sendjetton)+str(betwf)+str(totalpot)+' '+str(ROUND)+' '+str(OnlineNumB)+' '+str(GAME)+str(isButton)+'\n')
                        #f.write(' fix='+str(fix)+' prob='+str(PROB)+'\n money='+str(sendmoney)+'\n jetton='+str(sendjetton)+'\n jettonwf='+str(jettonwf)+'\n bet='+str(betwf)+'\n totalpot='+str(totalpot)+'\n stage='+str(ROUND)+'\n validplayer='+str(OnlineNumB)+'\n totalplayer='+str(OnlineNumA)+'\n GAME='+str(GAME)+'\n isButton='+str(isButton)+'\n ACIB='+str(ACIB)+'\n raiseinfo='+str(allcheck)+'\n checkenable='+str(checkenable)+'\n')
                        #f.write('=======================================\n')
                        if ROUND == 1:	    
                            RESACT = ActionDecision(PROB, sendmoney, sendjetton, betwf, totalpot, ROUND, OnlineNumB, GAME,opphisallin,opphisraise,isButton,allcheck,OnlineNumA,ACIB,smallBlind,initialJetton,initialMoney,MoneyJettonSB,isBlind,checkenable,jettonwf)
                        else:
                            RESACT = ActionDecision(fix*PROB, sendmoney, sendjetton, betwf, totalpot, ROUND, OnlineNumB, GAME,opphisallin,opphisraise,isButton,allcheck,OnlineNumA,ACIB,smallBlind,initialJetton,initialMoney,MoneyJettonSB,isBlind,checkenable,jettonwf)
                        try:
                            sock.send(RESACT)
                            #f.write(RESACT+str(GAME)+str(GAMEB)+'\n\n')
                        except socket.error, e:
                            pass
                        if (RESACT == 'fold' or RESACT == 'all_in') and OnlineNumB != 2:
                            hasNOTIFY = True
                        else:
                            hasNOTIFY = False
                        if hasNOTIFY == True:
                            startRec()
                        OnlineNumBTMP = OnlineNumB
                        ROUNDTMP = ROUND
                    msg = msg[msg.find('/inquire \n')+10:]
                    continue        

            if 'notify/' == msg[0:7]:
                if -1 == msg.find('/notify \n'):
                    TMPMSG = msg
                    return True
                else:
                    if hasNOTIFY == False:
                        msg = msg[msg.find('/notify \n')+9:]
                        continue
                    else:
                        notifyinfo = msg.split('notify/ \n')[1].split('/notify \n')[0].split(' \n')
                        [notifyjetton, notifybet, notifytotalpot] = getnotifyinfo(notifyinfo)
                        notinfo = msg.split('notify/ \n')[1].split('/notify \n')[0]
                        OnlineNumB = OnlineNumA - notinfo.count('fold')
                        [notifyID , notifyplayeraction] = getopponentinfo(notifyinfo)
                        notifyID.append(playerid)
                        opponentInfoUpdataRec(notifyID, notifyplayeraction,notifybet, CARDNUM, OnlineNumB, GAME)
                        msg = msg[msg.find('/notify \n')+9:]
                        continue      

            if 'showdown/' == msg[0:9]:
                if -1 == msg.find('/showdown \n'):
                    TMPMSG = msg
                    return True
                else:
                    showdowninfo = msg.split('showdown/ \n')[1].split('/showdown \n')[0]
                    [playersid,playercol,playerpot,pubcol,pubpot]=getshowdowninfo(showdowninfo)          
                    if hasNOTIFY == False:
                        startRecNoNotify()
                    hasSHOWDOWN = True
                    oppoAnalyzeRec(playersid,playercol,playerpot,pubcol,pubpot)
                    msg = msg[msg.find('/showdown \n')+11:]
                    continue    

            if 'pot-win/' == msg[0:8]:
                if -1 == msg.find('/pot-win \n'):
                    TMPMSG = msg
                    return True
                else:
                    if hasNOTIFY == False and hasSHOWDOWN == False:
                        startRecNoNotify()
                    if hasNOTIFY == False:
                        endRecNoNotify()
                    #f.write('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
                    #zhstest(f,GAME)
                   # f.write('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n')
                    msg = msg[msg.find('/pot-win \n')+10:]
                    continue    
    

            if 'game-over' == msg[0:9]:
                return False
            else:
                if TMPMSG == '':
                    TMPMSG = msg
                    return True
                else:
                    msg = TMPMSG + msg
                    TMPMSG = ''
                    continue
        except:
            print 'has wrong'
            info = sys.exc_info()
            print info[0],":",info[1]
            traceback.print_exc(file=sys.stdout)
            if 0 != msg.count('inquire/'):
                for i in range(msg.count('inquire/')):
                    RESACT = 'fold'
                    try:
                        sock.send(RESACT)
                    except socket.error, e:
                        pass
                return True
            else:
                return True    
    #t2=time.time()         
    #m.write(str(t2-t1)+'\n')
    return True

if __name__=='__main__':
    import socket, sys
    import time
    # if len(sys.argv) != 6
    #    sys.exit(1)
    
    serverhost = sys.argv[1]
    serverport = int(sys.argv[2])

    playerhost = sys.argv[3]
    playerport = int(sys.argv[4])

    playerid = sys.argv[5]

    playername = 'lovelylaoban'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    s.bind((playerhost,playerport))

    #m = open(playerid+'.txt','a')
    #f = open('recv'+playerid+'.txt','a')

    while True:
        try:
            s.connect((serverhost, serverport))
        except:
            time.sleep(0.1)
            continue
        break

    s.send('reg: %s %s need_notify \n' %(playerid, playername))
    
    while 1:
        try:
            buf = s.recv(4096)
        except socket.error, e:
            pass
        if len(buf)>0:
            if server_msg(buf,s,playerid)==False:
                break

    #m.close()
    #f.close()
    s.close()
