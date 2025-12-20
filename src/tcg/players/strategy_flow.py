from tcg.controller import Controller
from tcg.config import fortress_limit

class Flow(Controller):
    """
    兵力フロー維持戦略:
    - 充足度の高い自要塞から充足度の低い味方へ兵力を流し前線の厚みを維持。
    - 極端に満杯なら敵/中立へ圧力をかける。
    """
    def team_name(self) -> str:
        return "Flow"

    def update(self, info):
        team, state, moving_pawns, spawning_pawns, done = info
        my_forts = [i for i in range(12) if state[i][0] == 1]
        if not my_forts:
            return 0, 0, 0

        # 1) フロー再配置: 高充足→低充足の味方へ
        for i in sorted(my_forts, key=lambda k: state[k][3] / max(1, fortress_limit[state[k][2]]), reverse=True):
            limit_i = fortress_limit[state[i][2]]
            fill_i = state[i][3] / max(1, limit_i)
            if fill_i >= 0.7:
                allies = [n for n in state[i][5] if state[n][0] == 1]
                if allies:
                    target = min(allies, key=lambda a: state[a][3] / max(1, fortress_limit[state[a][2]]))
                    return 1, i, target

        # 2) 圧力攻撃（90%以上）
        for i in my_forts:
            limit = fortress_limit[state[i][2]]
            if state[i][3] >= int(limit * 0.9):
                neighbors = state[i][5]
                # 敵→中立の順で最弱へ
                enemies = [n for n in neighbors if state[n][0] == 2]
                neutrals = [n for n in neighbors if state[n][0] == 0]
                target = None
                if enemies:
                    target = min(enemies, key=lambda n: state[n][3])
                elif neutrals:
                    target = min(neutrals, key=lambda n: state[n][3])
                if target is not None:
                    return 1, i, target

        # 3) 軽アップグレード（安全＆60%以上）
        for i in my_forts:
            lvl = state[i][2]
            limit = fortress_limit[lvl]
            enemy_adj = any(state[n][0] == 2 for n in state[i][5])
            if not enemy_adj and lvl < 5 and state[i][4] == -1 and state[i][3] >= int(limit * 0.6):
                return 2, i, 0

        return 0, 0, 0