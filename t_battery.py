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

tests=[
 ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',4),
 ('r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1',3),
 ('8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1',4),
 ('rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8',3),
 ('r4rk1/1pp1qppp/p1np1n2/4p1B1/2P1P3/1Q3NP1/PP1P1P1P/2KR3R w - - 0 1',3),
 ('1n1R4/1k6/8/4K3/8/8/8/8 w - - 0 1',3),
 ('4k3/8/8/8/8/8/8/4K2R w K - 0 1',3),
 ('rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2',3),
 ('8/5p2/8/8/8/8/8/2K2k2 w - - 0 1',2),
 ('r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1',2),
 ('4k3/8/8/8/8/8/8/4K3 w - - 0 1',3),
 ('8/8/8/3pP3/8/8/8/4K2k w - d6 0 1',3),
 ('8/8/8/3p4/4P3/8/8/4K2k w - - 0 1',3),
]
bad=0
for f,d in tests:
    try:
        M.fen_set(f)
        m=perft_m(d)
        r=rec_ref(chess.Board(f),d)
    except Exception as ex:
        print('ERR',f[:40],type(ex).__name__,ex); bad+=1; continue
    status='OK' if m==r else 'MISMATCH'
    if m!=r: bad+=1
    print(status,'mine',m,'ref',r,'depth',d,f[:44])
print('BAD COUNT',bad)
