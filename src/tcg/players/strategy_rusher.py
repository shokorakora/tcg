
import random
from tcg.controller import Controller
from tcg.config import fortress_limit

class AggressiveRusher(Controller):
    """
    攻撃的戦略 (Aggressive strategy):
    - 常に最も弱い敵または中立の隣接要塞を攻撃します。
    - アップグレードよりも領土拡大を優先します。
    """
    def team_name(self) -> str:
        return "Rusher"

    def update(self, info):
        # info: [team_id, state, moving_pawns, spawning_pawns, done]
        team_id, state, moving_pawns, spawning_pawns, done = info
        
        my_fortresses = [i for i, s in enumerate(state) if s[0] == 1]
        
        # Shuffle to avoid deterministic loops
        random.shuffle(my_fortresses)
        
        for i in my_fortresses:
            # state[i]: [team, kind, level, pawn_number, upgrade_time, neighbors]
            pawn_count = state[i][3]
            neighbors = state[i][5]
            
            # If we have enough troops to attack (at least 2 to send 1)
            if pawn_count >= 2:
                # Find targets: Enemy or Neutral
                targets = []
                for n in neighbors:
                    # state[n][0] is team of neighbor
                    if state[n][0] != 1:
                        targets.append(n)
                
                if targets:
                    # Attack the one with fewest troops
                    targets.sort(key=lambda x: state[x][3])
                    target = targets[0]
                    return 1, i, target
                
                # If all neighbors are mine, send to the one with fewest troops (reinforce)
                # or just random to keep flow moving
                else:
                    # Filter neighbors that are not full
                    valid_neighbors = [n for n in neighbors if state[n][3] < fortress_limit[state[n][2]]]
                    if valid_neighbors:
                        target = random.choice(valid_neighbors)
                        return 1, i, target

        return 0, 0, 0
