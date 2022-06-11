# ====================
# 오셀로
# ====================

import math
import random

from misc import *


# 게임 상태
class State:
    # 초기화
    def __init__(self, pieces=None, enemy_pieces=None, depth=0):
        # 방향 정수
        self.dxy = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))

        # 연속 패스에 따른 종료
        self.pass_end = False

        # 돌의 배치
        self.pieces = pieces
        self.enemy_pieces = enemy_pieces
        self.depth = depth

        # 돌의 초기 배치
        if pieces == None or enemy_pieces == None:
            self.pieces = [0] * (ROW*COL)
            self.pieces[COL*(ROW//2-1) + COL//2] = self.pieces[COL*(ROW//2+1) - COL//2 - 1] = 1
            self.enemy_pieces = [0] * (ROW*COL)
            self.enemy_pieces[COL*(ROW//2-1) + COL//2 - 1] = self.enemy_pieces[COL*(ROW//2+1) - COL//2] = 1

    # 돌의 수 얻기
    def piece_count(self, pieces):
        count = 0
        for i in pieces:
            if i == 1:
                count += 1
        return count

    # 패배 여부 판정
    def is_lose(self):
        return self.is_done() and self.piece_count(self.pieces) < self.piece_count(self.enemy_pieces)

    # 무승부 여부 판정
    def is_draw(self):
        return self.is_done() and self.piece_count(self.pieces) == self.piece_count(self.enemy_pieces)

    # 게임 종료 여부 판정
    def is_done(self):
        return self.piece_count(self.pieces) + self.piece_count(self.enemy_pieces) == (ROW*COL)-len(BLOCKS) or self.pass_end

    # 다음 상태 얻기
    def next(self, action):
        state = State(self.pieces.copy(), self.enemy_pieces.copy(), self.depth + 1)
        if action != ROW*COL:
            state.is_legal_action_xy(action % COL, int(action / COL), True)
        w = state.pieces
        state.pieces = state.enemy_pieces
        state.enemy_pieces = w

        # 2회 연속 패스 판정
        if action == ROW*COL and state.legal_actions() == [ROW*COL]:
            state.pass_end = True
        return state

    # 합법적인 수 리스트 얻기
    def legal_actions(self):
        actions = []
        for j in range(0, ROW):
            for i in range(0, COL):
                if self.is_legal_action_xy(i, j):
                    actions.append(i + j * COL)
        if len(actions) == 0:
            actions.append(ROW*COL)  # 패스
        return actions

    # 임의의 매스가 합법적인 수인지 판정
    def is_legal_action_xy(self, x, y, flip=False):
        # 임의의 매스에서 임의의 방향이 합법적인 수인지 판정
        def is_legal_action_xy_dxy(x, y, dx, dy):
            # １번째 상대의 돌
            x, y = x + dx, y + dy
            if y < 0 or ROW-1 < y or x < 0 or COL-1 < x or \
                    self.enemy_pieces[x + y * COL] != 1 or \
                    (x + y * COL) in BLOCKS:
                return False

            # 2번째 이후
            for j in range(max(ROW,COL)):
                # 빈 칸
                if y < 0 or ROW-1 < y or x < 0 or COL-1 < x or \
                        (self.enemy_pieces[x + y * COL] == 0 and self.pieces[x + y * COL] == 0) or \
                        (x + y * COL) in BLOCKS:
                    return False

                # 자신의 돌
                if self.pieces[x + y * COL] == 1:
                    # 반전
                    if flip:
                        for i in range(max(ROW,COL)):
                            x, y = x - dx, y - dy
                            if self.pieces[x + y * COL] == 1:
                                return True
                            self.pieces[x + y * COL] = 1
                            self.enemy_pieces[x + y * COL] = 0
                    return True
                # 상대의 돌
                x, y = x + dx, y + dy
            return False

        # 빈칸 없음
        if self.enemy_pieces[x + y * COL] == 1 or self.pieces[x + y * COL] == 1 or (x + y * COL) in BLOCKS:
            return False

        # 돌을 놓음
        if flip:
            self.pieces[x + y * COL] = 1

        # 임의의 위치의 합법적인 수 여부 확인
        flag = False
        for dx, dy in self.dxy:
            if is_legal_action_xy_dxy(x, y, dx, dy):
                flag = True
        return flag

    # 선 수 여부 확인
    def is_first_player(self):
        return self.depth % 2 == 0

    # 문자열 표시
    def __repr__(self):
        ox = (C_BLACK, C_WHITE) if self.is_first_player() else (C_WHITE, C_BLACK)
        str = []
        row = ''
        for i in range(ROW*COL):
            if self.pieces[i] == 1:
                row += ox[0]
            elif self.enemy_pieces[i] == 1:
                row += ox[1]
            elif i in BLOCKS:
                row += C_BLOCK
            else:
                row += C_EMPTY
            if i % COL == COL-1:
                str.append(' '.join(row))
                row = ''
        return '\n'.join(str)


# 랜덤으로 행동 선택
def random_action(state):
    legal_actions = state.legal_actions()
    return legal_actions[random.randint(0, len(legal_actions) - 1)]


# 동작 확인
if __name__ == '__main__':
    # 상태 생성
    state = State()

    # 게임 종료 시까지 반복
    while True:
        # 게임 종료 시
        if state.is_done():
            break

        # 다음 상태 얻기
        state = state.next(random_action(state))

        # 문자열 출력
        print(f'depth: {state.depth}')
        print(f'turn : {"BLACK" if state.is_first_player() else "WHITE"}')

        print(state)
        b, w = state.piece_count(state.pieces), state.piece_count(state.enemy_pieces)
        if not state.is_first_player:
            b, w = w, b

        print(f'BLACK {b} {"✓" if b > w else ""}')
        print(f'WHITE {w} {"✓" if w > b else ""}')
        print('─'*30)