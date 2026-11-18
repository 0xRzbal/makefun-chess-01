import json,os,sys,time,urllib.request
C='abcdefghijklmn';Q=[0,5,10,15,20,25,30,50,-5,-10,-20,-30,-40,-50]
S=('aaaaaaaahhhhhhhhcceggeccbbcffcbbaaaeeaaabijaajibbcckkccbaaaaaaaa','nmllllmnmkaaaakmlacddcallbdeedblladeedallbcddcblmkabbakmnmllllmn','kjjjjjjkjaaaaaajjabccbajjbbccbbjjaccccajjccccccjjbaaaabjkjjjjjjk','aaaaaaaabccccccbiaaaaaaiiaaaaaaiiaaaaaaiiaaaaaaiiaaaaaaiaaabbaaa','kjjiijjkjaaaaaajjabbbbajiabbbbaiaabbbbaijbbbbbajjabaaaajkjjiijjk','lmmnnmmllmmnnmmllmmnnmmllmmnnmmlkllmmllkjkkkkkkjeeaaaaeeegcaacge')
P={k:[Q[C.find(x)]for x in s]for k,s in zip('PNBRQK',S)}
V={'p':100,'n':320,'b':330,'r':500,'q':900,'k':0}
D={'n':((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)),'k':((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)),'b':((-1,-1),(-1,1),(1,-1),(1,1)),'r':((-1,0),(1,0),(0,-1),(0,1)),'q':((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))}
RM={63:'K',56:'Q',7:'k',0:'q'};CA={62:(63,61),58:(56,59),6:(7,5),2:(0,3)}
B=None;T=1;R='';E=-1
def G(c):
 o=[]
 for i,x in enumerate(B):
  if x=='.'or x.isupper()!=c:continue
  L=x.lower();f=i&7;r=i>>3
  if L=='p':
   q=r==(1 if c else 6);d=-8 if c else 8;j=i+d
   if j>=0 and B[j]=='.':
    if q:o+=[(i,j,z)for z in'qrbn']
    else:
     o.append((i,j,0))
     if r==(6 if c else 1)and B[j+d]=='.':o.append((i,j+d,0))
   for df in(-1,1):
    nf=f+df
    if 0<=nf<8:
     j=i+d+df
     if j>=0:
      y=B[j]
      if y!='.'and y.isupper()!=c:
       if q:o+=[(i,j,z)for z in'qrbn']
       else:o.append((i,j,0))
      elif j==E and y=='.':o.append((i,j,0))
  elif L in'nk':
   for dr,df in D[L]:
    nr=r+dr;nf=f+df
    if 0<=nr<8 and 0<=nf<8:
     j=nr*8+nf;y=B[j]
     if y=='.'or y.isupper()!=c:o.append((i,j,0))
   if L=='k':
    if c:
     if'K'in R and B[63]=='R'and B[61]==B[62]=='.'and not any(h(z,0)for z in(60,61,62)):o.append((60,62,0))
     if'Q'in R and B[56]=='R'and B[57]==B[58]==B[59]=='.'and not any(h(z,0)for z in(60,59,58)):o.append((60,58,0))
    else:
     if'k'in R and B[7]=='r'and B[5]==B[6]=='.'and not any(h(z,1)for z in(4,5,6)):o.append((4,6,0))
     if'q'in R and B[0]=='r'and B[1]==B[2]==B[3]=='.'and not any(h(z,1)for z in(4,3,2)):o.append((4,2,0))
  else:
   for dr,df in D[L]:
    nr=r+dr;nf=f+df
    while 0<=nr<8 and 0<=nf<8:
     j=nr*8+nf;y=B[j]
     if y=='.':
      o.append((i,j,0));nr+=dr;nf+=df
     else:
      if y.isupper()!=c:o.append((i,j,0))
      break
 return o
def h(s,col):
 f=s&7;r=s>>3
 for i,x in enumerate(B):
  if x=='.'or x.isupper()!=col:continue
  L=x.lower();ff=i&7;rr=i>>3;dx=f-ff;dy=r-rr
  if L=='p':
   if dy==(-1 if col else 1)and abs(dx)==1:return 1
  elif L=='n':
   if abs(dx*dy)==2:return 1
  elif L=='k':
   if max(abs(dx),abs(dy))==1:return 1
  elif L in'brq':
   if(L in'bq'and abs(dx)==abs(dy))or(L in'rq'and(dx==0 or dy==0)):
    sx=(dx>0)-(dx<0);sy=(dy>0)-(dy<0);X=ff+sx;Y=rr+sy
    while(X,Y)!=(f,r):
     if not(0<=X<8 and 0<=Y<8):break
     if B[Y*8+X]!='.':break
     X+=sx;Y+=sy
    else:return 1
 return 0
def M(m):
 global B,R,E,T
 v=(list(B),R,E)
 f,t,p=m;c=B[f];w=B[t];B[f]='.'
 if c.lower()=='p'and t==E and t&7!=f&7 and w=='.':
  B[t+8 if T else t-8]='.'
 B[t]=p.upper() if p and T else(p if p else c)
 if c.lower()=='k':
  if t in CA:
   r0,r1=CA[t];B[r1]='R' if T else'r';B[r0]='.'
  R=R.replace('K','').replace('Q','') if T else R.replace('k','').replace('q','')
 elif c.lower()=='r'and f in RM:R=R.replace(RM[f],'')
 if w!='.'and w.lower()=='r'and t in RM:R=R.replace(RM[t],'')
 E=(f+t)//2 if c.lower()=='p'and abs(f-t)==16 else -1
 T=not T
 return v
def U(v):global B,R,E,T;B,R,E=v;T=not T
def K(m):
 f,t,p=m;c=B[f];v=0;cap=0
 if B[t]!='.':v=V[B[t].lower()];cap=1
 elif c.lower()=='p'and t==E and t&7!=f&7:v=V['p'];cap=1
 if p:v+=V[p]
 if cap:return(0,-v*16+V[c.lower()])
 return(1,-V[c.lower()])
def L():
 ms=[]
 for m in G(T):
  if B[m[1]] in'Kk':continue
  v=M(m);k=B.index('K')if not T else B.index('k')
  if not h(k,T):ms.append(m)
  U(v)
 ms.sort(key=K)
 return ms
def e():
 s=0
 for j,c in enumerate(B):
  if c=='.':continue
  if c.isupper():s+=V[c.lower()]+P[c][j]
  else:s-=V[c]+P[c.upper()][j^56]
 return s if T else -s
def q(a,b,d=2):
 x=e()
 if x>=b:return b
 if x>a:a=x
 if d==0:return a
 for m in L():
  if m[2]or B[m[1]]!='.'or(B[m[0]].lower()=='p'and m[1]==E and m[1]&7!=m[0]&7):
   v=M(m);s=-q(-b,-a,d-1);U(v)
   if s>=b:return b
   if s>a:a=s
 return a
MATE=30000
NODES=0
def A(d,a,b,ply):
 ms=L()
 if not ms:
  k=B.index('K')if T else B.index('k')
  return -MATE+ply if h(k,not T)else 0
 if d==0:return q(a,b)
 best=-MATE-1
 for m in ms:
  v=M(m);s=-A(d-1,-b,-a,ply+1);U(v)
  if s>best:best=s
  if s>a:a=s
  if a>=b:break
 return best
def F(fen):
 global B,T,R,E
 p=fen.split();B=['.']*64;r=0
 for row in p[0].split('/'):
  f=0
  for ch in row:
   if ch.isdigit():f+=int(ch)
   else:B[r*8+f]=ch;f+=1
  r+=1
 T=p[1]=='w';R=p[2];E=-1
 if p[3]!='-':E=(8-int(p[3][1]))*8+ord(p[3][0])-97
def u(m):
 f,t,p=m
 return chr(97+(f&7))+str(8-(f>>3))+chr(97+(t&7))+str(8-(t>>3))+(p or'')
fen_set=F;legal=L;makemove=M;unmakemove=U
TT={}
def A(d,a,b,ply):
 global NODES;NODES+=1
 key=(tuple(B),T,d,a,b)
 c=TT.get(key)
 if c is not None:return c
 ms=L()
 if not ms:
  k=B.index('K')if T else B.index('k')
  v=-MATE+ply if h(k,not T)else 0
  TT[key]=v;return v
 if d==0:
  v=q(a,b);TT[key]=v;return v
 best=-MATE-1
 for m in ms:
  v=M(m);s=-A(d-1,-b,-a,ply+1);U(v)
  if s>best:best=s
  if s>a:a=s
  if a>=b:break
 TT[key]=best;return best
NODES=0
CAP=30000
class Boom(Exception):pass
def x(d,cap):
 global NODES
 ms=L()
 ms.sort(key=lambda m:0 if m[2]or B[m[1]]!='.'else 1)
 b=ms[0]if ms else None;bs=-MATE-2
 for m in ms:
  v=M(m);NODES+=1
  if NODES>cap:raise Boom()
  s=-A(d-1,-MATE,MATE,1);U(v)
  if s>bs:bs=s;b=m
 return b
def pick():
 global TT,NODES
 ms=L()
 if not ms:return None
 T0=time.perf_counter()
 TT={}
 try:
  b=x(2,2500)
 except Boom:
  b=ms[0]
 t2=time.perf_counter()-T0
 if t2<1.5:
  try:
   NODES=0;TT={};b2=x(3,6000)
   if NODES<=6000:b=b2
   t3=time.perf_counter()-T0
   if t3<4.0:
    try:
     NODES=0;TT={};b3=x(4,9000)
     if NODES<=9000:b=b3
    except Boom:pass
  except Boom:pass
 return b
if __name__=='__main__':
 ENV=os.environ.get('MAKEFUN_ENV_URL')
 if not ENV:sys.exit('MAKEFUN_ENV_URL is not set')
 def post(path,body):
  r=urllib.request.Request(ENV+path,data=json.dumps(body).encode(),headers={'content-type':'application/json'})
  try:
   with urllib.request.urlopen(r)as z:
    d=json.load(z)
    sys.stderr.write('%s %s -> status=%s game=%s\n'%(path,body.get('game'),d.get('status'),d.get('game')))
    return d
  except urllib.error.HTTPError as z:
   sys.stderr.write('%s %s -> HTTP %d\n'%(path,body,z.code))
   raise
 def safe(fn):
  for i in range(3):
   try:return fn()
   except Exception as z:
    sys.stderr.write('%s\n'%z)
    time.sleep(1)
  return None
 while 1:
  g=safe(lambda:post('/game',{}))
  if not g or g['status']=='done':break
  while g.get('status')=='your_move':
   F(g['fen']);mv=pick()
   if not mv:break
   sys.stderr.write('FEN=%s legal=%s mv=%s\n'%(g['fen'][:40],g.get('legal_moves',[])[:4],u(mv)))
   ng=safe(lambda:post('/move',{'game':g['game'],'move':u(mv)}))
   if ng is None:
    try:post('/resign',{'game':g['game']})
    except Exception:pass
    break
   g=ng
  if g and g.get('status')!='your_move':print("game %d: %s by %s"%(g['game'],g.get('outcome'),g.get('reason')),file=sys.stderr)
 print("done: %s won, %s drawn, %s lost"%(g.get('wins'),g.get('draws'),g.get('losses')),file=sys.stderr)
