import json, os, sys, urllib.request, urllib.error

# --- constants ---------------------------------------------------------------
OFF = '#'
V = {'p':100,'n':320,'b':330,'r':500,'q':900,'k':0}
AL = 'abcdefghijklmn'
VM = [-50,-40,-30,-20,-10,-5,0,5,10,15,20,25,30,50]
PN='ggggggggnnnnnnnniikmmkiihhillihhgggkkggghfeggefhhiiddiihgggggggg'
NN='abccccbabdggggdbcgijjigcchjkkjhccgjkkjgcchijjihcbdghhgdbabccccba'
BN='deeeeeedeggggggeeghiihgeehhiihheegiiiigeeiiiiiieehgggghedeeeeeed'
RN='gggggggghiiiiiihfggggggffggggggffggggggffggggggffggggggfggghhggg'
QN='deeffeedeggggggeeghhhhgefghhhhgfgghhhhgfehhhhhgeeghggggedeeffeed'
KN='cbbaabbccbbaabbccbbaabbccbbaabbcdccbbccdeddddddekkggggkkkmiggimk'
PST={'P':[VM[AL.find(c)]for c in PN],'N':[VM[AL.find(c)]for c in NN],
     'B':[VM[AL.find(c)]for c in BN],'R':[VM[AL.find(c)]for c in RN],
     'Q':[VM[AL.find(c)]for c in QN],'K':[VM[AL.find(c)]for c in KN]}
KNIGHT=(8,12,19,21,-8,-12,-19,-21); BISHOP=(9,11,-9,-11)
ROOK=(1,10,-1,-10); QUEEN=(1,10,-1,-10,9,11,-9,-11)
KING=(1,10,-1,-10,9,11,-9,-11)
MATE=30000
TT={}; NODES=0; CAP=40000
B=None; T=1; R='KQkq'; E=-1

# --- board -------------------------------------------------------------------
def F(s):
    global B,T,R,E
    p=s.split(); B=[OFF]*120; r=1
    for rank in p[0].split('/'):
        c=1
        for ch in rank:
            if ch.isdigit():
                for _ in range(int(ch)): B[r*10+c]='.'; c+=1
            else: B[r*10+c]=ch; c+=1
        r+=1
    T=1 if p[1]=='w' else 0
    R=p[2] if len(p)>2 else 'KQkq'
    E=-1
    if len(p)>3 and p[3]!='-':
        E=(9-int(p[3][1]))*10+ord(p[3][0])-96

def g_castle(side, ms):
    R0=R
    if side:
        if 'K' in R0 and B[88]=='R' and B[86]==B[87]=='.': ms.append((85,87,''))
        if 'Q' in R0 and B[81]=='R' and B[82]==B[83]==B[84]=='.': ms.append((85,83,''))
    else:
        if 'k' in R0 and B[18]=='r' and B[16]==B[17]=='.': ms.append((15,17,''))
        if 'q' in R0 and B[11]=='r' and B[12]==B[13]==B[14]=='.': ms.append((15,13,''))

def G(side):
    ms=[]; fw=-10 if side else 10
    for s in range(11,89):
        pc=B[s]
        if pc==OFF or pc=='.': continue
        if pc.isupper()!=side: continue
        L=pc.lower(); f=s%10; r0=s//10
        if L=='p':
            pr=(r0==1) if side else (r0==8)
            j=s+fw
            if B[j]=='.':
                if pr:
                    for pz in 'qrbn': ms.append((s,j,pz))
                else:
                    ms.append((s,j,''))
                    if ((r0==7) if side else (r0==2)) and B[j+fw]=='.':
                        ms.append((s,j+fw,''))
            for df in (-1,1):
                if not 1<=f+df<=8: continue
                j=s+fw+df
                if B[j]!=OFF and B[j]!='.' and B[j].isupper()!=side:
                    if pr:
                        for pz in 'qrbn': ms.append((s,j,pz))
                    else: ms.append((s,j,''))
                elif j==E and B[j]=='.': ms.append((s,j,''))
        elif L=='n':
            for off in KNIGHT:
                j=s+off
                if B[j]!=OFF and (B[j]=='.' or B[j].isupper()!=side):
                    ms.append((s,j,''))
        elif L=='k':
            for off in KING:
                j=s+off
                if B[j]!=OFF and (B[j]=='.' or B[j].isupper()!=side):
                    ms.append((s,j,''))
            g_castle(side,ms)
        else:
            dirs = BISHOP if L=='b' else ROOK if L=='r' else QUEEN
            for off in dirs:
                j=s+off
                while B[j]=='.':
                    ms.append((s,j,'')); j+=off
                if B[j]!=OFF and B[j].isupper()!=side: ms.append((s,j,''))
    return ms

def M(m):
    global B,T,R,E
    f,t,p=m; c=B[f]; w=B[t]; fw=-10 if T else 10
    snap=(list(B),R,E)
    B[f]='.'
    if c.lower()=='p' and t==E and t%10!=f%10 and w=='.':
        B[t+fw]='.'
    B[t]=(p.upper() if T else p) if p else c
    if c.lower()=='k' and abs(t-f)==2:
        if t>f: B[f+1]='.'; B[t-1]='R' if T else 'r'
        else: B[f-1]='.'; B[t+1]='R' if T else 'r'
        R=R.replace('K','').replace('Q','') if T else R.replace('k','').replace('q','')
    elif c.lower()=='r':
        if T and f==88: R=R.replace('K','')
        elif T and f==81: R=R.replace('Q','')
        elif not T and f==18: R=R.replace('k','')
        elif not T and f==11: R=R.replace('q','')
    if w.lower()=='r':
        if (not T) and w=='R':
            if t==88: R=R.replace('K','')
            elif t==81: R=R.replace('Q','')
        if T and w=='r':
            if t==18: R=R.replace('k','')
            elif t==11: R=R.replace('q','')
    E=(f+t)//2 if c.lower()=='p' and abs(f-t)==20 else -1
    T=not T
    return snap

def U(snap):
    global B,R,E,T
    B,R,E=snap; T=not T

def uci(m):
    f,t,p=m
    return chr(97+(f%10-1))+str(9-f//10)+chr(97+(t%10-1))+str(9-t//10)+(p or '')

# --- search / eval -----------------------------------------------------------
def e():
    sc=0
    for s in range(11,89):
        c=B[s]
        if c==OFF or c=='.': continue
        f=s%10-1; r=s//10-1
        if c.isupper(): sc+=V[c.lower()]+PST[c][r*8+f]
        else: sc-=V[c]+PST[c.upper()][(r*8+f)^56]
    return sc if T else -sc

def q(a,b):
    global NODES
    NODES+=1
    x=e()
    if x>=b: return b
    if x>a: a=x
    for m in G(T):
        f,t,p=m
        if p or B[t]!='.' or (B[f].lower()=='p' and t==E and t%10!=f%10):
            if B[t].lower()=='k': return MATE
            snap=M(m); s=-q(-b,-a); U(snap)
            if s>=b: return b
            if s>a: a=s
    return a

def mvk(m):
    f,t,p=m
    vic=V[B[t].lower()] if B[t]!='.' else 0
    if p: vic=max(vic,V[p])
    if B[t].lower()=='k': vic=99000
    return -(vic*16 - V[B[f].lower()])

def A(d,a,b,ply):
    global NODES
    NODES+=1
    key=(tuple(B),T,d,a,b)
    z=TT.get(key)
    if z is not None: return z
    ms=G(T)
    if not ms:
        v=-MATE+ply; TT[key]=v; return v
    if d==0:
        v=q(a,b); TT[key]=v; return v
    best=-MATE-1
    ms.sort(key=mvk)
    for m in ms:
        f,t,p=m
        if B[t].lower()=='k': s=MATE-ply
        else:
            snap=M(m); s=-A(d-1,-b,-a,ply+1); U(snap)
        if s>best: best=s
        if s>a: a=s
        if a>=b: break
    TT[key]=best
    return best

def pick(legal=None):
    global TT,NODES
    ms=G(T)
    if not ms: return None
    if legal is not None:
        ls=set(legal); fl=[m for m in ms if uci(m) in ls]
        if fl: ms=fl
    for m in ms:
        if B[m[1]].lower()=='k': return m
    best=ms[0]; bestsc=None; d=1; NODES=0
    while True:
        if len(TT)>200000: TT={}
        over=False
        for m in ms:
            f,t,p=m
            if B[t].lower()=='k': return m
            NODES+=1
            snap=M(m); s=-A(d-1,-MATE,MATE,1); U(snap)
            if bestsc is None or s>bestsc: bestsc=s; best=m
            if NODES>CAP: over=True; break
        if over: break
        d+=1
    return best

# --- environment loop --------------------------------------------------------
if __name__=='__main__':
    ENV=os.environ.get('MAKEFUN_ENV_URL')
    if not ENV: sys.exit('MAKEFUN_ENV_URL is not set')
    def post(path,body):
        req=urllib.request.Request(ENV+path, data=json.dumps(body).encode(),
                                   headers={'content-type':'application/json'})
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    while True:
        g=post('/game',{})
        if g['status']=='done': break
        while g['status']=='your_move':
            F(g['fen'])
            mv=pick(legal=g.get('legal_moves'))
            if mv is None:
                try: post('/resign',{'game':g['game']})
                except Exception: pass
                g=post('/game',{})
                break
            try:
                g=post('/move',{'game':g['game'],'move':uci(mv)})
            except urllib.error.HTTPError as e:
                if e.code==400:
                    g=post('/game',{})
                    continue
                raise
        if g['status'] not in ('your_move','done'):
            print('game %s: %s by %s'%(g.get('game'),g.get('outcome'),g.get('reason')),file=sys.stderr)
    print('done: %s won, %s drawn, %s lost'%(g.get('wins'),g.get('draws'),g.get('losses')),file=sys.stderr)
