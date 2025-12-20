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

        # 軽いアップグレード（4,7を優先）
        for hub in [4, 7]:
            if state[hub][0] == 1:
                level = state[hub][2]
                if level < 5 and state[hub][4] == -1:
                    limit = fortress_limit[level]
                    if state[hub][3] >= int(limit * 0.6):
                        return 2, hub, 0

        # レーンごとに中立→敵の順でプッシュ
        for lane in self.LANES:
            my_lane = [i for i in lane if state[i][0] == 1]
            if not my_lane:
                continue
            # 兵力の多い起点を選ぶ
            start = max(my_lane, key=lambda i: state[i][3])
            start_level = state[start][2]
            start_limit = fortress_limit[start_level]
            # 閾値: 70%以上で攻める
            if state[start][3] >= int(start_limit * 0.7):
                neighbors = state[start][5]
                # lane内優先
                lane_neighbors = [n for n in neighbors if n in lane]
                # 中立→敵→味方の順でターゲットを選ぶ（最弱優先）
                neutral_targets = [n for n in lane_neighbors if state[n][0] == 0]
                enemy_targets = [n for n in lane_neighbors if state[n][0] == 2]
                ally_targets = [n for n in lane_neighbors if state[n][0] == 1]
                target = None
                if neutral_targets:
                    target = min(neutral_targets, key=lambda n: state[n][3])
                elif enemy_targets:
                    target = min(enemy_targets, key=lambda n: state[n][3])
                elif ally_targets:
                    # 前線強化: 兵力比が低い味方へ再配置
                    target = min(ally_targets, key=lambda n: state[n][3] / max(1, fortress_limit[state[n][2]]))
                if target is not None:
                    return 1, start, target

        return 0, 0, 0
