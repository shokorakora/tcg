from tcg.controller import Controller
from tcg.config import fortress_limit

class Feeder(Controller):
    """
    後方補給線戦略:
    - 敵隣接のない安全な後方から前線味方へ継続的に兵力供給。
    - 余力があれば後方もアップグレードして補給力を強化。
    """
    def team_name(self) -> str:
        return "Feeder"

    def update(self, info):
        team, state, moving_pawns, spawning_pawns, done = info
        my_forts = [i for i in range(12) if state[i][0] == 1]
        if not my_forts:
            return 0, 0, 0

        # 1) 後方のアップグレード（敵隣接なし＆60%以上）
        for i in my_forts:
            lvl = state[i][2]
            limit = fortress_limit[lvl]
            enemy_adj = any(state[n][0] == 2 for n in state[i][5])
            if not enemy_adj and lvl < 5 and state[i][4] == -1 and state[i][3] >= int(limit * 0.6):
                return 2, i, 0

        # 2) 後方から前線への補給（70%以上）
        for i in my_forts:
            lvl = state[i][2]
            limit = fortress_limit[lvl]
            enemy_adj = any(state[n][0] == 2 for n in state[i][5])
            if not enemy_adj and state[i][3] >= int(limit * 0.7):
                allies = [n for n in state[i][5] if state[n][0] == 1]
                if allies:
                    # 前線（敵隣接）を優先し、兵力比の低い味方へ供給
                    front_allies = [a for a in allies if any(state[m][0] == 2 for m in state[a][5])]
                    target_pool = front_allies if front_allies else allies
                    target = min(target_pool, key=lambda a: state[a][3] / max(1, fortress_limit[state[a][2]]))
                    return 1, i, target

        # 3) 余力攻撃（90%以上）: 敵→中立の順
        for i in my_forts:
            limit = fortress_limit[state[i][2]]
            if state[i][3] >= int(limit * 0.9):
                neighbors = state[i][5]
                enemies = [n for n in neighbors if state[n][0] == 2]
                neutrals = [n for n in neighbors if state[n][0] == 0]
                target = None
                if enemies:
                    target = min(enemies, key=lambda n: state[n][3])
                elif neutrals:
                    target = min(neutrals, key=lambda n: state[n][3])
                if target is not None:
                    return 1, i, target

        return 0, 0, 0