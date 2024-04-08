# 오답1: checkWall()에서 return T/F를 반대로 함
from collections import deque

class Knight:
    def __init__(self,n,r,c,h,w,k):
        self.n=n
        self.r=r
        self.c=c
        self.h=h
        self.w=w
        self.k=k
        self.k_org=k
    def printk(self):
        print(f'n={self.n},r={self.r},c={self.c},k={self.k}')

def redraw(klist, kboard):
    # reset
    for r in range(len(kboard)):
        for c in range(len(kboard[r])):
            kboard[r][c]=0

    for k in klist:
        if k.k<=0: # if dead, dont draw
            continue
        for ir in range(k.h):
            for ic in range(k.w):
                kboard[k.r+ir][k.c+ic]=k.n

def checkWall(r,c,h,w,board): # return T if include wall
    for ir in range(h):
        for ic in range(w):
            if board[r+ir][c+ic]==2:
                return True
    return False

def nTraps(k,board): # return num of traps the knight is stepping on
    nsum=0
    for ir in range(k.h):
        for ic in range(k.w):
            if board[k.r+ir][k.c+ic]==1:
                nsum+=1
    return nsum

def move(i,d,dirs,klist,board,kboard,vis,q):
    # print(i)
    now = klist[i] # A
    nR, nC = now.r+dirs[d][0],now.c+dirs[d][1]
    vis.append(i)
    if checkWall(nR,nC,now.h,now.w,board)==True:
        # print('wall!')
        # print(f'nR={nR},nC={nC}')
        return False
    else:
        # find other knights that were hit -> add to Queue
        for ir in range(now.h):
            for ic in range(now.w):
                n = kboard[nR+ir][nC+ic]
                if n!=0 and (n not in vis): # hit other knight!
                    vis.append(n)
                    q.append(n)
        # recursion
        if q:
            i_nxt = q.popleft()
            nxt = klist[i_nxt]
            result = move(i_nxt,d,dirs,klist,board,kboard,vis,q)
            if result==False:
                return False
            else:
                now.r,now.c=nR,nC
                now.k-=nTraps(now,board)
                return True
        else: # end case
            now.r,now.c=nR,nC
            now.k-=nTraps(now,board)
            return True

# input & setup
L,N,Q = list(map(int,input().split()))
board = [[0]*(L+2) for _ in range(L)]
board = [[2]*(L+2),*board,[2]*(L+2)]
for r in range(1,L+1):
    ln = list(map(int,input().split())) # 0 0 1 0
    ln = [2,*ln,2]
    board[r] = ln

klist = [Knight(0,0,0,0,0,0)]
for i in range(N):
    r,c,h,w,k = list(map(int,input().split()))
    klist.append(Knight(i+1,r,c,h,w,k))
qlist = []
for q in range(Q):
    ln = list(map(int,input().split()))
    qlist.append(ln) # i=1, d=2
# # print knights
# for k in klist:
#     k.printk()

kboard = [[0]*(L+2) for _ in range(L+2)]
redraw(klist,kboard)
# print('board:')
# print(board)
# print('kboard:')
# print(kboard)

# 명령 수행
dirs=[(-1,0),(0,1),(1,0),(0,-1)] # (r,c), 위 오른 아래 왼
for i,d in qlist:
    if klist[i].k<=0:
        continue
    now=klist[i]
    q=deque()
    vis=[]
    result=move(i,d,dirs,klist,board,kboard,vis,q) # main algorithm
    if result==False:
        continue
    else:
        now.k+=nTraps(now,board) # 현재 knight 체력은 원상복귀
        redraw(klist,kboard)

ans=0
for k in klist:
    if k.k<=0:
        continue
    ans+=k.k_org-k.k
print(ans)