from typing import List, Tuple

def evaluate_state(state: List[List[int]], team: int = 1) -> float:
    """
    現在のゲーム状態のざっくり評価（軽量版）。
    - 自軍（team=1）の兵数・レベルは加点
    - 敵（team=2）の兵数・レベルは減点
    """
    score = 0.0
    for fortress in state:
        fortress_team, fortress_kind, fortress_level, pawn_number, upgrade_time, neighbors = fortress
        if fortress_team == team:
            score += pawn_number * 2.0
            score += fortress_level * 2.0
        elif fortress_team == 2:
            score -= pawn_number * 1.0
            score -= fortress_level * 1.0
    return score

def score_action(state: List[List[int]], action: Tuple[int, int, int]) -> float:
    """
    単一アクションの「期待度」を簡易に採点するヒューリスティック。
    command: 0=何もしない, 1=移動, 2=アップグレード
    """
    command, subject, to = action

    # 何もしない
    if command == 0:
        return 0.0

    # 範囲・自軍チェック（安全対策）
    if subject < 0 or subject >= len(state):
        return -1e6
    if state[subject][0] != 1:
        return -1e6

    # アップグレード
    if command == 2:
        level = state[subject][2]
        pawn_number = state[subject][3]
        upgrade_time = state[subject][4]
        fortress_limit = [10, 10, 20, 30, 40, 50]
        if upgrade_time == 0 and pawn_number >= fortress_limit[level] // 2:
            # 生産速度アップは強力なので加点を高めに
            return 15.0 + level * 2.0
        else:
            return -100.0  # 無効または非効率

    # 部隊移動
    if command == 1:
        neighbors = state[subject][5]
        if to not in neighbors:
            return -1e6  # 無効な移動先
        from_pawns = state[subject][3]
        sent = from_pawns // 2  # 仕様上「半分」を送る
        target_team = state[to][0]
        target_level = state[to][2]
        target_pawns = state[to][3]

        # 中立に進出は取りやすいので加点
        if target_team == 0:
            # 中立は兵が少ないことが多い。送る兵が多いほど加点。
            return 5.0 + min(sent, 10) - target_level

        # 敵に攻撃は、相手兵数との相対で評価
        if target_team == 2:
            # 相手が弱いほど加点。レベルが高い敵は減点。
            margin = sent - (target_pawns + target_level * 2)
            return 8.0 + margin

        # 自軍へ移動（再配置）は基本ゼロ。将来の防御・攻勢準備として少加点もあり得る
        if target_team == 1:
            # 再配置は慎重に。敵圧力が高い位置に集めるなどの高度ロジックは別途。
            return 1.0

    # その他（未知コマンド）
    return -1000.0

def evaluate_strategy(state: List[List[int]], team: int) -> float:
    """
    戦略の有効性を現在のゲーム状態に基づいて評価する関数（軽量グローバル評価）。
    """
    return evaluate_state(state, team)

def compare_strategies(strategy_a, strategy_b, info) -> str:
    """
    2つの戦略を一歩先のアクション期待度で比較する。
    strategy_* は info を受けて (command, subject, to) を返す関数を想定。
    """
    # info = (team, state, moving_pawns, spawning_pawns, done)
    team, state, moving_pawns, spawning_pawns, done = info

    action_a = strategy_a(info)
    action_b = strategy_b(info)

    score_a = score_action(state, action_a)
    score_b = score_action(state, action_b)

    if score_a > score_b:
        return "Strategy A is better"
    elif score_b > score_a:
        return "Strategy B is better"
    else:
        return "Both strategies are equal"