from copy import deepcopy
import heapq
from heapq import heappush
from heapq import heappop

totalblack=0
totalwhite=0

def input():
    with open("input.txt", 'r') as f1:
        lines = f1.readlines()
        player_type = int(lines[0])
        prevboard = [[int(x) for x in line.rstrip('\n')] for line in lines[1:6]]
        currboard = [[int(x) for x in line.rstrip('\n')] for line in lines[6:11]]

        return player_type, prevboard, currboard

# def input():
#   with open("input.txt",'r') as fl:
#     lines = fl.readlines()
#     player_type= int(lines[0])
#     prev_board=[]
#     curr_board=[]
    
#     for i in lines[1:6]:
#       l=i.rstrip("\n")
#       t=[]
#       for j in l:
#         t.append(int(j))
#       prev_board.append(t)
#     for i in lines[6:11]:
#       l=i.rstrip("\n")
#       t=[]
#       for j in l:
#         t.append(int(j))
#       curr_board.append(t)
#     # print(prev_board)
#     # print(curr_board)
#   return player_type,prev_board,curr_board

# # input()

def output(result):
    s = ""
    if result == "PASS":
        s = "PASS"
    else:
        s += str(result[0]) + ',' + str(result[1])

    with open("output.txt", 'w') as f1:
        f1.write(s)

# def output(result):
#   s=""
#   if result=="PASS":
#     s="PASS"
#   else:
#     s=str(result[0])+','+str(result[1])
#   # print(s)
#   with open("output.txt",'w') as fl:
#     fl.write(s)

def withinBoard(x, y):
    if x>=0 and x < 5 and y >= 0 and y < 5:
        return True
    else:
        return False

def compareBoard(board1,board2):
    for i in range(0,5):
        for j in range(0,5):
            if board1[i][j]!=board2[i][j]:
                return False
    return True

# p,pb,cb=input()
# print(compareBoard(pb,cb))

def addNeighbors(x,y):
    n = []
    d = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    for i in d:
        xi = x + i[0]
        yi = y + i[1]
        if withinBoard(xi, yi):
            n.append((xi, yi))
        # print(n)
    return n


def findNeighborAlly(x, y, board, player_type):
    n = addNeighbors(x, y)
    allies = []
    # print(n)
    for i in n:
        # print(i)
        if board[i[0]][i[1]] == player_type:
            allies.append(i)
    # print(allies)
    return allies

# p,pb,cb=input()
# addNeighbour(2,2)
# findNeighbourAlly(2,2,p,cb)

def allyPositionDFS(x, y, board, player_type):
    stack = [(x, y)]
    allies = []
    while stack:
        t = stack.pop()
        # print(t)
        allies.append(t)
        # print(allies)
        n = findNeighborAlly(t[0], t[1], board, player_type)
        for i in n:
            if i not in stack and i not in allies:
                # print(stack)
                stack.append(i)
                # print(stack)
    return allies

# p,pb,cb=input()
# allyPositionDFS(1,2,p,pb)

def findLibertyValue(x, y, board, player_type):
    allies = allyPositionDFS(x, y, board, player_type)
    for i in allies:
        n = addNeighbors(i[0], i[1])
        for j in n:
            if board[j[0]][j[1]] == 0:
                return True
    return False

def findDeadPieces(player_type, board):
    dead = []
    for i in range(0, 5):
        for j in range(0, 5):
            if board[i][j] == player_type:
                if not findLibertyValue(i, j, board, player_type):
                    dead.append((i, j))
                    # print(dead)
    return dead

def removeDeadPieces(died_pieces, board):
    for i in died_pieces:
        board[i[0]][i[1]] = 0
    # print(board)
    return board

def removeAllDeadPieces(player_type,board):
    dead=findDeadPieces(player_type,board)
    nextboard=removeDeadPieces(dead,board)
    return nextboard


def libertyPositions(x,y,board,player_type):
    l=set()
    allies = allyPositionDFS(x,y,board,player_type)
    for i in allies:
        n = addNeighbors(i[0], i[1])
        for j in n:
            if board[j[0]][j[1]] == 0:
                l=l|set([j])
                # print(l)
    return list(l)
#   l=[]
#   allies=allyPositionDFS(x,y,player_type,board)
#   for i in allies:
#     n=addNeighbour(i[0],i[1])
#     for j in n:
#       if board[j[0]][j[1]]==0:
#         l.append(tuple(j))
#       # print(l)
#   # print(list(l))
#   return l

# p,pb,cb=input()
# print(libertyPositions(1,2,p,pb))

def neighbourLibertyPositions(x,y,board,player_type):
    l = set()
    n = addNeighbors(x,y)
    for i in n:
        if board[i[0]][i[1]] == 0:
            l=l|set([i])
    #print(i,j)
    #print("lib",list(liberties))
    return list(l)

#   l=[]
#   n=addNeighbour(x,y)
#   # print(n)
#   for i in n:
#     # print(board[i[0]][i[1]])
#     if board[i[0]][i[1]]==0:
#       l.append(tuple(i))
#   # print(list(l))
#   return l

# p,pb,cb=input()
# print(neighbourLibertyPositions(1,2,pb))
    
def checkMove(x, y, board, player_type):
    nb = board
    nb[x][y] = player_type
    dp = findDeadPieces(3 - player_type, nb)
    if len(dp) == 0:
        return nb,len(dp),nb
    else:
        next_board = removeDeadPieces(dp, nb)
        return next_board,len(dp),nb

# b=board
# board[x][y]=player_type
# l=len(findDeadPieces(3-player_type,board))
# print(findDeadPieces(3-player_type,board))
# if l==0:
#   return board,l,board
# else:
#   print(removeDeadPieces(findDeadPieces(3-player_type,board),board))
#   return removeDeadPieces(findDeadPieces(3-player_type,board),board),l,board

# p,pb,cb=input()
# print(checkMove(1,1,1,pb))

def allValidMoves(player_type, previous_board, new_board):
    validmoves=set()
    # queue=[]
    for i in range(0, 5):
        for j in range(0, 5):
            if new_board[i][j]==player_type:    
                #print(i,j)
                libpos=libertyPositions(i,j,new_board,player_type)
                # print(libpos)
                if len(libpos)==1:
                    validmoves=validmoves|set(libpos)
                    # print(validmoves)
                    if i==0 or i==4 or j==0 or j==4:
                        neighbourpositions=neighbourLibertyPositions(libpos[0][0],libpos[0][1],new_board,player_type)
                        if neighbourpositions:
                            validmoves=validmoves|set(neighbourpositions)
                            # print(validmoves)
     
            elif new_board[i][j]==3-player_type:
                opponentlibpos=libertyPositions(i,j,new_board,3-player_type)
                validmoves=validmoves|set(opponentlibpos)
                # print(validmoves)
   
    finalmoves1 = []
    finalmoves2 = []
    v=list(validmoves)
    if len(v):
        for i in v:
            # print(i)
            duplicate = deepcopy(new_board)
            nxtb,died_pieces,b = checkMove(i[0],i[1], duplicate, player_type)
            if findLibertyValue(i[0], i[1], nxtb, player_type)and nxtb != previous_board and nxtb != new_board:
                finalmoves1.append((i[0], i[1],died_pieces))
                # heappush(queue,[i,-died_pieces])
                # print(finalmoves1)
        if len(finalmoves1)!= 0:
            return sorted(finalmoves1, key=lambda x: x[2],reverse=True)
            # return queue
        
    for i in range(0, 5):
        for j in range(0, 5):
            if  new_board[i][j] == 0:
                duplicate = deepcopy(new_board)
                nxtb,died_pieces,b = checkMove(i, j, duplicate, player_type)
                if findLibertyValue(i, j, nxtb, player_type) and nxtb != previous_board and nxtb != new_board:
                    finalmoves2.append((i, j,died_pieces))
                    # heappush(queue,[(i,j),-died_pieces])
                    # print(finalmoves2)
    return sorted(finalmoves2, key=lambda x: x[2],reverse=True)
    # return queue

def evalFunction(board, player_type,blackdead,whitedead):
    bcount = 0
    wcount = 2.5 #komi
    endangeredblack=0
    endangeredwhite=0
    for i in range(0, 5):
        for j in range(0, 5):
            if board[i][j] == 1:
                libpos=libertyPositions(i,j,board,1)
                if len(libpos)<=1:
                    endangeredblack+=1
                bcount += 1
            elif board[i][j] == 2:
                libpos=libertyPositions(i,j,board,2)
                if len(libpos)<=1:
                    endangeredwhite+=1
                wcount += 1
    # print(bcount)
    # print(wcount)
    # print(endangeredblack)
    # print(endangeredwhite)
    if player_type==1:
        eval_value = bcount-wcount+(endangeredwhite)-(endangeredblack)+(whitedead)-(blackdead)
        # eval_value = bcount-wcount+(endangeredwhite)-(endangeredblack)+(whitedead*10)-(blackdead*15)
        # eval_value = bcount-wcount+(endangeredwhite*2)-(endangeredblack*2)+(whitedead*10)-(blackdead*25)
    else:
        eval_value = wcount-bcount-(endangeredwhite)+(endangeredblack)+(blackdead)-(whitedead)
        # eval_value = wcount-bcount-(endangeredwhite)+(endangeredblack)+(blackdead*10)-(whitedead*15)
        # eval_value = wcount-bcount-(endangeredwhite*2)+(endangeredblack*2)+(blackdead*10)-(whitedead*25)
    return eval_value


def best_move(board,previous_board,player_type,depth):
    s, actions = maxMove(board,previous_board,player_type,depth, float("-inf"), float("inf"),board)
    #print(score,actions)
    if len(actions) > 0:
        return actions[0]  
    else:
        return "PASS"


def maxMove(board,previous_board,player_type,depth, alpha,beta,boardwithoutdead):
    global totalblack
    global totalwhite
    if player_type==2:
        deadwhite=len(findDeadPieces(player_type,boardwithoutdead))
        totalwhite=totalwhite+deadwhite
    if player_type==1:
        deadblack=len(findDeadPieces(player_type,boardwithoutdead))
        totalblack=totalblack+deadblack
    
    # print(totalblack)
    # print(totalwhite)

    if depth == 0:
        eval = evalFunction(board,player_type,totalblack,totalwhite)
        if player_type==1:
            totalblack=totalblack-len(findDeadPieces(1,boardwithoutdead))
        if player_type==2:
            totalwhite=totalwhite-len(findDeadPieces(2,boardwithoutdead))
        return eval,[]

    maxscore = float("-inf")
    maxactions = []
    validmoves = allValidMoves(player_type, previous_board, board)
    # print(validmoves)
    if len(validmoves)==25:
        return 200,[(2,2)]
    for i in validmoves:
        #print(i)
        duplicate = deepcopy(board)
        next_board,died_pieces,boardwithoutdead = checkMove(i[0], i[1], duplicate, player_type)
        score, actions = minMove(next_board,board,3-player_type,depth-1, alpha, beta,boardwithoutdead)
        
        if score > maxscore:
            maxscore = score
            maxactions = [i] + actions
            # print(maxactions)

        if maxscore > beta:
            # print(maxscore,maxactions)
            return maxscore, maxactions

        if maxscore > alpha:
            alpha = maxscore
            # print(alpha)

    return maxscore, maxactions    
    
def minMove(board,previous_board,player_type,depth, alpha, beta,boardwithoutdead):
    global totalblack
    global totalwhite
    if player_type==2:
        deadwhite=len(findDeadPieces(player_type,boardwithoutdead))
        totalwhite=totalwhite+deadwhite
    if player_type==1:
        deadblack=len(findDeadPieces(player_type,boardwithoutdead))
        totalblack=totalblack+deadblack
        
    # print(totalblack)
    # print(totalwhite)

    if depth == 0:
        eval = evalFunction(board,player_type,totalblack,totalwhite)
        if player_type==1:
            totalblack=totalblack-len(findDeadPieces(1,boardwithoutdead))
        if player_type==2:
            totalwhite=totalwhite-len(findDeadPieces(2,boardwithoutdead))
        return eval,[]

    minscore = float("inf")
    minactions = []
    validmoves = allValidMoves(player_type, previous_board, board)
    # print(validmoves)

    for i in validmoves:
        # print(i)
        duplicate = deepcopy(board)
        next_board,deadpieces,boardwithoutdead = checkMove(i[0], i[1], duplicate, player_type)
        score, actions = maxMove(next_board,board,3-player_type,depth-1, alpha, beta,boardwithoutdead)
        # print(score)
       
        if score < minscore:
            minscore = score
            minactions = [i] + actions
            # print(minactions)

        if minscore < alpha:
            # print(minscore,minactions)
            return minscore, minactions

        if minscore < beta:
            alpha = minscore
            # print(alpha)

    return minscore, minactions


def alphabeta(player_type, previous_board, new_board):  
    depth=4
    # if player_type==1:
    #     depth=4
    # if player_type==2:
    #     depth=6
    bestmove = best_move(new_board,previous_board,player_type,depth)
    #print(bestmove)
    output(bestmove)


p, pb, b = input()
alphabeta(p, pb, b)