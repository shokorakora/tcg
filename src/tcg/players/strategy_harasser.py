from tcg.controller import Controller
from tcg.config import fortress_limit

class Harasser(Controller):
    """
    攪乱重視戦略:
    - 敵のアップグレード中要塞や弱い隣接敵へ小規模攻撃で妨害。
    - 安全な後方から前線へ再配置し圧力維持。
    - 機会があれば軽いアップグレード。
    """
    def team_name(self) -> str:
        return "Harasser"

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

        # 0) 早期中立制圧（待ちにならないよう初動で動く）
        for i in my_forts:
            lvl = state[i][2]
            limit = fortress_limit[lvl]
            neighbors = state[i][5]
            neutrals = [n for n in neighbors if state[n][0] == 0]
            if neutrals and state[i][3] >= int(limit * 0.65):
                half_send = state[i][3] // 2
                dmg = 0.95 if state[i][1] == 1 else 0.65
                # 半分送って削り量が目標兵力を上回る最弱中立へ
                viable = [n for n in neutrals if (half_send * dmg) > state[n][3]]
                if viable:
                    target = min(viable, key=lambda n: state[n][3])
                    return 1, i, target

        # 1) 軽アップグレード: 前線に隣接している自要塞を優先
        for i in my_forts:
            lvl = state[i][2]
            if lvl < 5 and state[i][4] == -1:
                limit = fortress_limit[lvl]
                # 60%超ならアップグレード着手
                if state[i][3] >= int(limit * 0.6):
                    enemy_neighbors = any(state[n][0] == 2 for n in state[i][5])
                    if enemy_neighbors:
                        return 2, i, 0

        # 2) ハラス対象: 隣接する敵のうちアップグレード中 or 兵力が低いもの
        for i in my_forts:
            neighbors = state[i][5]
            enemies = [n for n in neighbors if state[n][0] == 2]
            if not enemies:
                continue
            # 攻撃可能条件: 自分の兵力がレベル上限の70%以上、かつ半分送って上回れる
            limit = fortress_limit[state[i][2]]
            if state[i][3] >= int(limit * 0.7):
                # まずアップグレード中の敵
                upgrading = [n for n in enemies if state[n][4] != -1]
                weak = sorted(enemies, key=lambda n: state[n][3])
                target = None
                if upgrading:
                    # アップグレード中なら優先妨害
                    cand = min(upgrading, key=lambda n: state[n][3])
                    dmg = 0.95 if state[i][1] == 1 else 0.65
                    if (state[i][3] // 2) * dmg > (state[cand][3] + 2):
                        target = cand
                elif weak:
                    cand = weak[0]
                    dmg = 0.95 if state[i][1] == 1 else 0.65
                    if (state[i][3] // 2) * dmg > (state[cand][3] + 2):
                        target = cand
                if target is not None:
                    return 1, i, target

        # 3) 後方からの前線強化
        for i in my_forts:
            enemy_adj = any(state[n][0] == 2 for n in state[i][5])
            lvl = state[i][2]
            limit = fortress_limit[lvl]
            # 敵がいない安全後方で85%以上なら、前線味方へ再配置（ちまちま送らない）
            if not enemy_adj and state[i][3] >= int(limit * 0.85):
                allies = [n for n in state[i][5] if state[n][0] == 1]
                if allies:
                    # 前線（敵隣接）を優先
                    front_allies = [a for a in allies if any(state[m][0] == 2 for m in state[a][5])]
                    target = None
                    if front_allies:
                        target = min(front_allies, key=lambda a: state[a][3] / max(1, fortress_limit[state[a][2]]))
                    else:
                        target = min(allies, key=lambda a: state[a][3] / max(1, fortress_limit[state[a][2]]))
                    if target is not None:
                        return 1, i, target

        return 0, 0, 0
