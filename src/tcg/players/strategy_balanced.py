
import random
from tcg.controller import Controller
from tcg.config import fortress_limit

class BalancedStrategist(Controller):
    """
    バランス型戦略 (Balanced strategy):
    - 各要塞の「危険度」と「好機」を評価します。
    - 安全であればアップグレードを行います。
    - 明確な有利があれば攻撃します。
    - 脅かされている要塞には増援を送ります。
    """
    def team_name(self) -> str:
        return "Balanced"

    def update(self, info):
        team_id, state, moving_pawns, spawning_pawns, done = info
        
        my_fortresses = [i for i, s in enumerate(state) if s[0] == 1]
        
        # Sort by ID to be deterministic or shuffle for variety. Let's shuffle.
        random.shuffle(my_fortresses)
        
        best_action = (0, 0, 0)
        best_score = -float('inf')
        
        for i in my_fortresses:
            level = state[i][2]
            pawn_count = state[i][3]
            limit = fortress_limit[level]
            neighbors = state[i][5]
            is_upgrading = state[i][4] != -1
            
            # Calculate local danger (sum of enemy troops in neighbors)
            enemy_troops = sum(state[n][3] for n in neighbors if state[n][0] == 2)
            
            # Action 1: Upgrade
            if level < 5 and not is_upgrading and pawn_count >= limit // 2:
                # Score based on safety and current level
                # Safer -> Higher score to upgrade
                # Lower level -> Higher priority to upgrade early
                safety_factor = 1.0 if enemy_troops == 0 else (pawn_count / enemy_troops)
                score = 10 + (5 - level) * 2 + safety_factor * 5
                
                if score > best_score:
                    best_score = score
                    best_action = (2, i, 0)
            
            # Action 2: Attack / Move
            if pawn_count >= 2:
                for n in neighbors:
                    target_team = state[n][0]
                    target_troops = state[n][3]
                    
                    score = 0
                    
                    if target_team != 1: # Enemy or Neutral
                        # Attack score
                        # High if we can win (our half > their troops)
                        # High if target is weak
                        
                        sending = pawn_count // 2
                        
                        # Simple combat simulation heuristic
                        # Damage depends on troop type but let's simplify
                        damage = sending * 0.8 # Average damage
                        
                        if damage > target_troops:
                            # Likely capture
                            score = 50 + (damage - target_troops)
                            if target_team == 2:
                                score += 20 # Priority to enemy over neutral
                        else:
                            # Harass
                            score = damage - target_troops # Negative if suicide
                            
                        # Don't leave ourselves empty if threatened
                        if enemy_troops > (pawn_count - sending):
                            score -= 50
                            
                    else: # Own team
                        # Reinforce
                        # Good if target is threatened or upgrading
                        target_limit = fortress_limit[state[n][2]]
                        target_is_full = target_troops >= target_limit
                        
                        if not target_is_full:
                            target_enemy_neighbors = sum(state[nn][3] for nn in state[n][5] if state[nn][0] == 2)
                            if target_enemy_neighbors > target_troops:
                                # Target is in danger, help it!
                                score = 40 + (target_enemy_neighbors - target_troops)
                            elif state[n][4] != -1:
                                # Target is upgrading, protect it? Or it doesn't need protection if safe?
                                # Actually upgrading consumes troops, so it might be low.
                                score = 10
                            else:
                                # Just balancing
                                score = 5
                        else:
                            score = -10 # Don't overfill
                            
                    if score > best_score:
                        best_score = score
                        best_action = (1, i, n)

        return best_action
