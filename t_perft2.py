import main as M
def perft(d):
    if d==0: return 1
    n=0
    for m in M.legal():
        saved=M.makemove(m)
        n+=perft(d-1)
        M.unmakemove(saved)
    return n
for f,depth in [
 ('r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1',3),
 ('8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1',4),
 ('rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8',3),
]:
    M.fen_set(f)
    print('---')
    for d in range(1,depth+1):
        print('perft',d,perft(d))
