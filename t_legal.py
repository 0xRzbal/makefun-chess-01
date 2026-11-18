import chess, main as M

def uci_of(m):
    f,t,p=m
    return chr(97+f%8)+str(8-f//8)+chr(97+t%8)+str(8-t//8)+(p or '')

for fen in [
 'r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1',
 '8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1',
]:
    M.fen_set(fen)
    mine=set(uci_of(m) for m in M.legal())
    ref=set(mv.uci() for mv in chess.Board(fen).legal_moves)
    print(fen[:30])
    print('  extra mine:', sorted(mine-ref))
    print('  missing  :', sorted(ref-mine))
