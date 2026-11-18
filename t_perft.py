import main as M
def perft(d):
    if d==0: return 1
    n=0
    for m in M.legal():
        saved=M.makemove(m)
        n+=perft(d-1)
        M.unmakemove(saved)
    return n
M.fen_set('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
for d in (1,2,3,4):
    print('perft',d,perft(d))
