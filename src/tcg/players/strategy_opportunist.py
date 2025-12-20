from tcg.controller import Controller
from tcg.config import fortress_limit

class Opportunist(Controller):
    """
    機会主義戦略:
    - 全自要塞の中から、最も攻めやすい隣接（中立/弱敵）への攻撃機会を常に探索。
    - ソースは兵力充足度が高い要塞を選択。
    """
    def team_name(self) -> str:
        return "Opportunist"

    def update(self, info):
        team, state, moving_pawns, spawning_pawns, done = info
        my_forts = [i for i in range(12) if state[i][0] == 1]
        if not my_forts:
            return 0, 0, 0

        # 1) 軽アップグレード（60%超）
        for i in my_forts:
            lvl = state[i][2]
            if lvl < 5 and state[i][4] == -1:
                limit = fortress_limit[lvl]
                if state[i][3] >= int(limit * 0.6):
                    return 2, i, 0

        # 2) グローバルに攻撃機会を探索
        best = None
        best_score = None
        for i in my_forts:
            limit = fortress_limit[state[i][2]]
            fill = state[i][3] / max(1, limit)
            if fill < 0.65:
                continue
            for n in state[i][5]:
                if state[n][0] == 0:
                    score = (fill, -state[n][3])
                elif state[n][0] == 2:
                    score = (fill, -state[n][3] - 1)  # 中立を少し優先
                else:
                    continue
                if best_score is None or score > best_score:
                    best_score = score
                    best = (i, n)
        if best is not None:
            return 1, best[0], best[1]

        # 3) 味方再配置（前線強化）
        for i in my_forts:
            limit = fortress_limit[state[i][2]]
            if state[i][3] >= int(limit * 0.75):
                allies = [n for n in state[i][5] if state[n][0] == 1]
                if allies:
                    front = [a for a in allies if any(state[m][0] == 2 for m in state[a][5])]
                    target_pool = front if front else allies
                    target = min(target_pool, key=lambda a: state[a][3] / max(1, fortress_limit[state[a][2]]))
                    return 1, i, target

        return 0, 0, 0