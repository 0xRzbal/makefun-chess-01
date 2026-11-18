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

def check(fen,d,label):
    M.fen_set(fen)
    m=perft_m(d); r=rec_ref(chess.Board(fen),d)
    print(label,'mine',m,'ref',r,'OK' if m==r else 'MISMATCH')

# Kiwipete without castling rights (get '-') - isolate castling
f='r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1'
check(f,3,'kiwi full')
check(f.replace(' KQkq',' -'),3,'kiwi norights')
# ep-only position
check('8/8/8/3pP3/8/8/8/8 w - d6 0 1',3,'ep white')
# emission: white pawn e4 captures ep d6. also black d5 pawn moves.
check('8/8/8/3p4/4P3/8/8/8 w - - 0 1',3,'noep')
