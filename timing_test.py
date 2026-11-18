import time
import engine_v4 as M

FENS = [
    'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
    'r1bq1rk1/pp2bppp/2n1pn2/2p5/3P4/2N1PN2/PP2BPPP/R1BQ1RK1 w - - 0 1',
]
for f in FENS:
    M.F(f)
    t = time.time()
    mv = M.x(3)
    print('d3 %.2fs' % (time.time() - t), M.u(mv))
    M.F(f)
    t = time.time()
    mv = M.x(4)
    print('d4 %.2fs' % (time.time() - t), M.u(mv))
