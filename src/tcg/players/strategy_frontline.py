
import random
from tcg.controller import Controller
from tcg.config import fortress_limit

class FrontlineMaster(Controller):
    """
    前線維持戦略 (Frontline strategy):
    - 「前線（敵に隣接）」と「後方」を区別します。
    - 後方の要塞は前線に部隊を送り込みます。
    - 前線の要塞は攻撃または維持に集中します。
    """
    def team_name(self) -> str:
        return "Frontline"

    def update(self, info):
        team_id, state, moving_pawns, spawning_pawns, done = info
        
        my_fortresses = [i for i, s in enumerate(state) if s[0] == 1]
        
        # Identify Frontline vs Backline
        frontline = []
        backline = []
        
        for i in my_fortresses:
            neighbors = state[i][5]
            is_front = False
            for n in neighbors:
                if state[n][0] == 2: # Enemy
                    is_front = True
                    break
            if is_front:
                frontline.append(i)
            else:
                backline.append(i)
        
        # Backline Logic: Send to nearest Frontline
        # BFS to find distance to frontline could be good, but for now just send to neighbor closer to enemy?
        # Or simply: if neighbor is Frontline, send there. If neighbor is Backline, send to one that has path to Frontline?
        # Simplified: Send to any neighbor that is closer to enemy or is Frontline.
        
        # Let's process Backline first
        for i in backline:
            if state[i][3] < 5: continue
            
            neighbors = state[i][5]
            # Priority: Neighbor is Frontline > Neighbor is Neutral > Neighbor is Backline
            
            front_neighbors = [n for n in neighbors if n in frontline]
            neutral_neighbors = [n for n in neighbors if state[n][0] == 0]
            back_neighbors = [n for n in neighbors if n in backline]
            
            target = None
            if front_neighbors:
                # Send to the one needing most help (lowest troops)
                front_neighbors.sort(key=lambda x: state[x][3])
                target = front_neighbors[0]
            elif neutral_neighbors:
                # Expand if no frontline connection
                target = random.choice(neutral_neighbors)
            elif back_neighbors:
                # Send to random backline to circulate? Or try to find path?
                # Random for now to avoid getting stuck
                target = random.choice(back_neighbors)
            
            if target is not None:
                return 1, i, target
                
        # Frontline Logic: Attack or Upgrade
        for i in frontline:
            pawn_count = state[i][3]
            level = state[i][2]
            neighbors = state[i][5]
            
            # If very safe (lots of troops), attack weakest enemy
            if pawn_count > 20: # Arbitrary threshold
                enemies = [n for n in neighbors if state[n][0] == 2]
                if enemies:
                    enemies.sort(key=lambda x: state[x][3])
                    return 1, i, enemies[0]
            
            # If can upgrade and not under immediate heavy fire (heuristic), do it
            # Or maybe Frontline should prioritize troops over levels?
            # Let's say if we have A LOT of troops, upgrade.
            if level < 5 and pawn_count > fortress_limit[level] * 0.8:
                 if state[i][4] == -1:
                     return 2, i, 0
                     
        # Fallback: If we have neutrals nearby, take them
        for i in my_fortresses:
            if state[i][3] > 10:
                neighbors = state[i][5]
                neutrals = [n for n in neighbors if state[n][0] == 0]
                if neutrals:
                    return 1, i, neutrals[0]

        return 0, 0, 0
