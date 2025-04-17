# Kinboise

n = (-1, 0)
e = (0, 1)
s = (1, 0)
w = (0, -1)
dirs = (n, e, s, w)

def findFrom(board, route, dests):
    # route = routes[rid]
    p0 = route[-1]
    d0 = move(p0, rev(route[-2]))
    for d in dirs:
        p = move(p0, d)
        if d != rev(d0) and board.get(p) != -1:
            if d == d0:
                dests.add(p)
                # print(route)
            if board.get(p) == 1 and p not in route:
                findFrom(board, route+(p,), dests)

def findAll(board, turn):
    start = None
    for row in range(len(board.data)):
        for col in range(len(board.data[row])):
            if board.get((col, row)) == turn:
                start = (col, row)
    if start is None:
        return set()
    dests = set()
    for d0 in dirs:
        p = move(start, d0)
        if board.get(p) == 1:
            findFrom(board, (start, p), dests)
    return dests

def move(p, d):
    return (p[0]+d[0], p[1]+d[1])

def rev(d):
    return (d[0]*-1, d[1]*-1)
    # return tuple(-1 * i for i in list(d))

def isIsolated(board, loc):
    for d0 in dirs:
        p = move(loc, d0)
        if board.get(p) == 1:
            return False
    return True
