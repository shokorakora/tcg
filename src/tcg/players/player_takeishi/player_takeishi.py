from tcg.controller import Controller
from tcg.config import fortress_limit

class TakeishiPlayer(Controller):
    def __init__(self) -> None:
        super().__init__()
        self.step = 0

    def team_name(self) -> str:
        return "TakeishiAI"

    def update(self, info) -> tuple[int, int, int]:
        self.step += 1
        team, state, moving_pawns, spawning_pawns, done = info

        # 自軍拠点を取得（このマップは自軍が1拠点のみのことが多い）
        my_forts = [i for i, f in enumerate(state) if f[0] == 1]
        if not my_forts:
            return (0, 0, 0)
        i = my_forts[0]
        _, _, level, pawns, upg_time, neighbors = state[i]

        # 1) アップグレードフェーズ：upgrade_time < 0 なら連続でLv5まで上げる
        if level < 5 and upg_time < 0:
            need = max(1, fortress_limit[level] // 3)  # 1/3に緩和
            if pawns >= need:
                return (2, i, 0)

        # 2) 実行中は待機（完了まで約 upg_time ターン）
        if level < 5 and upg_time >= 0:
            return (0, 0, 0)

        # 3) Lv5達成後の拡大：最も弱い中立へ送兵（最低8兵送れるとき）
        if level >= 5 and pawns // 2 >= 8:
            neutral = [n for n in neighbors if state[n][0] == 0]
            if neutral:
                target = min(neutral, key=lambda n: (state[n][3], state[n][2]))
                return (1, i, target)

        # 4) それ以外は兵を貯める
        return (0, 0, 0)