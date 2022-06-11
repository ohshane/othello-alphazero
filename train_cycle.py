# ====================
# 학습 사이클 실행
# ====================

from tqdm import tqdm

from dual_network import dual_network
from evaluate_network import evaluate_network
from self_play import self_play
from train_network import train_network

# 듀얼 네트워크 생성
dual_network()

cycle = 10
for i in tqdm(range(cycle)):
    print(f'========== TRAIN CYCLE {i}/{cycle} ==========')
    # 셀프 플레이 파트
    self_play()

    # 파라미터 변경 파트
    train_network()

    # 신규 파라미터 평가 파트
    evaluate_network()
