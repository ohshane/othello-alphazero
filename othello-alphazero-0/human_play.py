# ====================
# 사람과 AI의 대전
# ====================

import tkinter as tk
from pathlib import Path
from threading import Thread

from tensorflow.keras.models import load_model

from game import State
from misc import *
from pv_mcts import pv_mcts_action

# 베스트 플레이어 모델 로드
model = load_model('./model/best.h5')

SIZE = 40

# 게임 UI 정의
class GameUI(tk.Frame):
    # 초기화
    def __init__(self, master=None, model=None):
        tk.Frame.__init__(self, master)
        self.master.title(f'Othello {ROW}x{COL}')

        # 게임 상태 생성
        self.state = State()

        # PV MCTS를 활용한 행동을 선택하는 함수 생성
        self.next_action = pv_mcts_action(model, 0.0)

        # 캔버스 생성
        self.c = tk.Canvas(self, width=SIZE*COL, height=SIZE*ROW, highlightthickness=0)
        self.c.bind('<Button-1>', self.turn_of_human)
        self.c.pack()

        # 화면 갱신
        self.on_draw()

    # 사람의 턴
    def turn_of_human(self, event):
        # 게임 종료 시
        if self.state.is_done():
            self.state = State()
            self.on_draw()
            return

        # 선 수가 아닌 경우
        if not self.state.is_first_player():
            return

        # 클릭 위치를 행동으로 변환
        x = int(event.x / SIZE)
        y = int(event.y / SIZE)
        if x < 0 or COL-1 < x or y < 0 or ROW-1 < y:  # 범위 외
            return
        action = x + y * ROW

        # 합법적인 수가 아닌 경우
        legal_actions = self.state.legal_actions()
        if legal_actions == [ROW*COL]:
            action = ROW*COL  # 패스
        if action != ROW*COL and not (action in legal_actions):
            return

        # 다음 상태 얻기
        self.state = self.state.next(action)
        self.on_draw()

        # AI의 턴
        self.master.after(1, self.turn_of_ai)

    # AI의 턴
    def turn_of_ai(self):
        # 게임 종료 시
        if self.state.is_done():
            return

        # 행동 얻기
        action = self.next_action(self.state)

        # 다음 상태 얻기
        self.state = self.state.next(action)
        self.on_draw()

    # 돌 그리기
    def draw_piece(self, index, first_player):
        x = (index % ROW) * SIZE + 5
        y = int(index / COL) * SIZE + 5
        if first_player:
            self.c.create_oval(x, y, x + (SIZE - 2*5), y + (SIZE - 2*5), width=1.0, outline='#000000', fill='#121A18')
        else:
            self.c.create_oval(x, y, x + (SIZE - 2*5), y + (SIZE - 2*5), width=1.0, outline='#000000', fill='#F5FEFA')

    # 화면 갱신
    def on_draw(self):
        self.c.delete('all')
        self.c.create_rectangle(0, 0, SIZE*COL, SIZE*ROW, width=0.0, fill='#009067')
        for i in range(ROW*COL):
            if i in BLOCKS:
                x = (i % COL)*SIZE
                y = (i // COL)*SIZE
                self.c.create_rectangle(x, y, x+SIZE, y+SIZE, width=0.0, fill='#FFFFFF')
        for i in range(1, ROW+2):
            self.c.create_line(0, i * SIZE, SIZE*ROW, i * SIZE, width=1.0, fill='#000000')
            self.c.create_line(i * SIZE, 0, i * SIZE, SIZE*COL, width=1.0, fill='#000000')
        for i in range(ROW*COL):
            if self.state.pieces[i] == 1:
                self.draw_piece(i, self.state.is_first_player())
            if self.state.enemy_pieces[i] == 1:
                self.draw_piece(i, not self.state.is_first_player())
        for i in range(ROW*COL):
            if i in self.state.legal_actions():
                x = (i % COL)*SIZE + SIZE*0.45
                y = int(i / COL)*SIZE + SIZE*0.45
                self.c.create_oval(x, y, x+SIZE*0.1, y+SIZE*0.1, width=0.0, fill='#FFFFFF')

        print('-'*20)
        print(f'depth: {self.state.depth}')
        print(f'turn : {"BLACK" if self.state.is_first_player() else "WHITE"}')
        b, w = self.state.piece_count(self.state.pieces), self.state.piece_count(self.state.enemy_pieces)
        if not self.state.is_first_player:
            b, w = w, b

        print(f'BLACK {b} {"✓" if b > w else ""}')
        print(f'WHITE {w} {"✓" if w > b else ""}')

# 게임 UI 실행
f = GameUI(model=model)
f.pack()
f.mainloop()
