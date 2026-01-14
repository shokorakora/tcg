from typing import Optional

from tcg.controller import Controller
from tcg.config import fortress_limit


class ShotaPlayer(Controller):
    def team_name(self) -> str:
        return "Shota"

    def __init__(self) -> None:
        super().__init__()
        self.step = 0
        self._last_enemy_center_team: Optional[int] = None
        self._force_feed_enemy_center = False
        self._team: Optional[int] = None

    # Helpers
    def own(self, state, i: int) -> bool:
        return 0 <= i < 12 and self._team is not None and state[i][0] == self._team

    def enemy(self, state, i: int) -> bool:
        return 0 <= i < 12 and self._team is not None and state[i][0] != 0 and state[i][0] != self._team

    def neutral(self, state, i: int) -> bool:
        return 0 <= i < 12 and state[i][0] == 0

    @staticmethod
    def can_upgrade(state, i: int) -> bool:
        lvl = state[i][2]
        return 1 <= lvl <= 4 and state[i][4] == -1 and state[i][3] >= fortress_limit[lvl] // 2

    @staticmethod
    def can_send(state, i: int) -> bool:
        return state[i][3] >= 2

    @staticmethod
    def neighbors(state, i: int) -> list[int]:
        return state[i][5]

    def choose_mapping(self, state):
        # Returns (A,B,C,Center, enemy_center, enemy_A, flanks, base_extremes, enemy_base_set)
        if self.own(state, 1):
            # Top perspective
            A, B, C, Center = 1, 0, 2, 4
            enemy_center = 7
            enemy_A = 10
            flanks = [6, 8]
            base_extremes = [9, 11]
            enemy_base = {9, 10, 11}
        else:
            # Bottom perspective
            A, B, C, Center = 10, 11, 9, 7
            enemy_center = 4
            enemy_A = 1
            flanks = [3, 5]
            base_extremes = [0, 2]
            enemy_base = {0, 1, 2}
        return A, B, C, Center, enemy_center, enemy_A, flanks, base_extremes, enemy_base

    def update(self, info) -> tuple[int, int, int]:
        team, state, moving_pawns, spawning_pawns, done = info
        self._team = team
        self.step += 1

        A, B, C, Center, enemy_center, enemy_A, flanks, base_extremes, enemy_base = self.choose_mapping(state)

        # Track enemy_center capture to start continuous Center->enemy_center streaming
        ec_team = state[enemy_center][0]
        if self._last_enemy_center_team is None:
            self._last_enemy_center_team = ec_team
        else:
            if self._last_enemy_center_team in (0, 2) and ec_team == 1:
                self._force_feed_enemy_center = True
            self._last_enemy_center_team = ec_team

        # Early-phase progression: ensure A upgrades then pushes to B when gated conditions are met
        # Phase 1: A to Lv5 asap
        if self.own(state, A):
            lvlA = state[A][2]
            if lvlA < 5 and self.can_upgrade(state, A):
                return 2, A, 0
            if lvlA < 5:
                if self.neutral(state, B) and state[A][3] >= int(fortress_limit[lvlA] * 0.9) and self.can_send(state, A):
                    return 1, A, B
                # Do nothing else until A reaches Lv5
                return 0, 0, 0

        # Phase 2: Take/upgrade B; after A reaches Lv5, gate A->B by threshold
        if self.own(state, A):
            lvlA = state[A][2]
            if not self.own(state, B):
                if lvlA >= 5:
                    limitA = fortress_limit[lvlA]
                    if state[A][3] >= int(limitA * 0.7) and self.can_send(state, A):
                        return 1, A, B
                # If gate not met, allow other high-priority logic (like defense) to proceed
            elif state[B][2] < 5:
                if self.can_upgrade(state, B):
                    return 2, B, 0
                if self.can_send(state, A):
                    return 1, A, B

        # High-priority defense: specific routing when 3(8) or 5(6) are targeted
        center_neighbors = self.neighbors(state, Center)
        attacked: dict[int, int] = {}
        for pawn in moving_pawns:
            p_team, _, _, to, _ = pawn
            if p_team != 0 and p_team != self._team and to in center_neighbors:
                attacked[to] = attacked.get(to, 0) + 1
        if attacked:
            is_top = self.own(state, 1)
            def_left = 3 if is_top else 8
            def_right = 5 if is_top else 6
            # Only override for specified neighbors (3/8 and 5/6)
            if attacked.get(def_left, 0) > 0:
                if def_left in self.neighbors(state, B) and self.can_send(state, B):
                    return 1, B, def_left
                if self.can_send(state, Center):
                    return 1, Center, def_left
                for src in (A, B):
                    if Center in self.neighbors(state, src) and self.can_send(state, src):
                        return 1, src, Center
            if attacked.get(def_right, 0) > 0:
                if def_right in self.neighbors(state, C) and self.can_send(state, C):
                    return 1, C, def_right
                if self.can_send(state, Center):
                    return 1, Center, def_right
                for src in (A, C):
                    if Center in self.neighbors(state, src) and self.can_send(state, src):
                        return 1, src, Center

        # Phase 4 readiness
        c_ready = self.own(state, C) and state[C][2] >= 5 and self.own(state, A) and self.own(state, B)
        if c_ready:
            # Center not owned: only supply ABC -> Center
            if not self.own(state, Center):
                for src in (A, B, C):
                    if Center in self.neighbors(state, src) and self.can_send(state, src):
                        return 1, src, Center
                return 0, 0, 0

            # Center owned but < Lv5: upgrade and supply; allow force-feed to enemy_center
            if state[Center][2] < 5:
                if self._force_feed_enemy_center and self.own(state, enemy_center) and self.can_send(state, Center):
                    return 1, Center, enemy_center
                if self.can_upgrade(state, Center):
                    return 2, Center, 0
                for src in (A, B, C):
                    if Center in self.neighbors(state, src) and self.can_send(state, src):
                        return 1, src, Center
                return 0, 0, 0

            # Center is Lv5 -> split into cases based on Center-adjacent enemy presence
            c_nei = self.neighbors(state, Center)
            c_adj_enemies = [n for n in c_nei if self.enemy(state, n)]

            if not c_adj_enemies:
                # Case ①: No enemy adjacent to Center -> wait until 110% then push Center->enemy_center
                center_limit = fortress_limit[state[Center][2]]
                center_ok_110 = state[Center][3] >= int(center_limit * 0.6)
                if not self.own(state, enemy_center):
                    if self.can_send(state, Center) and center_ok_110:
                        return 1, Center, enemy_center
                else:
                    # enemy_center captured: stream via 7(4) -> Center or attack its adjacent enemies
                    if self.can_send(state, enemy_center):
                        ec_nei = self.neighbors(state, enemy_center)
                        ec_adj_enemies = [n for n in ec_nei if self.enemy(state, n)]
                        if ec_adj_enemies:
                            ec_target = min(ec_adj_enemies, key=lambda i: state[i][3])
                            return 1, enemy_center, ec_target
                        # If no adjacent enemies for 7(4), feed back to Center to reinforce
                        if Center in ec_nei:
                            return 1, enemy_center, Center
                # Continue ABC -> Center supply when not sending
                for src in (A, B, C):
                    if Center in self.neighbors(state, src) and self.can_send(state, src):
                        return 1, src, Center
                return 0, 0, 0
            else:
                # Case ②: Enemy holds 6/8 (or 3/5) -> push Center->flank at 80%
                center_limit = fortress_limit[state[Center][2]]
                center_ok_80 = state[Center][3] >= int(center_limit * 0.8)
                flank_enemies = [n for n in c_adj_enemies if n in flanks]
                if flank_enemies and self.can_send(state, Center) and center_ok_80:
                    target_flank = min(flank_enemies, key=lambda i: state[i][3])
                    return 1, Center, target_flank
                # After flanks captured (or if not present), attack any Center-adjacent enemies
                if c_adj_enemies and self.can_send(state, Center) and center_ok_80:
                    target_adj = min(c_adj_enemies, key=lambda i: state[i][3])
                    return 1, Center, target_adj
                # If none adjacent remain, use 7(4) to bridge: attack 7-adjacent enemies or feed to Center
                if self.own(state, enemy_center) and self.can_send(state, enemy_center):
                    ec_nei = self.neighbors(state, enemy_center)
                    ec_adj_enemies = [n for n in ec_nei if self.enemy(state, n)]
                    if ec_adj_enemies:
                        ec_target = min(ec_adj_enemies, key=lambda i: state[i][3])
                        return 1, enemy_center, ec_target
                    if Center in ec_nei:
                        return 1, enemy_center, Center
                # Continue ABC -> Center supply when not sending
                for src in (A, B, C):
                    if Center in self.neighbors(state, src) and self.can_send(state, src):
                        return 1, src, Center
                return 0, 0, 0

        # Phase 1: A to Lv5 asap
        if self.own(state, A):
            lvlA = state[A][2]
            if lvlA < 5 and self.can_upgrade(state, A):
                return 2, A, 0
            if lvlA < 5:
                if self.neutral(state, B) and state[A][3] >= int(fortress_limit[lvlA] * 0.9) and self.can_send(state, A):
                    return 1, A, B
                return 0, 0, 0

        # Phase 2: Take B first
        if self.own(state, A):
            lvlA = state[A][2]
            if not self.own(state, B):
                if lvlA >= 5:
                    limitA = fortress_limit[lvlA]
                    if state[A][3] >= int(limitA * 0.7) and self.can_send(state, A):
                        return 1, A, B
                return 0, 0, 0
            if state[B][2] < 5:
                if self.can_upgrade(state, B):
                    return 2, B, 0
                if self.can_send(state, A):
                    return 1, A, B

        # Phase 3: After B Lv5, continuously stream B->A and A->C; upgrade C during this period
        if self.own(state, B) and state[B][2] >= 5:
            # Prefer B->A whenever possible
            if A in self.neighbors(state, B) and self.can_send(state, B):
                return 1, B, A
            # Then push A->C to capture/upgrade C
            if C in self.neighbors(state, A) and self.can_send(state, A):
                return 1, A, C
            # If C is owned and upgradeable, upgrade it while continuing the pipeline
            if self.own(state, C) and state[C][2] < 5 and self.can_upgrade(state, C):
                return 2, C, 0

        # Fallback: do nothing
        return 0, 0, 0
