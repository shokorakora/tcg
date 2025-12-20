from tcg.controller import Controller
from tcg.config import fortress_limit

class Counter(Controller):
    """
    反撃重視戦略:
    - 多数の自要塞に隣接する敵やアップグレード中の敵を優先して叩く。
    - 前線付近の自要塞は適度にアップグレード。
    """
    def team_name(self) -> str:
        return "Counter"

    def update(self, info):
        team, state, moving_pawns, spawning_pawns, done = info
        my_forts = [i for i in range(12) if state[i][0] == 1]
        if not my_forts:
            return 0, 0, 0

        # 0) 初期ブートストラップ: 自拠点が少ない序盤は自要塞をLv4まで優先アップグレード
        if len(my_forts) <= 2:
            for i in my_forts:
                lvl = state[i][2]
                if lvl < 4 and state[i][4] == -1:
                    limit = fortress_limit[lvl]
                    if state[i][3] >= limit // 2:
                        return 2, i, 0

        # 1) 初動の中立制圧（待ちにならないようにする）
        for i in my_forts:
            lvl = state[i][2]
            limit = fortress_limit[lvl]
            if state[i][3] >= int(limit * 0.65):
                neutrals = [n for n in state[i][5] if state[n][0] == 0]
                if neutrals:
                    half_send = state[i][3] // 2
                    dmg = 0.95 if state[i][1] == 1 else 0.65
                    viable = [n for n in neutrals if (half_send * dmg) > state[n][3]]
                    if viable:
                        target = min(viable, key=lambda n: state[n][3])
                        return 1, i, target

        # 2) 前線付近のアップグレード（敵隣接あり＆60%以上）
        for i in my_forts:
            lvl = state[i][2]
            limit = fortress_limit[lvl]
            enemy_adj = any(state[n][0] == 2 for n in state[i][5])
            if enemy_adj and lvl < 5 and state[i][4] == -1 and state[i][3] >= int(limit * 0.6):
                return 2, i, 0

        # 3) 優先敵を特定: 自要塞に隣接する敵の「隣接自要塞数」が多いほど優先
        enemy_score = {}
        for i in my_forts:
            for n in state[i][5]:
                if state[n][0] == 2:
                    enemy_score[n] = enemy_score.get(n, 0) + 1
        # 先にアップグレード中の敵を強く優先
        for e in list(enemy_score.keys()):
            if state[e][4] != -1:
                enemy_score[e] += 2

        # 4) 攻撃実行: 充足度が高い自要塞から優先敵へ
        for i in sorted(my_forts, key=lambda k: state[k][3] / max(1, fortress_limit[state[k][2]]), reverse=True):
            limit = fortress_limit[state[i][2]]
            half_send = state[i][3] // 2
            dmg = 0.95 if state[i][1] == 1 else 0.65
            if state[i][3] < int(limit * 0.75):
                continue
            candidates = [n for n in state[i][5] if state[n][0] == 2]
            if not candidates:
                continue
            # スコア＋弱さで選択
            ranked = sorted(candidates, key=lambda n: (enemy_score.get(n, 0), -state[n][3]), reverse=True)
            for cand in ranked:
                if (half_send * dmg) > (state[cand][3] + 2):
                    return 1, i, cand

        # 5) 前線強化: 安全後方から前線へ再配置（トリクル防止のため高充足時のみ）
        for i in my_forts:
            limit = fortress_limit[state[i][2]]
            enemy_adj = any(state[n][0] == 2 for n in state[i][5])
            if not enemy_adj and state[i][3] >= int(limit * 0.9):
                allies = [n for n in state[i][5] if state[n][0] == 1]
                if allies:
                    front = [a for a in allies if any(state[m][0] == 2 for m in state[a][5])]
                    target_pool = front if front else allies
                    target = min(target_pool, key=lambda a: state[a][3] / max(1, fortress_limit[state[a][2]]))
                    return 1, i, target

        return 0, 0, 0