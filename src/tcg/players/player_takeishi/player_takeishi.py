from tcg.controller import Controller
from tcg.config import fortress_limit

class TakeishiPlayer(Controller):
    def __init__(self) -> None:
        super().__init__()
        self.step = 0
        # target capture plan: try to take these in order and upgrade them to level 5
        self.targets = [9, 11]
        self.target_index = 0
        # idle detection: count consecutive idle turns to trigger mobilization
        self.idle_steps = 0
        # throttle repeated sends: record last send step per (src,target)
        self.last_sent = {}
        self.send_cooldown = 3

    def team_name(self) -> str:
        return "TakeishiAI"

    def update(self, info) -> tuple[int, int, int]:
        self.step += 1
        team, state, moving_pawns, spawning_pawns, done = info

        # 自軍拠点一覧
        my_forts = [i for i, f in enumerate(state) if f[0] == 1]
        if not my_forts:
            return (0, 0, 0)

        # choose a primary source (most pawns)
        my_forts.sort(key=lambda idx: state[idx][3], reverse=True)
        src = my_forts[0]
        _, _, src_level, src_pawns, src_upg_time, src_neighbors = state[src]

        # 1) If any of our forts (including captured targets) can/should be upgraded, prefer that.
        # pick the lowest-level upgradable fortress we own
        upg_candidates = []
        for j in my_forts:
            t, _, lvl, pawns, upg_time, _ = state[j]
            if lvl >= 5:
                continue
            # in this environment upgrade_time < 0 means ready
            if upg_time >= 0:
                continue
            need = max(1, fortress_limit[lvl] // 3)
            if pawns >= need:
                upg_candidates.append((lvl, -pawns, j))
        if upg_candidates:
            upg_candidates.sort()
            _, _, subj = upg_candidates[0]
            return (2, subj, 0)

        # 2) If currently upgrading (any of our forts has upg_time >=0 and lvl<5), wait
        for j in my_forts:
            if state[j][2] < 5 and state[j][4] >= 0:
                return (0, 0, 0)

        # 3) Target capture flow: try to capture targets[self.target_index] then upgrade it to 5
        # advance index to next unfinished target
        while self.target_index < len(self.targets):
            tgt = self.targets[self.target_index]
            # if target already belongs to us and is lvl>=5, mark done and continue
            if state[tgt][0] == 1 and state[tgt][2] >= 5:
                self.target_index += 1
                continue
            break

        # if all targets done, fall back to aggressive expansion/attacking behavior
        if self.target_index >= len(self.targets):
            # Aggressive policy when idle: prefer attacking enemy forts, then weak neutrals.
            # Make harassment periodic and lower thresholds to avoid long idle times.
            min_send_half = 2
            harass_every = 5
            if self.step % harass_every == 0:
                min_send_half = 1

            # 1) Try adjacent enemy attack from any of our forts that has enough pawns
            for s in my_forts:
                s_pawns = state[s][3]
                if s_pawns // 2 < min_send_half:
                    continue
                en_neighbors = [n for n in state[s][5] if state[n][0] != 0 and state[n][0] != 1]
                if not en_neighbors:
                    continue
                # try candidates ordered by weakness; attack if our send (half) exceeds required estimate
                for candidate in sorted(en_neighbors, key=lambda n: (state[n][3] + state[n][2] * 5)):
                    required = state[candidate][3] + state[candidate][2] * 3 + 1
                    if s_pawns // 2 < required:
                        continue
                    key = (s, candidate)
                    if self.last_sent.get(key, -9999) + self.send_cooldown > self.step:
                        continue
                    self.last_sent[key] = self.step
                    self.idle_steps = 0
                    print(f"[Takeishi] step{self.step} ATTACK from {s} -> enemy {candidate} (p:{s_pawns})")
                    return (1, s, candidate)

            # 2) If no adjacent enemy, try global weakest enemy if primary src can spare
            enemies = [i for i, f in enumerate(state) if f[0] != 0 and f[0] != 1]
            if enemies:
                for candidate in sorted(enemies, key=lambda n: (state[n][3] + state[n][2] * 5)):
                    required = state[candidate][3] + state[candidate][2] * 3 + 1
                    if src_pawns // 2 < required:
                        continue
                    key = (src, candidate)
                    if self.last_sent.get(key, -9999) + self.send_cooldown > self.step:
                        continue
                    self.last_sent[key] = self.step
                    self.idle_steps = 0
                    print(f"[Takeishi] step{self.step} GLOBAL_ATTACK from {src} -> enemy {candidate} (p:{src_pawns})")
                    return (1, src, candidate)

            # 3) Move troops toward frontline: concentrate forces on a frontline fortress
            frontlines = [f for f in my_forts if any(state[n][0] != 1 for n in state[f][5])]
            if frontlines:
                # if src is not frontline, move half from src to a frontline fort
                if src not in frontlines and src_pawns // 2 >= 1:
                    recv = frontlines[0]
                    key = (src, recv)
                    if self.last_sent.get(key, -9999) + self.send_cooldown <= self.step:
                        self.last_sent[key] = self.step
                        self.idle_steps = 0
                        print(f"[Takeishi] step{self.step} CONCENTRATE from {src} -> {recv} (p:{src_pawns})")
                        return (1, src, recv)

            # 4) Otherwise, opportunistically expand to nearest weak neutral from primary src
            if src_pawns // 2 >= 1:
                neutral = [n for n in src_neighbors if state[n][0] == 0]
                if neutral:
                    target = min(neutral, key=lambda n: (state[n][3], state[n][2]))
                    key = (src, target)
                    if self.last_sent.get(key, -9999) + self.send_cooldown <= self.step:
                        self.last_sent[key] = self.step
                        self.idle_steps = 0
                        print(f"[Takeishi] step{self.step} EXPAND from {src} -> neutral {target} (p:{src_pawns})")
                        return (1, src, target)

            # nothing sensible to do, keep accumulating
            self.idle_steps += 1
            # if idle too long, mobilize (send small probes or concentrate)
            if self.idle_steps >= 5:
                # try to move from non-frontline to frontline or probe nearest enemy
                frontlines = [f for f in my_forts if any(state[n][0] != 1 for n in state[f][5])]
                moved = False
                for s in my_forts:
                    if state[s][3] < 2:
                        continue
                    if frontlines and s not in frontlines:
                        recv = frontlines[0]
                        print(f"[Takeishi] step{self.step} MOBILIZE from {s} -> {recv} (p:{state[s][3]})")
                        self.idle_steps = 0
                        return (1, s, recv)
                # if no frontlines, probe global weakest enemy or neutral
                enemies = [i for i, f in enumerate(state) if f[0] != 0 and f[0] != 1]
                if enemies:
                    for s in my_forts:
                        if state[s][3] >= 2:
                            weakest = min(enemies, key=lambda n: (state[n][3] + state[n][2] * 5))
                            print(f"[Takeishi] step{self.step} PROBE from {s} -> enemy {weakest} (p:{state[s][3]})")
                            self.idle_steps = 0
                            return (1, s, weakest)
                # else probe neutral from src
                if src_pawns // 2 >= 1:
                    neutral = [n for n in src_neighbors if state[n][0] == 0]
                    if neutral:
                        target = min(neutral, key=lambda n: (state[n][3], state[n][2]))
                        print(f"[Takeishi] step{self.step} PROBE_NEUTRAL from {src} -> {target} (p:{src_pawns})")
                        self.idle_steps = 0
                        return (1, src, target)

            print(f"[Takeishi] step{self.step} IDLE (no actions)")
            return (0, 0, 0)

        # operate on current target
        target = self.targets[self.target_index]
        t_team, t_kind, t_level, t_pawns, t_upg_time, t_neighbors = state[target]

        # If we already own the target but it's not lvl5, try upgrading it when ready
        if t_team == 1 and t_level < 5:
            if t_upg_time < 0:
                need = max(1, fortress_limit[t_level] // 3)
                if state[target][3] >= need:
                    return (2, target, 0)
            # if upgrading in progress or not enough pawns, wait to accumulate
            return (0, 0, 0)

        # If target not ours, try to attack from a source that is adjacent and strong enough
        # prefer sending from src if adjacent
        def can_take(frm, to):
            sent = state[frm][3] // 2
            return sent >= (state[to][3] + state[to][2] + 1)

        # look for a source that has the target as neighbor and can take it
        candidate_src = None
        for s in my_forts:
            neighbors = state[s][5]
            if target in neighbors and can_take(s, target):
                candidate_src = s
                break

        if candidate_src is not None:
            return (1, candidate_src, target)

        # if no single source can take it yet, try to move from src to a neutral/easier neighbor to strengthen position
        # but avoid splitting: prefer to wait until enough pawns
        return (0, 0, 0)