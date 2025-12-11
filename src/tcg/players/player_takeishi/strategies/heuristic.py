from typing import List, Tuple

def evaluate_state(state: List[List[int]]) -> int:
    """
    現在のゲーム状態を評価する関数。
    
    引数:
        state: ゲームの状態を表すリスト。
    
    返り値:
        int: 状態の望ましさを表すスコア。
    """
    score = 0
    for fortress in state:
        team, kind, level, pawn_number, upgrade_time, _ = fortress
        if team == 1:  # 自分の要塞
            score += pawn_number * 2  # 部隊数に比例してスコアが増える(係数は調整可能)
            score += level * 1  # レベルに比例してスコアが増える(係数は調整可能)
        elif team == 2:  # 相手の要塞
            score -= pawn_number  # 相手の部隊数分スコアを減らす
            score -= level  # 相手のレベル分スコアを減らす
    return score

def choose_action(state: List[List[int]], moving_pawns: List[int]) -> Tuple[int, int, int]:
    """
    現在の状態に基づいて行動を選択する関数。
    
    引数:
        state: ゲームの状態を表すリスト。
        moving_pawns: 現在移動中の部隊のリスト。
    
    返り値:
        Tuple[int, int, int]: 選択されたコマンド、対象、目標。
    """
    command, subject, to = 0, 0, 0 # デフォルトは何もしない
    score = evaluate_state(state) # 現在状態の評価値を取得

    if score > 10:  # 強いポジションにある場合(閾値は調整可能)
        for i in range(len(state)):
            if state[i][0] == 1 and state[i][3] > 5:  # 自分の要塞で十分な部隊がいる場合
                neighbors = state[i][5]  # 隣接する要塞リストを取得
                enemy_neighbors = [n for n in neighbors if state[n][0] == 2] # 隣接要塞のうち敵の要塞のみ抽出
                if enemy_neighbors:
                    return 1, i, enemy_neighbors[0]  # コマンド(1=移動)、送出元i、送り先最初の敵隣接要塞 (要するに攻撃)

    return command, subject, to  # 攻撃条件に該当しない場合は、デフォルト(何もしない)

def heuristic_strategy(info) -> Tuple[int, int, int]:
    """
    ヒューリスティックな戦略に基づいた行動選択関数。
    
    引数:
        info: チーム、状態、移動中の部隊などのゲーム情報。
    
    返り値:
        Tuple[int, int, int]: 選択されたコマンド、対象、目標。
    """
    team, state, moving_pawns, spawning_pawns, done = info
    return choose_action(state, moving_pawns)