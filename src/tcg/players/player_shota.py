from tcg.controller import Controller
from tcg.config import fortress_limit


class ShotaPlayer(Controller):
    """
    Deterministic player enforcing early Lv5 upgrades and continuous streaming.

    Strategy outline (perspective-independent via index mapping):
    - Choose base triangle (A,B,C) and central (Center) based on which side we're on.
      If we own 1, use (A=1, B=0, C=2, Center=4); else use (A=10, B=11, C=9, Center=7).
    - Phase 1: Upgrade A to Lv5 ASAP (no sending from A until Lv5).
    - Phase 2: Stream A -> B continuously; upgrade B to Lv5.
    - Phase 3: Stream A -> C and B -> A; upgrade C to Lv5.
    - Phase 4: Stream A,B,C -> Center continuously; keep Center at Lv1.
    - Phase 5: From Center, continuously attack the opponent's frontline.
      Prefer attacking enemy Center (7 if Center=4, else 4).
      Special case: if enemy still holds any of base triangle (their 9,10,11 or 0,1,2), attack enemy Center instead of those base forts.
      Once captured, keep streaming from Center to that fort.
    """

    def team_name(self) -> str:
        return "Shota"

    def __init__(self) -> None:
        super().__init__()
        self.step = 0

    # --- Helpers ---
    @staticmethod
    def own(state, i: int) -> bool:
        return 0 <= i < 12 and state[i][0] == 1

    @staticmethod
    def enemy(state, i: int) -> bool:
        return 0 <= i < 12 and state[i][0] == 2

    @staticmethod
    def neutral(state, i: int) -> bool:
        return 0 <= i < 12 and state[i][0] == 0

    @staticmethod
    def can_upgrade(state, i: int) -> bool:
        lvl = state[i][2]
        if not (1 <= lvl <= 4):
            return False
        return state[i][4] == -1 and state[i][3] >= fortress_limit[lvl] // 2

    @staticmethod
    def can_send(state, i: int) -> bool:
        return state[i][3] >= 2

    @staticmethod
    def neighbors(state, i: int) -> list[int]:
        return state[i][5]

    def choose_mapping(self, state):
        """Decide indices for A,B,C,Center and enemy base set by perspective.
        If we own 1, we are 'top' perspective; otherwise use bottom mapping.
        """
        if self.own(state, 1):
            A, B, C, Center = 1, 0, 2, 4
            enemy_base = {9, 10, 11}
            enemy_center = 7
        else:
            A, B, C, Center = 10, 11, 9, 7
            enemy_base = {0, 1, 2}
            enemy_center = 4
        return A, B, C, Center, enemy_base, enemy_center

    def update(self, info) -> tuple[int, int, int]:
        team, state, moving_pawns, spawning_pawns, done = info
        self.step += 1

        A, B, C, Center, enemy_base, enemy_center = self.choose_mapping(state)

        # Phase 4 (priority when ready): Once C is owned and Lv5, stream A/B/C -> Center,
        # and alternate with Center/bridge attacks to advance the frontline.
        c_ready = self.own(state, C) and state[C][2] >= 5 and self.own(state, A) and self.own(state, B)
        if c_ready:
            # If Center is not owned yet: only supply ABC -> Center (no sends from Center)
            if not self.own(state, Center):
                if Center in self.neighbors(state, A) and self.can_send(state, A):
                    return 1, A, Center
                if Center in self.neighbors(state, B) and self.can_send(state, B):
                    return 1, B, Center
                if Center in self.neighbors(state, C) and self.can_send(state, C):
                    return 1, C, Center
                return 0, 0, 0

            # If Center is owned but below Lv5: prioritize upgrading and only supply ABC -> Center
            if state[Center][2] < 5:
                if self.can_upgrade(state, Center):
                    return 2, Center, 0
                if Center in self.neighbors(state, A) and self.can_send(state, A):
                    return 1, A, Center
                if Center in self.neighbors(state, B) and self.can_send(state, B):
                    return 1, B, Center
                if Center in self.neighbors(state, C) and self.can_send(state, C):
                    return 1, C, Center
                return 0, 0, 0

            # Center is Lv5: alternate supply and attack/bridge
            if self.step % 2 == 0:
                # Supply: A/B/C -> Center
                if Center in self.neighbors(state, A) and self.can_send(state, A):
                    return 1, A, Center
                if Center in self.neighbors(state, B) and self.can_send(state, B):
                    return 1, B, Center
                if Center in self.neighbors(state, C) and self.can_send(state, C):
                    return 1, C, Center
            else:
                # Attack/Bridge from Center or enemy_center
                c_neighbors = self.neighbors(state, Center)
                adj_enemies = [n for n in c_neighbors if self.enemy(state, n)]
                # Gate attacks: require Center pawns >= 80% of capacity
                center_limit = fortress_limit[state[Center][2]]
                center_ok = state[Center][3] >= int(center_limit * 0.8)
                if adj_enemies and self.can_send(state, Center) and center_ok:
                    target = min(adj_enemies, key=lambda i: state[i][3])
                    return 1, Center, target
                # No adjacent enemies: push to enemy_center
                if not self.own(state, enemy_center):
                    if self.can_send(state, Center) and center_ok:
                        return 1, Center, enemy_center
                else:
                    # enemy_center is ours: attack from there and keep feeding it
                    ec_neighbors = self.neighbors(state, enemy_center)
                    ec_enemies = [n for n in ec_neighbors if self.enemy(state, n)]
                    # Gate enemy_center attacks similarly
                    ec_limit = fortress_limit[state[enemy_center][2]]
                    ec_ok = state[enemy_center][3] >= int(ec_limit * 0.7)
                    if ec_enemies and self.can_send(state, enemy_center) and ec_ok:
                        ec_target = min(ec_enemies, key=lambda i: state[i][3])
                        return 1, enemy_center, ec_target
                    if self.can_send(state, Center) and center_ok:
                        return 1, Center, enemy_center
            # Fallback supply
            if Center in self.neighbors(state, A) and self.can_send(state, A):
                return 1, A, Center
            if Center in self.neighbors(state, B) and self.can_send(state, B):
                return 1, B, Center
            if Center in self.neighbors(state, C) and self.can_send(state, C):
                return 1, C, Center
            return 0, 0, 0

        # Phase 1: Upgrade A to Lv5 ASAP (no send from A until Lv5)
        if self.own(state, A):
            lvlA = state[A][2]
            if lvlA < 5 and self.can_upgrade(state, A):
                return 2, A, 0
            # If A < 5 and cannot upgrade yet, avoid draining troops from A
            if lvlA < 5:
                # Optionally capture neutral B if A is very full; otherwise wait
                if self.neutral(state, B) and state[A][3] >= fortress_limit[lvlA] * 0.9 and self.can_send(state, A):
                    return 1, A, B
                return 0, 0, 0

        # Phase 2: Take B first
        if self.own(state, A):
            lvlA = state[A][2]
            # While B not owned: A->B gated at 70% once A is Lv5
            if not self.own(state, B):
                if lvlA >= 5:
                    limitA = fortress_limit[lvlA]
                    if state[A][3] >= int(limitA * 0.7) and self.can_send(state, A):
                        return 1, A, B
                # else wait to reach Lv5/threshold
                return 0, 0, 0
            # If B is owned but not Lv5: upgrade B and stream A->B continuously
            if self.own(state, B) and state[B][2] < 5:
                if self.can_upgrade(state, B):
                    return 2, B, 0
                if self.can_send(state, A):
                    return 1, A, B

        # Phase 3: After B reaches Lv5, continuously send B->A and A->C; upgrade C to Lv5 when owned
        if self.own(state, B) and state[B][2] >= 5:
            # If C is owned and not Lv5, upgrade when possible
            if self.own(state, C) and state[C][2] < 5 and self.can_upgrade(state, C):
                return 2, C, 0

            can_A_to_C = self.can_send(state, A)
            can_B_to_A = self.can_send(state, B)

            if not self.own(state, C):
                # Alternate between A->C and B->A if both available; otherwise send whichever is available
                if can_A_to_C and can_B_to_A:
                    if self.step % 2 == 0:
                        return 1, A, C
                    else:
                        return 1, B, A
                if can_A_to_C:
                    return 1, A, C
                if can_B_to_A:
                    return 1, B, A
            else:
                # If C owned (possibly already Lv5 later), continue alternating A->C and B->A until Phase 4 kicks in
                if can_A_to_C and can_B_to_A:
                    if self.step % 2 == 0:
                        return 1, A, C
                    else:
                        return 1, B, A
                if can_A_to_C:
                    return 1, A, C
                if can_B_to_A:
                    return 1, B, A

        # (Phase 4 handled above with alternation and bridge attacks)

        # Phase 5: From Center, attack opponent's frontline
        if self.own(state, Center) and self.can_send(state, Center):
            center_neighbors = self.neighbors(state, Center)
            enemy_neighbors = [n for n in center_neighbors if self.enemy(state, n)]
            neutral_neighbors = [n for n in center_neighbors if self.neutral(state, n)]

            target = None
            # Special case: if enemy still holds any of their base triangle, prefer attacking their Center
            enemy_base_present = any(self.enemy(state, i) for i in enemy_base)
            if enemy_base_present and self.enemy(state, enemy_center):
                target = enemy_center
            else:
                # Prefer enemy neighbors (choose with lowest pawns), excluding enemy base forts when possible
                non_base_enemies = [n for n in enemy_neighbors if n not in enemy_base]
                candidates = non_base_enemies if non_base_enemies else enemy_neighbors
                if candidates:
                    target = min(candidates, key=lambda i: state[i][3])
                elif neutral_neighbors:
                    target = min(neutral_neighbors, key=lambda i: state[i][3])

            if target is not None:
                return 1, Center, target

        # Fallbacks: If we don't own A yet (early), try to claim it via neighbors
        # Try capturing A from B/C if they are ours and adjacent
        if not self.own(state, A):
            for src in [B, C]:
                if self.own(state, src) and A in self.neighbors(state, src) and self.can_send(state, src):
                    return 1, src, A

        # If nothing to do, idle
        return 0, 0, 0
