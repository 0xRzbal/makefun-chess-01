import chess, main as M

def perft_m(d):
    if d==0: return 1
    n=0
    for m in M.legal():
        saved=M.makemove(m)
        n+=perft_m(d-1)
        M.unmakemove(saved)
    return n

def rec_ref(board,d):
    if d==0: return 1
    n=0
    for mv in board.legal_moves:
        board.push(mv); n+=rec_ref(board,d-1); board.pop()
    return n

fen='r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1'
M.fen_set(fen)
ref=chess.Board(fen)
for m in M.legal():
    u=chr(97+m[0]%8)+str(8-m[0]//8)+chr(97+m[1]%8)+str(8-m[1]//8)+(m[2] or '')
    mv=chess.Move.from_uci(u)
    saved=M.makemove(m)
    ref.push(mv)
    mm=perft_m(2)
    rr=rec_ref(ref,2)
    ref.pop()
    M.unmakemove(saved)
    if mm!=rr:
        print('DIFF',u,'mine',mm,'ref',rr)
