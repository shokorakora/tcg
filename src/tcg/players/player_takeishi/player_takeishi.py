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
        self.send_cooldown = 5
        # global attack pacing
        self.last_global_attack_step = -10**9
        self.global_attack_gap = 8
        # short-term suppression of repeated (src,dst)
        self.pair_hits: dict[tuple[int,int], tuple[int,int]] = {}
        # lightweight metrics
        self.metrics = {
            "idle": 0,
            "attack": 0,
            "global_attack": 0,
            "concentrate": 0,
            "expand": 0,
            "rear_probe": 0,
            "rear_forward": 0,
            "mobilize": 0,
            "probe_enemy": 0,
            "probe_neutral": 0,
            "upgrade": 0,
        }

    def team_name(self) -> str:
        return "TakeishiAI"

    def update(self, info) -> tuple[int, int, int]:
        self.step += 1
        team, state, moving_pawns, spawning_pawns, done = info

        # periodic metrics snapshot regardless of branch
        if self.step % 600 == 0:
            m = self.metrics
            print(f"[Takeishi] METRICS step{self.step}: winrate=N/A, idle={m['idle']}, atk={m['attack']}, gatk={m['global_attack']}, conc={m['concentrate']}, exp={m['expand']}, rprobe={m['rear_probe']}, rforw={m['rear_forward']}, mob={m['mobilize']}")

        # if game ended, emit final metrics snapshot once and no-op
        if done:
            m = self.metrics
            print(
                f"[Takeishi] FINAL_METRICS step{self.step}: idle={m['idle']}, atk={m['attack']}, gatk={m['global_attack']}, "
                f"conc={m['concentrate']}, exp={m['expand']}, rprobe={m['rear_probe']}, rforw={m['rear_forward']}, "
                f"mob={m['mobilize']}, probeE={m['probe_enemy']}, probeN={m['probe_neutral']}, upg={m['upgrade']}"
            )
            return (0, 0, 0)

        # 自軍拠点一覧
        my_forts = [i for i, f in enumerate(state) if f[0] == 1]
        if not my_forts:
            return (0, 0, 0)

        # choose a primary source (most pawns)
        my_forts.sort(key=lambda idx: state[idx][3], reverse=True)
        src = my_forts[0]
        _, _, src_level, src_pawns, src_upg_time, src_neighbors = state[src]

        # 0) If any fort is ready to upgrade but lacks required pawns, feed it first.
        lacking = []
        for j in my_forts:
            t, _, lvl, pawns, upg_time, _ = state[j]
            if lvl >= 5:
                continue
            if upg_time < 0:
                need = max(1, fortress_limit[lvl] // 3)
                if pawns < need:
                    lacking.append((lvl, pawns, j, need))
        if lacking:
            lacking.sort()  # lowest level, then lowest pawns
            lvl, pawns, recv, need = lacking[0]
            donors = [n for n in state[recv][5] if state[n][0] == 1 and n != recv and state[n][3] >= 3]
            if donors:
                # pick the strongest donor
                donor = max(donors, key=lambda n: state[n][3])
                key = (donor, recv)
                if self.last_sent.get(key, -9999) + self.send_cooldown <= self.step:
                    self.last_sent[key] = self.step
                    self.idle_steps = 0
                    print(f"[Takeishi] step{self.step} FEED_UPGRADE from {donor} -> {recv} (need:{need}, p_donor:{state[donor][3]}, p_recv:{pawns})")
                    self.metrics["concentrate"] += 1
                    return (1, donor, recv)

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
            self.metrics["upgrade"] += 1
            return (2, subj, 0)

        # 2) Do not freeze globally during upgrades; allow other actions to proceed.

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
            # Dynamic aggression based on map control
            my_count = sum(1 for i, f in enumerate(state) if f[0] == 1)
            enemy_count = sum(1 for i, f in enumerate(state) if f[0] != 0 and f[0] != 1)
            if my_count >= enemy_count + 1:
                req_level_factor = 5
                harass_every = 6
            elif enemy_count >= my_count + 1:
                req_level_factor = 3
                harass_every = 4
            else:
                req_level_factor = 4
                harass_every = 5
            # Aggressive policy when idle: prefer attacking enemy forts, then weak neutrals.
            # Make harassment periodic and lower thresholds to avoid long idle times.
            min_send_half = 2

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
                    required = state[candidate][3] + state[candidate][2] * req_level_factor + 2
                    if s_pawns // 2 < required:
                        continue
                    key = (s, candidate)
                    if self.last_sent.get(key, -9999) + self.send_cooldown > self.step:
                        continue
                    # pair suppression within 50-step window
                    cnt, last = self.pair_hits.get(key, (0, -10**9))
                    if self.step - last <= 50 and cnt >= 3:
                        continue
                    self.pair_hits[key] = (cnt + 1 if self.step - last <= 50 else 1, self.step)
                    self.last_sent[key] = self.step
                    self.idle_steps = 0
                    print(f"[Takeishi] step{self.step} ATTACK from {s} -> enemy {candidate} (p:{s_pawns})")
                    self.metrics["attack"] += 1
                    return (1, s, candidate)

            # 2) If no adjacent enemy, try global weakest enemy if primary src can spare
            enemies = [i for i, f in enumerate(state) if f[0] != 0 and f[0] != 1]
            if enemies and (self.step - self.last_global_attack_step) >= self.global_attack_gap:
                global_req_factor = req_level_factor + 1
                for candidate in sorted(enemies, key=lambda n: (state[n][3] + state[n][2] * 5)):
                    required = state[candidate][3] + state[candidate][2] * global_req_factor + 2
                    if src_pawns // 2 < required:
                        continue
                    key = (src, candidate)
                    if self.last_sent.get(key, -9999) + self.send_cooldown > self.step:
                        continue
                    cnt, last = self.pair_hits.get(key, (0, -10**9))
                    if self.step - last <= 50 and cnt >= 2:
                        continue
                    self.pair_hits[key] = (cnt + 1 if self.step - last <= 50 else 1, self.step)
                    self.last_sent[key] = self.step
                    self.idle_steps = 0
                    self.last_global_attack_step = self.step
                    print(f"[Takeishi] step{self.step} GLOBAL_ATTACK from {src} -> enemy {candidate} (p:{src_pawns})")
                    self.metrics["global_attack"] += 1
                    return (1, src, candidate)

            # 3) Move troops toward frontline: concentrate forces on a frontline fortress
            frontlines = [f for f in my_forts if any(state[n][0] != 1 for n in state[f][5])]
            if frontlines:
                # score frontlines by enemy pressure and expansion potential
                def frontline_score(fidx: int) -> int:
                    en = [n for n in state[fidx][5] if state[n][0] != 1]
                    score = 0
                    for n in en:
                        # enemy neighbors weigh more than neutral
                        score += (5 if state[n][0] != 0 else 2)
                        score += state[n][3] // 3
                    return score

                best_front = max(frontlines, key=frontline_score)
                # if src is not frontline, move from src to the highest pressure frontline
                if src not in frontlines and src_pawns // 2 >= 1:
                    recv = best_front
                    if state[recv][3] >= 12:
                        pass
                    key = (src, recv)
                    if self.last_sent.get(key, -9999) + self.send_cooldown <= self.step:
                        self.last_sent[key] = self.step
                        self.idle_steps = 0
                        print(f"[Takeishi] step{self.step} CONCENTRATE from {src} -> {recv} (p:{src_pawns})")
                        self.metrics["concentrate"] += 1
                        return (1, src, recv)

            # 3b) Rear mobilization: if some rear forts (not frontline) are sitting with many pawns,
            # send probes to neutral 8 if available or forward to a nearer frontline/weak neighbor.
            for f in my_forts:
                f_pawns = state[f][3]
                if f in frontlines:
                    continue
                if f_pawns < 8:
                    continue
                # prefer neutral 8 if adjacent
                if 8 in state[f][5] and state[8][0] == 0:
                    key = (f, 8)
                    if self.last_sent.get(key, -9999) + self.send_cooldown <= self.step:
                        self.last_sent[key] = self.step
                        self.idle_steps = 0
                        print(f"[Takeishi] step{self.step} REAR_PROBE from {f} -> neutral 8 (p:{f_pawns})")
                        self.metrics["rear_probe"] += 1
                        return (1, f, 8)
                # else forward to weakest neighboring frontline or lower-pawn own neighbor
                own_neighbors = [n for n in state[f][5] if state[n][0] == 1]
                if own_neighbors:
                    recv = min(own_neighbors, key=lambda n: state[n][3])
                    if state[recv][3] + 2 < f_pawns:
                        key = (f, recv)
                        if self.last_sent.get(key, -9999) + self.send_cooldown <= self.step:
                            self.last_sent[key] = self.step
                            self.idle_steps = 0
                            print(f"[Takeishi] step{self.step} REAR_FORWARD from {f} -> {recv} (p:{f_pawns})")
                            self.metrics["rear_forward"] += 1
                            return (1, f, recv)

            # 4) Otherwise, opportunistically expand to nearest weak neutral from any suitable fort (src first)
            order = [src] + [f for f in my_forts if f != src]
            for s in order:
                s_pawns = state[s][3]
                if s_pawns // 2 < 1:
                    continue
                neutral = [n for n in state[s][5] if state[n][0] == 0]
                if neutral:
                    # choose weakest neutral we can take now
                    candidates = sorted(neutral, key=lambda n: (state[n][3], state[n][2]))
                    target = None
                    for n in candidates:
                        need = state[n][3] + state[n][2] * 2 + 1
                        if s_pawns // 2 >= need:
                            target = n
                            break
                    if target is None:
                        continue
                    key = (s, target)
                    if self.last_sent.get(key, -9999) + self.send_cooldown <= self.step:
                        self.last_sent[key] = self.step
                        self.idle_steps = 0
                        print(f"[Takeishi] step{self.step} EXPAND from {s} -> neutral {target} (p:{s_pawns})")
                        self.metrics["expand"] += 1
                        return (1, s, target)

            # nothing sensible to do, keep accumulating
            self.idle_steps += 1
            # if idle too long, mobilize (send small probes or concentrate)
            if self.idle_steps >= 3:
                # try to move from non-frontline to frontline or probe nearest enemy
                frontlines = [f for f in my_forts if any(state[n][0] != 1 for n in state[f][5])]
                moved = False
                for s in my_forts:
                    if state[s][3] < 2:
                        continue
                    if frontlines and s not in frontlines:
                        recv = frontlines[0]
                        print(f"[Takeishi] step{self.step} MOBILIZE from {s} -> {recv} (p:{state[s][3]})")
                        self.metrics["mobilize"] += 1
                        self.idle_steps = 0
                        return (1, s, recv)
                # if no frontlines, probe global weakest enemy or neutral
                enemies = [i for i, f in enumerate(state) if f[0] != 0 and f[0] != 1]
                if enemies:
                    for s in my_forts:
                        if state[s][3] >= 2:
                            weakest = min(enemies, key=lambda n: (state[n][3] + state[n][2] * 5))
                            print(f"[Takeishi] step{self.step} PROBE from {s} -> enemy {weakest} (p:{state[s][3]})")
                            self.metrics["probe_enemy"] += 1
                            self.idle_steps = 0
                            return (1, s, weakest)
                # else probe neutral from src
                if src_pawns // 2 >= 1:
                    neutral = [n for n in src_neighbors if state[n][0] == 0]
                    if neutral:
                        # probe only if we can likely capture now
                        candidates = sorted(neutral, key=lambda n: (state[n][3], state[n][2]))
                        target = None
                        for n in candidates:
                            need = state[n][3] + state[n][2] * 2 + 1
                            if src_pawns // 2 >= need:
                                target = n
                                break
                        if target is not None:
                            print(f"[Takeishi] step{self.step} PROBE_NEUTRAL from {src} -> {target} (p:{src_pawns})")
                            self.metrics["probe_neutral"] += 1
                            self.idle_steps = 0
                            return (1, src, target)

            print(f"[Takeishi] step{self.step} IDLE (no actions)")
            self.metrics["idle"] += 1
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
            return sent >= (state[to][3] + state[to][2] + 2)

        # look for a source that has the target as neighbor and can take it
        candidate_src = None
        for s in my_forts:
            neighbors = state[s][5]
            if target in neighbors and can_take(s, target):
                candidate_src = s
                break

        if candidate_src is not None:
            return (1, candidate_src, target)

        # If no single source can take target, try cooperative staging:
        # if multiple adjacent friendly forts can together send enough, start by sending from the largest
        adj_my = [s for s in my_forts if target in state[s][5] and state[s][3] >= 2]
        if adj_my:
            total_potential = sum(state[s][3] // 2 for s in adj_my)
            req = state[target][3] + state[target][2] + 2
            if total_potential >= req:
                donor = max(adj_my, key=lambda s: state[s][3])
                key = (donor, target)
                if self.last_sent.get(key, -9999) + self.send_cooldown <= self.step:
                    self.last_sent[key] = self.step
                    self.idle_steps = 0
                    print(f"[Takeishi] step{self.step} STAGE_ATTACK from {donor} -> {target} (p:{state[donor][3]})")
                    self.metrics["attack"] += 1
                    return (1, donor, target)

        # if no single source can take it yet, let other forts act (expand/mobilize) instead of freezing
        # try expansion from any fort
        for s in my_forts:
            s_pawns = state[s][3]
            if s_pawns // 2 < 2:
                continue
            neutral = [n for n in state[s][5] if state[n][0] == 0]
            if not neutral:
                continue
            candidates = sorted(neutral, key=lambda n: (state[n][3], state[n][2]))
            for n in candidates:
                need = state[n][3] + state[n][2] * 2 + 1
                if s_pawns // 2 >= need:
                    key = (s, n)
                    if self.last_sent.get(key, -9999) + self.send_cooldown <= self.step:
                        self.last_sent[key] = self.step
                        self.idle_steps = 0
                        print(f"[Takeishi] step{self.step} FALLBACK_EXPAND from {s} -> neutral {n} (p:{s_pawns})")
                        self.metrics["expand"] += 1
                        return (1, s, n)

        # otherwise try rear mobilization from non-frontline forts
        frontlines = [f for f in my_forts if any(state[n][0] != 1 for n in state[f][5])]
        for f in my_forts:
            if f in frontlines:
                continue
            f_pawns = state[f][3]
            if f_pawns < 6:
                continue
            if 8 in state[f][5] and state[8][0] == 0:
                key = (f, 8)
                if self.last_sent.get(key, -9999) + self.send_cooldown <= self.step:
                    self.last_sent[key] = self.step
                    self.idle_steps = 0
                    print(f"[Takeishi] step{self.step} FALLBACK_REAR_PROBE from {f} -> neutral 8 (p:{f_pawns})")
                    self.metrics["rear_probe"] += 1
                    return (1, f, 8)
            own_neighbors = [n for n in state[f][5] if state[n][0] == 1]
            if own_neighbors:
                recv = min(own_neighbors, key=lambda n: state[n][3])
                if state[recv][3] + 2 < f_pawns:
                    key = (f, recv)
                    if self.last_sent.get(key, -9999) + self.send_cooldown <= self.step:
                        self.last_sent[key] = self.step
                        self.idle_steps = 0
                        print(f"[Takeishi] step{self.step} FALLBACK_REAR_FORWARD from {f} -> {recv} (p:{f_pawns})")
                        self.metrics["rear_forward"] += 1
                        return (1, f, recv)

        # nothing sensible to do for target now
        return (0, 0, 0)