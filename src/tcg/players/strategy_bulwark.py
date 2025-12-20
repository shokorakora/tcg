from tcg.controller import Controller
from tcg.config import fortress_limit

class Bulwark(Controller):
    """
    要塞堅守戦略:
    - アップグレード最優先で兵力蓄積、前線の味方へ強化。
    - 攻撃は満杯近くのときのみ行い、確実な制圧を狙う。
    """
    def team_name(self) -> str:
        return "Bulwark"

    def update(self, info):
        team, state, moving_pawns, spawning_pawns, done = info
        my_forts = [i for i in range(12) if state[i][0] == 1]
        if not my_forts:
            return 0, 0, 0

        # 1) アップグレード最優先
        for i in my_forts:
            lvl = state[i][2]
            if lvl < 5 and state[i][4] == -1:
                limit = fortress_limit[lvl]
                cost = limit // 2
                if state[i][3] >= cost:
                    return 2, i, 0

        # 2) 後方から前線へ強化（70%以上）
        for i in my_forts:
            lvl = state[i][2]
            limit = fortress_limit[lvl]
            enemy_adj = any(state[n][0] == 2 for n in state[i][5])
            if not enemy_adj and state[i][3] >= int(limit * 0.7):
                allies = [n for n in state[i][5] if state[n][0] == 1]
                if allies:
                    # 敵隣接の味方を優先、次に兵力比が低い味方
                    front = [a for a in allies if any(state[m][0] == 2 for m in state[a][5])]
                    target_pool = front if front else allies
                    target = min(target_pool, key=lambda a: state[a][3] / max(1, fortress_limit[state[a][2]]))
                    return 1, i, target

        # 3) 満杯近くで攻撃（敵→中立→味方の順）
        for i in my_forts:
            lvl = state[i][2]
            limit = fortress_limit[lvl]
            if state[i][3] >= int(limit * 0.9):
                neighbors = state[i][5]
                enemies = [n for n in neighbors if state[n][0] == 2]
                neutrals = [n for n in neighbors if state[n][0] == 0]
                allies = [n for n in neighbors if state[n][0] == 1]
                target = None
                if enemies:
                    target = min(enemies, key=lambda n: state[n][3])
                elif neutrals:
                    target = min(neutrals, key=lambda n: state[n][3])
                elif allies:
                    # 兵力比が低い味方へ
                    target = min(allies, key=lambda a: state[a][3] / max(1, fortress_limit[state[a][2]]))
                if target is not None:
                    return 1, i, target

        return 0, 0, 0
