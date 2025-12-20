from tcg.controller import Controller
from tcg.config import fortress_limit

class Rusher(Controller):
    """
    早期制圧重視戦略:
    - アップグレードは控えめ、兵力が溜まれば隣接の弱い目標へ即攻撃。
    - 中立優先でマップ支配を広げ、次いで敵を叩く。
    """
    def team_name(self) -> str:
        return "Rusher"

    def update(self, info):
        team, state, moving_pawns, spawning_pawns, done = info
        my_forts = [i for i in range(12) if state[i][0] == 1]
        if not my_forts:
            return 0, 0, 0

        # 1) 軽いアップグレード（50%超）
        for i in my_forts:
            lvl = state[i][2]
            if lvl < 5 and state[i][4] == -1:
                limit = fortress_limit[lvl]
                if state[i][3] >= int(limit * 0.5):
                    return 2, i, 0

        # 2) 攻撃優先（60%以上）: 中立→敵→味方の順で最弱へ
        for i in my_forts:
            limit = fortress_limit[state[i][2]]
            if state[i][3] >= int(limit * 0.6):
                neighbors = state[i][5]
                neutrals = [n for n in neighbors if state[n][0] == 0]
                enemies = [n for n in neighbors if state[n][0] == 2]
                allies = [n for n in neighbors if state[n][0] == 1]
                target = None
                if neutrals:
                    target = min(neutrals, key=lambda n: state[n][3])
                elif enemies:
                    target = min(enemies, key=lambda n: state[n][3])
                elif allies:
                    target = min(allies, key=lambda a: state[a][3] / max(1, fortress_limit[state[a][2]]))
                if target is not None:
                    return 1, i, target

        return 0, 0, 0