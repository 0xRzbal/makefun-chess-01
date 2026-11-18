import time, main as M
for fen in [
 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
 'r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1',
 'r1bq1rk1/pp2bppp/2n1pn2/2p5/3P4/2N1PN2/PP2BPPP/R1BQ1RK1 w - - 0 1',
]:
    M.fen_set(fen)
    t=time.time()
    mv=M.root(3)
    dt=time.time()-t
    print('%.2fs'%dt, M.uci(mv), fen[:40])
