def evaluate_strategy(state, team):
    """
    戦略の有効性を現在のゲーム状態に基づいて評価する関数

    引数:
        state (list): 現在のゲーム状態。要塞の状態などの情報を含む。
        team (int): プレイヤーのチームID（1は自分、2は相手）。
    返り値:
        float: 戦略の有効性を表すスコア
    """
    score = 0.0

    # 例: 評価ロジック
    for fortress in state: # 各要塞の状態を評価
        fortress_team, fortress_kind, fortress_level, pawn_number, upgrade_time, neighbors = fortress
        # fortress_teamは要塞の所属(0は中立、1は自分、2は相手)
        # fortress_kindは要塞の種類(速い要塞、強い要塞など)
        # fortress_levelは要塞のレベル(1-5)
        # pawn_numberは要塞にいる部隊数
        # upgrade_timeはアップグレード中の残り時間
        # neighborsは隣接要塞のリスト
        if fortress_team == team: # 自分の要塞の場合 
            score += pawn_number * 1.0  # 部隊数に比例してスコアを加算(係数は調整可能)
            score += fortress_level * 2.0  # レベルに比例してスコアを加算(係数は調整可能)
        else: # 相手又は中立の要塞の場合
            score -= pawn_number * 0.5  # 部隊数に比例してスコアを減算(係数は調整可能)

    return score


def compare_strategies(strategy_a, strategy_b, state, team):
    """
    現在の状態に基づいて2つの戦略を比較する関数

    引数:
        strategy_a (callable): 評価する最初の戦略関数
        strategy_b (callable): 評価する2番目の戦略関数
        state (list): ゲームの現在の状態
        team (int): プレイヤーのチームID
    返り値:
        str: より良い戦略の名前
    """
    score_a = evaluate_strategy(state, team) # strategy_aを評価(未実装)
    score_b = evaluate_strategy(state, team) # strategy_bを評価(未実装)

    if score_a > score_b:
        return "Strategy A is better"
    elif score_b > score_a:
        return "Strategy B is better"
    else:
        return "Both strategies are equal"