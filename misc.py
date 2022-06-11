from itertools import chain

ROW = 8
COL = 8
SIZE = (ROW, COL)
BLOCKS = []

CUSTOM = True

EMPTY = 0
BLOCK = 1
BLACK = 2
WHITE = 3

C_EMPTY = '·'
C_BLOCK = ' '
C_BLACK = '●'
C_WHITE = '◯'
C_LEGAL = '*'

board = \
'''
0000
0000
0000
0000
'''

if CUSTOM:
    board = board.split()
    if not all([len(row) == len(board[0]) for row in board]):
        raise Exception('shape error')
    if not set(chain.from_iterable(board)).issubset({'0','1'}):
        raise Exception('value error')
    
    ROW = len(board)
    COL = len(board[0])

    BLOCKS = [i for i, c in enumerate(chain.from_iterable(board)) if c == '1']
