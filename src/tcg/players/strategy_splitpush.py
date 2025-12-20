from tcg.controller import Controller
from tcg.config import fortress_limit

class SplitPusher(Controller):
    """
    レーン分割プッシュ戦略:
    - 上中下のレーンを意識して中立→敵へ順次制圧。
    - 兵力が閾値を超えた要塞から隣接の最弱目標へ送軍。
    - 重要中枢(4,7)は適度にアップグレード。
    """
    def team_name(self) -> str:
        return "SplitPush"

    LANES = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [9, 10, 11],
    ]

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

        # 軽いアップグレード（4,7を優先）
        for hub in [4, 7]:
            if state[hub][0] == 1:
                level = state[hub][2]
                if level < 5 and state[hub][4] == -1:
                    limit = fortress_limit[level]
                    if state[hub][3] >= int(limit * 0.6):
                        return 2, hub, 0

        # レーンごとに中立→敵の順でプッシュ（十分な兵力があるときのみ）
        for lane in self.LANES:
            my_lane = [i for i in lane if state[i][0] == 1]
            if not my_lane:
                continue
            # 兵力の多い起点を選ぶ
            start = max(my_lane, key=lambda i: state[i][3])
            start_level = state[start][2]
            start_limit = fortress_limit[start_level]
            # 閾値: 中立は65%、敵は85%推奨。さらに送軍量（半分）が目標兵力を上回ること。
            neighbors = state[start][5]
            lane_neighbors = [n for n in neighbors if n in lane]
            # laneに候補がなければ通常隣接にフォールバック
            lane_neighbors = lane_neighbors if lane_neighbors else neighbors
            half_send = state[start][3] // 2
            # 到着時の削り量（kindに応じて）
            dmg = 0.95 if state[start][1] == 1 else 0.65
            neutral_targets = [n for n in lane_neighbors if state[n][0] == 0]
            enemy_targets = [n for n in lane_neighbors if state[n][0] == 2]
            ally_targets = [n for n in lane_neighbors if state[n][0] == 1]
            # 中立のうち、半分送って勝てるもの
            viable_neutrals = [n for n in neutral_targets if state[start][3] >= int(start_limit * 0.65) and (half_send * dmg) > state[n][3]]
            # 敵のうち、半分送っても兵力差で上回れるもの（+2マージン）
            viable_enemies = [n for n in enemy_targets if state[start][3] >= int(start_limit * 0.85) and (half_send * dmg) > (state[n][3] + 2)]
            target = None
            if viable_neutrals:
                target = min(viable_neutrals, key=lambda n: state[n][3])
            elif viable_enemies:
                target = min(viable_enemies, key=lambda n: state[n][3])
            elif ally_targets and state[start][3] >= int(start_limit * 0.9):
                # 前線強化は満杯近くのみ（ちまちま送らない）
                target = min(ally_targets, key=lambda n: state[n][3] / max(1, fortress_limit[state[n][2]]))
            if target is not None:
                return 1, start, target

        return 0, 0, 0
