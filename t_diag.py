import chess, main as M

def uci_of(m):
    f,t,p=m
    return chr(97+f%8)+str(8-f//8)+chr(97+t%8)+str(8-t//8)+(p or '')

fen='r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w - - 0 1'
M.fen_set(fen)
ref=chess.Board(fen)
tot=0
# find our moves not in ref
mine=set(uci_of(m) for m in M.legal())
r=set(mv.uci() for mv in ref.legal_moves)
print('root extra:', sorted(mine-r))
print('root missing:', sorted(r-mine))
# for each child where next-level differs, show an offending move
for m in M.legal():
    u=uci_of(m)
    mv=chess.Move.from_uci(u)
    saved=M.makemove(m)
    ref.push(mv)
    mm=set(uci_of(x) for x in M.legal())
    rr=set(x.uci() for x in ref.legal_moves)
    if mm!=rr:
        print(u,'extra',sorted(mm-rr)[:8],'missing',sorted(rr-mm)[:8])
    ref.pop()
    M.unmakemove(saved)
