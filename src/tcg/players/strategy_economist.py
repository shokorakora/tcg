
import random
from tcg.controller import Controller
from tcg.config import fortress_limit

class DefensiveEconomist(Controller):
    """
    経済重視戦略 (Economic strategy):
    - 要塞を最大レベルまでアップグレードすることを最優先します。
    - 要塞が満杯になったときのみ攻撃します。
    - 最大レベルになるまで部隊を貯め込んで防衛します。
    """
    def team_name(self) -> str:
        return "Economist"

    def update(self, info):
        team_id, state, moving_pawns, spawning_pawns, done = info
        
        my_fortresses = [i for i, s in enumerate(state) if s[0] == 1]
        random.shuffle(my_fortresses)
        
        for i in my_fortresses:
            level = state[i][2]
            pawn_count = state[i][3]
            limit = fortress_limit[level]
            upgrade_cost = limit // 2
            is_upgrading = state[i][4] != -1
            
            # 1. Try to upgrade if not max level and not currently upgrading
            if level < 5 and not is_upgrading:
                if pawn_count >= upgrade_cost:
                    return 2, i, 0
            
            # 2. If full (or close to full), attack/expand
            # We use a threshold slightly lower than limit to avoid wasting generation
            if pawn_count >= limit * 0.9:
                neighbors = state[i][5]
                
                # Prioritize attacking enemy > neutral > reinforcing own
                enemies = [n for n in neighbors if state[n][0] == 2]
                neutrals = [n for n in neighbors if state[n][0] == 0]
                allies = [n for n in neighbors if state[n][0] == 1]
                
                target = None
                if enemies:
                    # Attack strongest enemy to weaken them? Or weakest?
                    # Let's attack weakest to capture.
                    enemies.sort(key=lambda x: state[x][3])
                    target = enemies[0]
                elif neutrals:
                    neutrals.sort(key=lambda x: state[x][3])
                    target = neutrals[0]
                elif allies:
                    # Send to ally with lowest percentage of troops
                    allies.sort(key=lambda x: state[x][3] / fortress_limit[state[x][2]])
                    target = allies[0]
                
                if target is not None:
                    return 1, i, target

        return 0, 0, 0
