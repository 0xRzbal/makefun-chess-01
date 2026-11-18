import chess, main as M

def perft_m(d):
    if d==0: return 1
    n=0
    for m in M.legal():
        saved=M.makemove(m)
        n+=perft_m(d-1)
        M.unmakemove(saved)
    return n

def perft_ref(fen,d):
    b=chess.Board(fen)
    def rec(board,d):
        if d==0: return 1
        n=0
        for mv in board.legal_moves:
            board.push(mv); n+=rec(board,d-1); board.pop()
        return n
    return rec(b,d)

fens=[
 ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',3),
 ('r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1',3),
 ('8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1',4),
 ('rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8',3),
 ('r4rk1/1pp1qppp/p1np1n2/4p1B1/2P1P3/1Q3NP1/PP1P1P1P/2KR3R w - - 0 1',2),
 ('8/8/8/8/8/1k6/8/K7 w - - 0 1',1),
]
for f,d in fens:
    M.fen_set(f)
    m=perft_m(d)
    r=perft_ref(f,d)
    print('OK' if m==r else 'MISMATCH', 'mine',m,'ref',r,'depth',d,f[:40])
