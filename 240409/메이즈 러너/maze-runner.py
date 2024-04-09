# 16m (/1hr)
class Player:
    def __init__(self,r,c):
        self.r=r
        self.c=c
        self.escape=False
        self.d=0 
    def printp(self):
        print(f'r={self.r},c={self.c},esc={self.escape},d={self.d}')

def dist(r1,c1,r2,c2):
    return math.abs(r1-c1)2+math.abs(r2-c2)


# setup
N,M,K = list(map(int,input().split()))
board=[]
for _ in range(N):
    ln=list(map(int,input().split()))
    board.append(ln)
plist=[]
for _ in range(M):
    r,c=list(map(int,input().split()))
    plist.append(Player(r-1,c-1))
e=list(map(int,input().split()))

# 1) player move
for p in plist:
    if p.escape:
        continue
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    minD=dist(p.r,p.c,e[0],e[1])
    for dr,dc in dirs:
        nR,nC = p.r+dr,p.c+dc