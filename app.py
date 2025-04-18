from flask import Flask, request
from legalMove import findAll, isIsolated
from board import fmt, Board66
import ulid
import json
import os

app = Flask(__name__)

def play(game, note):
    b = Board66(game['board'])
    if note.startswith('+') or note.startswith(' '):
        if b.get(note[1:]) == 0 and game['hand'][game['turn']-2] > 0:
            b.place(note[1:], 1)
            game['hand'][game['turn'] - 2] -= 1
            oper = '+'
        else:
            return game, 'not empty or none left'
    elif note[1:] in [fmt(i) for i in game['legal']]:
        orig = b.locate(game['turn'])
        piece = b.get(note[1:])
        b.place(orig, 0)
        b.place(note[1:], game['turn'])
        if piece == 1:
            game['hand'][game['turn'] - 2] += 1
            oper = '='
            oploc = b.locate(3 if game['turn'] == 2 else 2)
            if oploc is not None:
                if isIsolated(b, oploc):
                    game['res'] = game['turn']
        if piece == (3 if game['turn'] == 2 else 2):
            game['res'] = game['turn']
            oper = '='
        else:
            oper = '-'
        if note[1:] == ('f6' if game['turn'] == 2 else 'a1'):
            game['res'] = game['turn']
    else:
        return game, 'illegal move'
    game['hist'].append(oper + note[1:])
    game['turn'] = (3 if game['turn'] == 2 else 2)
    if game['res'] == 0:
        game['legal'] = list(findAll(b, game['turn']))
    return game, ''



@app.route('/api', methods=['GET'])
def home():
    act =  request.args.get('act')
    if act == 'start':
        b = Board66([[2,1,0,0,0,1],[1,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,1],[1,0,0,0,1,3]])
        game = {
            'id': ulid.new().str,
            'board': b.data,
            'hand': [11,11],
            'turn': 2,
            'legal': list(findAll(b, 2)),
            'hist': [],
            'res': 0
        }
        with open(f'game/{game["id"]}.json', 'w', -1, 'utf-8') as f:
            json.dump(game, f)
        jsonText = json.dumps(game)
        if jsonText is None:
            return 'none'
        return jsonText
    if act == 'move':
        gameid = request.args.get('id')
        note = request.args.get('move')
        if note is None:
            note = '+a1'
        # draw = request.args.get('draw')
        # if draw is None:
        #     draw = 0
        if f'{gameid}.json' not in os.listdir('game'):
            return 'id does not exist'
        with open(f'game/{gameid}.json', 'r', -1, 'utf-8') as f:
            game = json.load(f)
        game, result = play(game, note)
        if result == '':
            with open(f'game/{gameid}.json', 'w', -1, 'utf-8') as f:
                json.dump(game, f)
            jsonText = json.dumps(game)
            if jsonText is None:
                return 'none'
            return jsonText
        return result
    if act == 'draw':
        gameid = request.args.get('id')
        if f'{gameid}.json' not in os.listdir('game'):
            return 'id does not exist'
        with open(f'game/{gameid}.json', 'r', -1, 'utf-8') as f:
            game = json.load(f)
        b = Board66(game['board'])
        return '<br>'.join(b.draw().split('\n'))
    if act == 'showlegal':
        gameid = request.args.get('id')
        if f'{gameid}.json' not in os.listdir('game'):
            return 'id does not exist'
        with open(f'game/{gameid}.json', 'r', -1, 'utf-8') as f:
            game = json.load(f)
        b = Board66(game['board'])
        s = set(tuple(i) for i in game['legal'])
        return '<br>'.join(b.draw(s).split('\n'))
    if act == 'replay':
        gameid = request.args.get('id')
        draw = request.args.get('draw')
        if f'{gameid}.json' not in os.listdir('game'):
            return 'id does not exist'
        with open(f'game/{gameid}.json', 'r', -1, 'utf-8') as f:
            game = json.load(f)
        b = Board66([[2,1,0,0,0,1],[1,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,1],[1,0,0,0,1,3]])
        gameDict = {
            'id': 'replay',
            'board': b.data,
            'hand': [11,11],
            'turn': 2,
            'legal': list(findAll(b, 2)),
            'hist': [],
            'res': 0
        }
        replayList = '[' + json.dumps({'board': gameDict['board'], 'hand': gameDict['hand']})
        pic = '<br>'.join(b.draw().split('\n')) + '<br><br>'
        for i in game['hist']:
            gameDict = play(gameDict, i)[0]
            replayList += (',' + json.dumps({'board': gameDict['board'], 'hand': gameDict['hand']}))
            pic += '<br>'.join(Board66(gameDict['board']).draw().split('\n')) + '<br><br>'
        replayList = replayList + ']'
        ret = {
            'hist': game['hist'],
            'res': game['res'],
            'states': json.loads(replayList)
        }
        del gameDict
        if draw is not None:
            return pic
        return json.dumps(ret)
    return 'none'

@app.route('/about')
def about():
    return 'About'

if __name__ == '__main__':
    app.run(debug=False, port=2010)
