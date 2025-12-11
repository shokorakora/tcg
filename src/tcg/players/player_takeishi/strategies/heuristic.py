from typing import List, Tuple
from tcg.config import fortress_limit

# 調整用パラメータ
ATTACK_PAWN_THRESHOLD = 8     # 攻撃に出る最低兵数
NEUTRAL_PAWN_THRESHOLD = 6    # 中立拠点拡大に出す最低兵数
DEFENSE_ENEMY_NEAR = 6        # 近接敵の兵数がこの値以上なら防御優先
GLOBAL_SCORE_ATTACK = 12      # グローバルスコアがこの値以上なら攻撃方針に傾く

def evaluate_state(state: List[List[int]]) -> int:
    """
    現在のゲーム状態を軽量に評価する。
    - 自軍拠点の兵数・レベルは加点
    - 敵拠点の兵数・レベルは減点
    """
    score = 0
    for fortress in state:
        team, kind, level, pawn_number, upgrade_time, _ = fortress
        if team == 1:  # 自分の要塞
            score += pawn_number * 2
            score += level * 2
        elif team == 2:  # 相手の要塞
            score -= pawn_number
            score -= level
    return score

def can_upgrade(state: List[List[int]], i: int) -> bool:
    """
    拠点 i がアップグレード可能かチェック。
    条件:
      - 自軍拠点
      - upgrade_time == 0
      - 兵数 >= fortress_limit[level] // 2
    """
    team, _, level, pawn_number, upgrade_time, _ = state[i]
    if team != 1:
        return False
    if upgrade_time != 0:
        return False
    return pawn_number >= fortress_limit[level] // 2

def safe_neighbors(state: List[List[int]], i: int) -> Tuple[List[int], List[int]]:
    """
    隣接拠点を分類して返す。
    returns: (neutral_neighbors, enemy_neighbors)
    """
    neighbors = state[i][5]
    neutral = [n for n in neighbors if state[n][0] == 0]
    enemy = [n for n in neighbors if state[n][0] == 2]
    return neutral, enemy

def enemy_pressure(state: List[List[int]], i: int) -> int:
    """
    拠点 i 周辺の敵兵数合計（近傍脅威）の簡易推定。
    """
    neighbors = state[i][5]
    pressure = 0
    for n in neighbors:
        if state[n][0] == 2:
            pressure += state[n][3]
    return pressure

def choose_action(state: List[List[int]], moving_pawns: List[int]) -> Tuple[int, int, int]:
    """
    現在の状態に基づいて行動を選択する。
    優先度:
      1. 防御（強い敵が近い場合、無闇に兵を分散しない）
      2. アップグレード（条件満たす自軍拠点）
      3. 攻撃（有利なとき、弱い隣接敵へ）
      4. 中立拠点拡大（兵数が閾値超）
      5. 何もしない
    """
    # デフォルトは何もしない
    command, subject, to = 0, 0, 0

    # 1. 防御チェック：敵圧力が強い拠点は兵を保持
    # ここでは「防御」は積極行動を返さず保持する方針（必要なら再配置戦略を追加）
    for i in range(len(state)):
        if state[i][0] != 1:
            continue
        pressure = enemy_pressure(state, i)
        if pressure >= DEFENSE_ENEMY_NEAR and state[i][3] < ATTACK_PAWN_THRESHOLD + 4:
            # 近接敵が強い場合は守り優先（何もしない）
            return command, subject, to

    # 2. アップグレード優先（生産加速は長期で有利）
    for i in range(len(state)):
        if can_upgrade(state, i):
            return 2, i, 0

    global_score = evaluate_state(state)

    # 3. 攻撃：有利時のみ、隣接の弱い敵を狙う
    if global_score >= GLOBAL_SCORE_ATTACK:
        # 兵数が多い拠点から優先
        my_forts = [(i, state[i][3]) for i in range(len(state)) if state[i][0] == 1]
        my_forts.sort(key=lambda x: x[1], reverse=True)
        for i, pawns in my_forts:
            if pawns < ATTACK_PAWN_THRESHOLD:
                continue
            neutral, enemy = safe_neighbors(state, i)
            if enemy:
                # 最も弱い敵隣接を選ぶ
                target = min(enemy, key=lambda n: (state[n][3], state[n][2]))
                # 送るのは自動で半分だが、最低兵数を満たすときのみ
                return 1, i, target

    # 4. 中立拠点拡大：兵数が閾値を超える自軍拠点から近隣中立へ進出
    my_forts = [(i, state[i][3]) for i in range(len(state)) if state[i][0] == 1]
    my_forts.sort(key=lambda x: x[1], reverse=True)
    for i, pawns in my_forts:
        if pawns < NEUTRAL_PAWN_THRESHOLD:
            continue
        neutral, enemy = safe_neighbors(state, i)
        if neutral:
            # 兵の少ない中立から順に占領を狙う（中立は team=0 なので pawn_number は小さいことが多い）
            target = min(neutral, key=lambda n: (state[n][3], state[n][2]))
            return 1, i, target

    # 5. 何もしない
    return command, subject, to

def heuristic_strategy(info) -> Tuple[int, int, int]:
    """
    ヒューリスティックな戦略に基づいた行動選択関数。
    info = (team, state, moving_pawns, spawning_pawns, done)
    """
    team, state, moving_pawns, spawning_pawns, done = info
    # チーム視点は既に自分=1に正規化されている前提
    return choose_action(state, moving_pawns)