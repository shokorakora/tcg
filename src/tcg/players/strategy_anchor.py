from tcg.controller import Controller
from tcg.config import fortress_limit

class Anchor(Controller):
    """
    中枢堅守＋近接制圧戦略:
    - 4,7の中枢要塞を優先アップグレードし堅守。
    - 充足度の高い要塞から隣接の中立→敵→味方(前線強化)の順に送軍。
    """
    def team_name(self) -> str:
        return "Anchor"

    HUBS = [4, 7]

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

        # 1) 中枢アップグレード優先
        for hub in self.HUBS:
            if state[hub][0] == 1:
                lvl = state[hub][2]
                if lvl < 5 and state[hub][4] == -1:
                    limit = fortress_limit[lvl]
                    if state[hub][3] >= int(limit * 0.6):
                        return 2, hub, 0

        # 2) 充足度の高い要塞から近接制圧（十分な兵力でのみ）
        start_candidates = sorted(my_forts, key=lambda i: state[i][3] / max(1, fortress_limit[state[i][2]]), reverse=True)
        for start in start_candidates:
            limit = fortress_limit[state[start][2]]
            neighbors = state[start][5]
            neutrals = [n for n in neighbors if state[n][0] == 0]
            enemies = [n for n in neighbors if state[n][0] == 2]
            allies = [n for n in neighbors if state[n][0] == 1]
            half_send = state[start][3] // 2
            dmg = 0.95 if state[start][1] == 1 else 0.65
            # 中立は65%以上かつ半分で上回る
            viable_neutrals = [n for n in neutrals if state[start][3] >= int(limit * 0.65) and (half_send * dmg) > state[n][3]]
            # 敵は85%以上かつ半分で上回る（+2）
            viable_enemies = [n for n in enemies if state[start][3] >= int(limit * 0.85) and (half_send * dmg) > (state[n][3] + 2)]
            target = None
            if viable_neutrals:
                target = min(viable_neutrals, key=lambda n: state[n][3])
            elif viable_enemies:
                target = min(viable_enemies, key=lambda n: state[n][3])
            elif allies and state[start][3] >= int(limit * 0.9):
                # 満杯近くのみ前線強化（ちまちま送らない）
                target = min(allies, key=lambda a: state[a][3] / max(1, fortress_limit[state[a][2]]))
            if target is not None:
                return 1, start, target

        return 0, 0, 0