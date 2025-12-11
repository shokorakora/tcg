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

        # 自軍のアップグレード候補を収集（upgrade_time < 0 が「待機中で実行可」）
        candidates = []
        for i, f in enumerate(state):
            ft_team, _, level, pawn_number, upgrade_time, _ = f
            if ft_team != 1:
                continue
            if level >= 5:
                continue
            if upgrade_time >= 0:  # 実行中 or 実行不可とみなす
                continue
            need = max(1, fortress_limit[level] // 2)
            if pawn_number >= need:
                candidates.append((level, -pawn_number, i))  # 低レベル・兵多い優先

        if self.step <= 10:
            print(f"[Step {self.step}] candidates={candidates}")

        if candidates:
            candidates.sort()
            _, _, subj = candidates[0]
            return (2, subj, 0)

        # アップグレード候補がないターンは待機（兵を貯める）
        return (0, 0, 0)