# 오답: out of bound -> pos=(1,1)부터 시작하는 거 (0,0)으로 고침
class Santa:
    def __init__(self,n,r,c,state,score): # 오답: self 하는법
        self.n=n
        self.r=r
        self.c=c
        self.state=state # 0 is alive, 1 is faint, 2 is dead
        self.faintCnt=0
        self.score=score
    def printS(self): # 오답: self 빼먹음
        print(f'n={self.n},r={self.r},c={self.c},state={self.state},faintCnt={self.faintCnt},score={self.score}')

def dist(r1,c1,r2,c2):
    return (r1-r2)**2+(c1-c2)**2

# MODIFY: board, s.r, s.c
def santaCollision(board, s, d, N, posOrNeg):
    temp = board[s.r][s.c] # 방 빼
    board[s.r][s.c]=s # 입주
    nSr, nSc = s.r+d[0]*posOrNeg, s.c+d[1]*posOrNeg
    temp.r = nSr
    temp.c = nSc
    if not (0<=nSr<N and 0<=nSc<N): # 밀린 놈 죽음
        temp.state=2
    elif board[nSr][nSc]==0: # 밀린 자리 빔
        board[nSr][nSc]=temp
    else: # 밀린 자리 다른 놈 있음
        santaCollision(board,temp,d,N,posOrNeg) # recursion으로 반복!

    
# 1) 셋업
N,M,P,C,D = list(map(int,input().split()))
Rr, Rc = list(map(int,input().split()))
Rr, Rc = Rr-1, Rc-1
slist = []
# slist
for _ in range(1,P+1):
    i,r,c = tuple(map(int,input().split()))
    slist.append(Santa(i,r-1,c-1,0,0))
# board
board=[[0]*N for _ in range(N)]
for s in slist:
    board[s.r][s.c]=s # address of Santa object

# 2) 본게임
for _ in range(M):
# Rudolf Turn
    # closest santa
    s = None
    for nxt in slist:
        if nxt.state==2:
            continue
        if s==None:
            s=nxt
            continue
        if dist(s.r,s.c,Rr,Rc) > dist(nxt.r,nxt.c,Rr,Rc):
            s = nxt
        elif dist(s.r,s.c,Rr,Rc) == dist(nxt.r,nxt.c,Rr,Rc):
            if nxt.r>s.r or (nxt.r==s.r and nxt.c>s.c):
                s = nxt
    
    # nRr nRc
    dirsR = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(1,-1)] # row, col
    d_R=0
    minD = 10**10
    for i_dr,d in enumerate(dirsR):
        if 0<=Rr+d[0]<N and 0<=Rc+d[1]<N and dist(Rr+d[0],Rc+d[1],s.r,s.c)<minD:
            minD=dist(Rr+d[0],Rc+d[1],s.r,s.c)
            d_R=i_dr
    # Rudolf 이동
    Rr, Rc = Rr+dirsR[d_R][0], Rc+dirsR[d_R][1]

    # 충돌
    if Rr==s.r and Rc==s.c:
        s.state=1 # faint
        s.faintCnt=2
        s.score+=C
        s_org_r, s_org_c = s.r, s.c
        board[s_org_r][s_org_c]=0
        s.r+=dirsR[d_R][0]*C
        s.c+=dirsR[d_R][1]*C
        if not (0<=s.r<N and 0<=s.c<N): # out of board
            s.state=2 # dead
        elif board[s.r][s.c]!=0: # collide with other santa
            santaCollision(board,s,dirsR[d_R],N,1)
        else: # 다른 산타랑 충돌 안함: move to new spot
            board[s.r][s.c]=s
    # 충돌 안함
    if not (0<=Rr<N and 0<=Rc<N): # out of board
        print("Error: Rudolf moved out of board!")

# Santa Turn
    for s in slist:
        if s.state==1 or s.state==2:
            continue
        # nSr nSc
        dirsS = [(-1,0),(0,1),(1,0),(0,-1)] # row, col
        d_S=-1
        minD = dist(s.r,s.c,Rr,Rc) # 현재 거리
        for i_dr,d in enumerate(dirsS):
            if 0<=s.r+d[0]<N and 0<=s.c+d[1]<N and board[s.r+d[0]][s.c+d[1]]==0 and dist(s.r+d[0],s.c+d[1],Rr,Rc)<minD: # 산타 없고 현재 거리보다 짧을 시
                minD=dist(s.r+d[0],s.c+d[1],Rr,Rc)
                d_S=i_dr
        if d_S==-1: # 안 움직임
            continue
        s_org_r, s_org_c = s.r, s.c
        s.r, s.c = s.r+dirsS[d_S][0], s.c+dirsS[d_S][1]
        # s.printS()
        # 충돌
        if Rr==s.r and Rc==s.c:
            s.state=1 # faint
            s.faintCnt=2
            s.score+=D
            s.r-=dirsS[d_S][0]*D
            s.c-=dirsS[d_S][1]*D
            board[s_org_r][s_org_c]=0
            if not (0<=s.r<N and 0<=s.c<N): # out of board
                s.state=2 # dead
            elif board[s.r][s.c]!=0: # collide with other santa
                santaCollision(board,s,dirsS[d_S],N,-1)
            else: # 다른 산타랑 충돌 안함: move to new spot
                board[s.r][s.c]=s
        # 충돌 안함
        else:
            board[s_org_r][s_org_c]=0
            board[s.r][s.c]=s
# 턴 마무리
    n_dead = 0
    for s in slist:
        if s.state==2:
            n_dead+=1
            continue
        elif s.state==1:
            s.faintCnt-=1
            if s.faintCnt==0:
                s.state=0
        s.score+=1
    
    if n_dead==len(slist):
        break
    
    # print(f'Turn {_}')
    # print(board)
    # print(Rr,Rc)
    # for s in slist:
    #     s.printS()

# print score
scores = []
# print(Rr,Rc)
# print(board)
for s in slist:
    # s.printS()
    scores.append(s.score)
ans = ' '.join(map(str,scores))
print(ans)