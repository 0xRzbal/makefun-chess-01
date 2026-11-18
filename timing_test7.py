import time
import engine_v8 as M

FENS = [
    'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
    'r1bq1rk1/pp2bppp/2n1pn2/2p5/3P4/2N1PN2/PP2BPPP/R1BQ1RK1 w - - 0 1',
    'r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1',
    '8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1',
]
for f in FENS:
    M.F(f)
    t = time.time()
    mv = M.pick()
    print('pick %.2fs' % (time.time() - t), M.u(mv), 'nodes:', M.NODES)
