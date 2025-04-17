def fmt(p, board=None, turn=None):
    if board is None:
        o = ''
    else:
        if board.get(p) == 0 or board.get(p) == turn:
            o = '-'
        else:
            o = '='
    return o + chr(97 + p[0]) + str(p[1] + 1)

class Board66():
    def __init__(self, data=[[2,1,0,0,0,1],[1,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,1],[1,0,0,0,1,3]]):
        self.data = data
    def locate(self, piece):
        for row in range(len(self.data)):
            for col in range(len(self.data[row])):
                if self.get((col, row)) == piece:
                    return (col, row)
        return None
    def get(self, pos):
        if isinstance(pos, tuple) and len(pos) == 2:
            x = int(pos[0])
            y = int(pos[1])
        elif isinstance(pos, str) and len(pos) > 1:
            if pos[0].isupper():
                x = ord(pos[0]) - 65
            else:
                x = ord(pos[0]) - 97
            y = int(pos[1:]) - 1
        else:
            return -2
        if x < 0 or x > 5 or y < 0 or y > 5:
            return -1
        else:
            return self.data[y][x]
    def place(self, pos, piece):
        if isinstance(pos, tuple) or isinstance(pos, list) and len(pos) == 2:
            x = int(pos[0])
            y = int(pos[1])
        elif isinstance(pos, str) and len(pos) > 1:
            if pos[0].isupper():
                x = ord(pos[0]) - 65
            else:
                x = ord(pos[0]) - 97
            y = int(pos[1:]) - 1
        else:
            return -2
        if x < 0 or x > 5 or y < 0 or y > 5:
            return -1
        else:
            self.data[y][x] = piece
            return 0
    def draw(self, set=set()):
        glyphs = {
            False: {0: '⬜', 1: '⬛', 2: '⚫', 3: '⚪'},
            True: {0: '🟩', 1: '🟥', 2: '🔴', 3: '🟢'}
        }
        pic = ''
        for y,row in enumerate(self.data):
            for x,pos in enumerate(row):
                pic += glyphs[(x,y) in set][pos]
            pic += '\n'
        return pic.rstrip('\n')