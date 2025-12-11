from typing import List, Tuple, Dict
Action = Tuple[int, int, int]

class LearningPlayer:
    def __init__(self):
        pass

    def select_action(self, info) -> Action:
        # 学習は今は使わず、アップグレード優先の最小版
        team, state, moving_pawns, spawning_pawns, done = info
        from tcg.config import fortress_limit
        best = None
        for i, f in enumerate(state):
            ft_team, _, level, pawn_number, upgrade_time, _ = f
            if ft_team != 1 or level >= 5:
                continue
            # upgrade_time < 0 が実行可能
            if upgrade_time >= 0:
                continue
            need = max(1, fortress_limit[level] // 2)
            if pawn_number >= need:
                key = (level, -pawn_number, i)
                if best is None or key < best:
                    best = key
        if best:
            return (2, best[2], 0)
        return (0, 0, 0)

    def observe(self, prev_state, action: Action, reward: float, next_state):
        pass

    def _tick_cooldown(self):
        pass