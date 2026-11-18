import time
import engine_v6 as M

FENS = [
    'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
    'r1bq1rk1/pp2bppp/2n1pn2/2p5/3P4/2N1PN2/PP2BPPP/R1BQ1RK1 w - - 0 1',
    'r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1',
]

def pick_budgeted(cap=80000):
    ms = M.L()
    if not ms:
        return None
    best = None
    for d in (2, 3, 4):
        M.TT = {}
        try:
            best = M.x(d)
        except Exception:
            break
        if M.NODES > cap:
            break
    return best

for f in FENS:
    M.F(f)
    t = time.time()
    mv = pick_budgeted()
    print('pick %.2fs' % (time.time() - t), M.u(mv), 'nodes:', M.NODES)
