from typing import List, Tuple
from tcg.config import fortress_limit

def can_upgrade(state: List[List[int]], i: int) -> bool:
    team, _, level, pawn_number, upgrade_time, _ = state[i]
    if team != 1 or level >= 5:
        return False
    # この環境では upgrade_time < 0 が「待機中＝アップグレード可能」
    if upgrade_time >= 0:
        return False
    need = max(1, fortress_limit[level] // 2)
    return pawn_number >= need

def heuristic_strategy(info) -> Tuple[int, int, int]:
    team, state, moving_pawns, spawning_pawns, done = info
    best = None
    for i in range(len(state)):
        if can_upgrade(state, i):
            lvl = state[i][2]
            pawns = state[i][3]
            key = (lvl, -pawns, i)
            if best is None or key < best:
                best = key
    if best:
        return (2, best[2], 0)
    return (0, 0, 0)