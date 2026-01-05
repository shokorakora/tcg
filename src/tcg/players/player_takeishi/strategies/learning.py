"""
Takeishi learning helpers and a minimal DQN scaffold.

Usage:
 - This file provides a featurizer, candidate generator, a small Q-network,
   a replay buffer, and a `LearningAgent` wrapper that can be used as a
   Controller replacement during training or inference.

Notes:
 - Requires PyTorch for training/inference. If not available, `LearningAgent`
   falls back to random candidate selection.
 - This is intentionally minimal to be a practical starting point.
"""
from __future__ import annotations
import random
import collections
from typing import List, Tuple, Optional
import numpy as np
from tcg import config as cfg

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
except Exception:
    torch = None

# State featurizer (global features)
def featurize_state(state) -> np.ndarray:
    my_pawns = 0
    en_pawns = 0
    my_count = 0
    en_count = 0
    my_level = 0
    en_level = 0
    for f in state:
        team, _, lvl, pawns, upg_time, _ = f
        if team == 1:
            my_count += 1
            my_pawns += pawns
            my_level += lvl
        elif team != 0:
            en_count += 1
            en_pawns += pawns
            en_level += lvl
    vec = [
        float(my_pawns), float(en_pawns), float(my_count), float(en_count),
        float(my_level) / max(1.0, float(my_count)),
        float(en_level) / max(1.0, float(en_count)),
    ]
    return np.array(vec, dtype=np.float32)

# Per-action local features (supports move and upgrade)
def featurize_action(state, cmd: int, src: int, dst: int) -> np.ndarray:
    s_team, _, s_lvl, s_pawns, s_upg, s_neighbors = state[src]
    if cmd == 2:
        # upgrade feature vector: reuse shape with relevant fields
        from tcg.config import fortress_limit
        half_send = float(s_pawns // 2)
        required = float(fortress_limit[s_lvl] // 2)
        margin = half_send - required
        vec = [
            float(s_lvl), float(s_pawns), 0.0, 0.0,
            0.0, 0.0, half_send, required, margin,
        ]
        return np.array(vec, dtype=np.float32)
    d_team, _, d_lvl, d_pawns, d_upg, d_neighbors = state[dst]
    is_enemy = 1.0 if (d_team != 0 and d_team != 1) else 0.0
    is_neutral = 1.0 if d_team == 0 else 0.0
    half_send = float(s_pawns // 2)
    needed = float(d_pawns + d_lvl * 2 + 1)
    margin = half_send - needed
    vec = [
        float(s_lvl), float(s_pawns), float(d_lvl), float(d_pawns),
        is_enemy, is_neutral, half_send, needed, margin,
    ]
    return np.array(vec, dtype=np.float32)

# Candidate actions generator (src, target)
def generate_action_candidates(state) -> List[Tuple[int,int,int]]:
    my_forts = [i for i,f in enumerate(state) if f[0] == 1]
    if not my_forts:
        return []
    candidates: List[Tuple[int,int,int]] = []
    # -1) Neutral fast-path: when a Level 5 source is near full and adjacent neutral exists,
    #     include neutral capture candidates early to reduce brief idling.
    from tcg.config import fortress_limit
    for s in my_forts:
        team, kind, lvl, pawns, upg, neighbors = state[s]
        if lvl == 5 and pawns >= int(fortress_limit[lvl] * 0.9):
            neutrals = [n for n in neighbors if state[n][0] == 0]
            if neutrals and pawns >= 2:
                half_send = pawns // 2
                dmg = 0.95 if kind == 1 else 0.65
                # Prefer viable neutrals by expected arrival damage (no extra margin)
                viable = [n for n in neutrals if (half_send * dmg) >= (state[n][3])]
                if viable:
                    target = min(viable, key=lambda n: state[n][3])
                    candidates.append((1, s, target))
                else:
                    # If at absolute max capacity, probe weakest neutral to avoid idling
                    if pawns >= fortress_limit[lvl]:
                        target = min(neutrals, key=lambda n: state[n][3])
                        candidates.append((1, s, target))
    # 0) Upgrades where possible
    for s in my_forts:
        team, kind, lvl, pawns, upg, _ = state[s]
        # upgrade possible: enough pawns, not already upgrading, level 1..4
        # fortress_limit index by level
        if upg == -1 and 1 <= lvl <= 4 and pawns >= fortress_limit[lvl] // 2:
            candidates.append((2, s, s))
    # 1) Feasible expansions and attacks from owned forts
    for s in my_forts:
        pawns = state[s][3]
        if pawns < 2:
            continue
        half_send = pawns // 2
        dmg = 0.95 if state[s][1] == 1 else 0.65
        for n in state[s][5]:
            d_team, _, d_lvl, d_pawns, _, _ = state[n]
            # Use expected arrival damage to avoid weak/trickle sends
            if (half_send * dmg) <= (d_pawns + 2):
                continue
            if d_team == 0:
                candidates.append((1, s, n))
            elif d_team != 1:
                candidates.append((1, s, n))
    # 2) Concentrates toward a frontline if no feasible attack/capture
    frontlines = [f for f in my_forts if any(state[n][0] != 1 for n in state[f][5])]
    if frontlines:
        for s in my_forts:
            if s not in frontlines:
                lvl = state[s][2]
                from tcg.config import fortress_limit
                # only reinforce when near full to avoid trickles
                if state[s][3] >= int(fortress_limit[lvl] * 0.85):
                    # concentrate only via adjacent edge to a frontline fortress
                    for n in state[s][5]:
                        if n in frontlines:
                            candidates.append((1, s, n))
                            break
    # dedupe while preserving order
    seen = set()
    out: List[Tuple[int,int,int]] = []
    for a in candidates:
        if a not in seen:
            seen.add(a)
            out.append(a)
    return out

# Simple heuristic fallback when the network is untrained/indecisive
def heuristic_fallback(state) -> Tuple[int,int,int]:
    my_forts = [i for i,f in enumerate(state) if f[0] == 1 and f[3] >= 2]
    if not my_forts:
        return (0,0,0)
    # Prefer sending from the fort with most pawns
    my_forts_sorted = sorted(my_forts, key=lambda i: state[i][3], reverse=True)
    # Target-first plan: ensure 9 and 11 are captured and upgraded to 5 early
    targets = [9, 11]
    from tcg.config import fortress_limit
    for tgt in targets:
        t_team, _, t_lvl, t_pawns, t_upg, t_neighbors = state[tgt]
        # If we own the target and can upgrade now, do it first
        if t_team == 1 and t_lvl < 5 and t_upg == -1:
            need = max(1, fortress_limit[t_lvl] // 3)
            if t_pawns >= need:
                return (2, tgt, tgt)
            # If lacking pawns, feed from strongest adjacent owned donor
            donors = [n for n in t_neighbors if state[n][0] == 1 and state[n][3] >= 3]
            if donors:
                donor = max(donors, key=lambda n: state[n][3])
                return (1, donor, tgt)
        # If we don't own it, try adjacent capture from strongest owned neighbor
        if t_team != 1:
            adj_my = [s for s in t_neighbors if state[s][0] == 1]
            best = None
            for s in adj_my:
                half_send = state[s][3] // 2
                needed = t_pawns + t_lvl * 2 + 1
                if half_send >= needed:
                    # prefer the largest sender
                    if best is None or state[s][3] > state[best][3]:
                        best = s
            if best is not None:
                return (1, best, tgt)
    # Priority plan: capture 9, then 11 from 10 if feasible
    if 10 in my_forts_sorted:
        s = 10
        for target in [9, 11]:
            if target in state[s][5]:
                d_team, _, d_lvl, d_pawns, _, _ = state[target]
                needed = d_pawns + d_lvl * 2 + 1
                half_send = state[s][3] // 2
                if half_send >= needed and d_team != 1:
                    return (1, s, target)
    # 0) Upgrade if possible (generic)
    for s in my_forts_sorted:
        team, kind, lvl, pawns, upg, _ = state[s]
        if upg == -1 and 1 <= lvl <= 4 and pawns >= fortress_limit[lvl] // 2:
            return (2, s, s)
    # 1) Prefer neutral capture with lowest effective defense
    best = None
    for s in my_forts_sorted:
        for n in state[s][5]:
            d_team, _, d_lvl, d_pawns, _, _ = state[n]
            if d_team == 0:
                needed = d_pawns + d_lvl * 2 + 1
                half_send = state[s][3] // 2
                if half_send < needed:
                    continue
                score = needed
                if best is None or score < best[0]:
                    best = (score, (1, s, n))
        if best is not None:
            return best[1]
    # 2) Attack weakest adjacent enemy
    best = None
    for s in my_forts_sorted:
        for n in state[s][5]:
            d_team, _, d_lvl, d_pawns, _, _ = state[n]
            if d_team != 0 and d_team != 1:
                needed = d_pawns + d_lvl * 2 + 1
                half_send = state[s][3] // 2
                if half_send < needed:
                    continue
                score = needed
                if best is None or score < best[0]:
                    best = (score, (1, s, n))
        if best is not None:
            return best[1]
    # 3) Concentrate toward any frontline
    frontlines = [f for f in my_forts_sorted if any(state[n][0] != 1 for n in state[f][5])]
    if frontlines:
        target = frontlines[0]
        for s in my_forts_sorted:
            if s != target:
                return (1, s, target)
    return (0,0,0)

# Small Q-network (scores a state representation)
class QNet(nn.Module):
    def __init__(self, inp_dim: int, hid: int = 128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(inp_dim, hid),
            nn.ReLU(),
            nn.Linear(hid, hid),
            nn.ReLU(),
            nn.Linear(hid, 1),
        )
    def forward(self, x):
        return self.net(x).squeeze(-1)

# Dueling-style Q-network: Q(s,a) = V(s) + A(s,a)
class QNetDueling(nn.Module):
    def __init__(self, state_dim: int, action_dim: int, hid: int = 128):
        super().__init__()
        # Value stream depends only on state features
        self.value = nn.Sequential(
            nn.Linear(state_dim, hid),
            nn.ReLU(),
            nn.Linear(hid, hid),
            nn.ReLU(),
            nn.Linear(hid, 1),
        )
        # Advantage stream depends on combined state+action features
        self.adv = nn.Sequential(
            nn.Linear(state_dim + action_dim, hid),
            nn.ReLU(),
            nn.Linear(hid, hid),
            nn.ReLU(),
            nn.Linear(hid, 1),
        )
        self.state_dim = state_dim
        self.action_dim = action_dim
    def forward(self, x):
        # x is concatenated [state, action]
        s = x[..., :self.state_dim]
        v = self.value(s)
        a = self.adv(x)
        return (v + a).squeeze(-1)

class PrioritizedReplayBuffer:
    """Proportional PER buffer with simple weighted sampling.

    Stores (experience, priority). Sampling uses p_i^alpha / sum p^alpha.
    Returns indices, batch, and importance weights w_i.
    """
    def __init__(self, capacity: int = 20000, alpha: float = 0.6, beta_start: float = 0.4, beta_increment: float = 1e-4, eps: float = 1e-5):
        self.capacity = capacity
        self.buffer: list[tuple] = []
        self.priorities: list[float] = []
        self.pos = 0
        self.alpha = alpha
        self.beta = beta_start
        self.beta_increment = beta_increment
        self.eps = eps
        self._max_priority = 1.0
    def push(self, experience):
        if len(self.buffer) < self.capacity:
            self.buffer.append(experience)
            self.priorities.append(self._max_priority)
        else:
            self.buffer[self.pos] = experience
            self.priorities[self.pos] = self._max_priority
            self.pos = (self.pos + 1) % self.capacity
    def sample(self, batch_size: int):
        n = len(self.buffer)
        if n == 0:
            return [], [], []
        # Probabilities
        probs = np.array(self.priorities[:n], dtype=np.float32) ** self.alpha
        probs_sum = float(probs.sum()) if float(probs.sum()) > 0 else 1.0
        probs = probs / probs_sum
        idxs = np.random.choice(n, size=batch_size, replace=False if n >= batch_size else True, p=probs)
        batch = [self.buffer[int(i)] for i in idxs]
        # Importance sampling weights
        w = (n * probs[idxs]) ** (-self.beta)
        w = w / (w.max() + 1e-8)
        # Anneal beta
        self.beta = min(1.0, self.beta + self.beta_increment)
        return idxs, batch, w.astype(np.float32)
    def update_priorities(self, idxs, new_priorities):
        for i, p in zip(idxs, new_priorities):
            pr = float(abs(p)) + self.eps
            self.priorities[int(i)] = pr
            if pr > self._max_priority:
                self._max_priority = pr
    def __len__(self):
        return len(self.buffer)

class LearningAgent:
    """Controller-compatible wrapper for a learned policy.

    Methods:
    - `select_action(info)` returns (cmd, subj, to) same as other controllers.
    - `observe(...)` can be used by external trainer to store experiences.
    """
    def __init__(self, model_path: Optional[str] = None, device: str = "cpu"):
        self.device = device
        self.net = None
        self.target_net = None
        # PER buffer
        self.replay = PrioritizedReplayBuffer()
        self.epsilon = 0.2
        self._train_steps = 0
        self.target_tau = 0.01  # soft update rate
        # n-step returns config (increase horizon for turtle games)
        self.n_step = 5
        self.gamma = 0.99
        self._nstep_queue: collections.deque = collections.deque()
        # gentle reward shaping magnitudes
        self.shaping_neutral_bonus = 0.05
        self.shaping_lv5_send_bonus = 0.03
        self.shaping_lv5_idle_penalty = 0.02
        # shaping toggles
        self.enable_shaping = True
        self.enable_idle_penalty = True
        if torch is not None:
            from tcg import config as cfg
            # input is state(6) + action(9) = 15 dims
            # Dueling network: split 6 state dims and 9 action dims
            self.net = QNetDueling(state_dim=6, action_dim=9).to(self.device)
            self.target_net = QNetDueling(state_dim=6, action_dim=9).to(self.device)
            if model_path is not None:
                try:
                    self.net.load_state_dict(torch.load(model_path, map_location=self.device))
                except Exception:
                    pass
            # initialize target with online weights
            self.target_net.load_state_dict(self.net.state_dict())
            self.target_net.eval()
        # debug counter
        self._debug_prints = 0

    def select_action(self, info) -> Tuple[int,int,int]:
        team, state, moving_pawns, spawning_pawns, done = info
        candidates = generate_action_candidates(state)
        if not candidates:
            return heuristic_fallback(state)
        state_vec = featurize_state(state)
        # if no model or explore, pick random
        if self.net is None or (torch is not None and random.random() < self.epsilon):
            cmd,s,t = random.choice(candidates)
            if not cfg.QUIET and self._debug_prints < 10:
                print(f"[RL] random action: {(cmd,s,t)} from {len(candidates)} candidates")
                self._debug_prints += 1
            return (cmd, s, t)
        best_val = None
        best_action = None
        vals = []
        with torch.no_grad():
            for (cmd,s,t) in candidates:
                act_vec = featurize_action(state, cmd, s, t)
                inp = np.concatenate([state_vec, act_vec]).astype(np.float32)
                x = torch.from_numpy(inp).float().to(self.device)
                val = self.net(x.unsqueeze(0)).item()
                vals.append(val)
                if best_val is None or val > best_val:
                    best_val = val
                    best_action = (cmd,s,t)
        # If network is indecisive (all nearly equal), use heuristic fallback
        if best_action is None or (len(vals) > 0 and (max(vals) - min(vals)) < 1e-5):
            fall = heuristic_fallback(state)
            if fall != (0,0,0):
                if not cfg.QUIET and self._debug_prints < 10:
                    print(f"[RL] heuristic fallback: {fall} (spread={0.0 if not vals else max(vals)-min(vals):.2e})")
                    self._debug_prints += 1
                return fall
            cmd,s,t = random.choice(candidates)
            if not cfg.QUIET and self._debug_prints < 10:
                print(f"[RL] random tie-break: {(cmd,s,t)}")
                self._debug_prints += 1
            return (cmd,s,t)
        if self._debug_prints < 10:
            if not cfg.QUIET:
                print(f"[RL] greedy action: {best_action} (spread={max(vals)-min(vals):.2e})")
            self._debug_prints += 1
        return best_action

    def observe(self, prev_state_vec, action_vec, reward, next_raw_state, done):
        """Store transition using n-step returns.

        We maintain a queue of recent steps and, when size >= n, push
        (s_t, a_t, R^{(n)}_t, s_{t+n}, done_{t+n}). On episode end, call
        `flush_nstep()` to emit remaining shorter-n transitions.
        """
        self._nstep_queue.append((prev_state_vec, action_vec, float(reward), next_raw_state, bool(done)))
        if len(self._nstep_queue) >= self.n_step:
            R = 0.0
            g = 1.0
            for i in range(self.n_step):
                R += g * float(self._nstep_queue[i][2])
                g *= self.gamma
            s_t, a_t = self._nstep_queue[0][0], self._nstep_queue[0][1]
            next_s_raw = self._nstep_queue[self.n_step - 1][3]
            done_n = self._nstep_queue[self.n_step - 1][4]
            self.replay.push((s_t, a_t, R, next_s_raw, done_n))
            self._nstep_queue.popleft()

    def flush_nstep(self):
        """Flush remaining queued transitions at episode end."""
        while len(self._nstep_queue) > 0:
            R = 0.0
            g = 1.0
            for i in range(len(self._nstep_queue)):
                R += g * float(self._nstep_queue[i][2])
                g *= self.gamma
            s_t, a_t = self._nstep_queue[0][0], self._nstep_queue[0][1]
            next_s_raw = self._nstep_queue[-1][3]
            done_n = self._nstep_queue[-1][4]
            self.replay.push((s_t, a_t, R, next_s_raw, done_n))
            self._nstep_queue.popleft()

    def shape_reward(self, prev_state_raw, action: Tuple[int,int,int], next_state_raw) -> float:
        """Gentle reward shaping to encourage cracking neutrals and timely Lv5 sends.

        - Add a small bonus when sending to an adjacent neutral, scaled by viability.
        - Add a small bonus when a Level 5 near-full source sends out to avoid idling.
        Magnitudes are deliberately modest.
        """
        try:
            if not getattr(self, 'enable_shaping', True):
                return 0.0
            cmd, s, t = action
            # Safety checks
            if not (0 <= s < len(prev_state_raw)) or not (0 <= t < len(prev_state_raw)):
                return 0.0
            s_team, s_kind, s_lvl, s_pawns, s_upg, s_neighbors = prev_state_raw[s]
            d_team, d_kind, d_lvl, d_pawns, d_upg, d_neighbors = prev_state_raw[t]
            bonus = 0.0
            # Neutral cracking bonus (only on move commands to neutral neighbors)
            if cmd == 1 and d_team == 0 and (t in s_neighbors):
                half_send = float(s_pawns // 2)
                dmg = 0.95 if s_kind == 1 else 0.65
                needed = float(d_pawns + d_lvl * 2 + 1)
                margin = (half_send * dmg) - needed
                # Viability scale in [0,1]
                scale = max(0.0, min(1.0, margin / max(1.0, needed)))
                bonus += self.shaping_neutral_bonus * scale
            # Timely Lv5 send bonus (avoid idling at near-full Lv5)
            if cmd == 1 and s_lvl == 5:
                from tcg.config import fortress_limit
                cap = float(fortress_limit[s_lvl])
                fill = float(s_pawns) / max(1.0, cap)
                if fill >= 0.90:
                    bonus += self.shaping_lv5_send_bonus
            # Small penalty when any near-full Lv5 has an adjacent neutral
            # and the chosen action does not send from such a Lv5 to that neutral.
            try:
                if not getattr(self, 'enable_idle_penalty', True):
                    return float(bonus)
                from tcg.config import fortress_limit
                has_candidate = False
                for i, f in enumerate(prev_state_raw):
                    team_i, kind_i, lvl_i, pawns_i, upg_i, neigh_i = f
                    if team_i != 1 or lvl_i != 5:
                        continue
                    cap_i = float(fortress_limit[lvl_i])
                    fill_i = float(pawns_i) / max(1.0, cap_i)
                    if fill_i >= 0.90 and any(prev_state_raw[n][0] == 0 for n in neigh_i):
                        has_candidate = True
                        break
                if has_candidate:
                    is_sending_lv5_to_neutral = (
                        cmd == 1 and s_lvl == 5 and d_team == 0 and (t in s_neighbors)
                    )
                    if not is_sending_lv5_to_neutral:
                        bonus -= self.shaping_lv5_idle_penalty
            except Exception:
                pass
            return float(bonus)
        except Exception:
            return 0.0

    def train_from_replay(self, epochs: int = 1, batch_size: int = 64, lr: float = 1e-3, gamma: float = 0.99):
        if torch is None or self.net is None or self.target_net is None:
            return
        # keep gamma consistent for n-step computation
        self.gamma = gamma
        opt = optim.Adam(self.net.parameters(), lr=lr)
        for _ in range(epochs):
            if len(self.replay) < batch_size:
                return
            idxs, batch, iw = self.replay.sample(batch_size)
            # current Q
            inp = torch.stack([torch.from_numpy(np.concatenate([x[0], x[1]]).astype(np.float32)) for x in batch]).to(self.device)
            pred_q = self.net(inp)
            # compute Double DQN target: r + gamma * Q_target(s', argmax_a Q_online(s',a))
            targets = []
            next_best_qs = []
            for (_, _, rwd, next_state_raw, done_flag) in batch:
                if done_flag:
                    targets.append(float(rwd))
                    next_best_qs.append(0.0)
                    continue
                next_candidates = generate_action_candidates(next_state_raw)
                if not next_candidates:
                    targets.append(float(rwd))
                    next_best_qs.append(0.0)
                    continue
                svec = featurize_state(next_state_raw)
                # argmax over online net
                best_idx = -1
                best_q_online = None
                with torch.no_grad():
                    for i, (cmd, ns, nt) in enumerate(next_candidates):
                        Avec = featurize_action(next_state_raw, cmd, ns, nt)
                        xin = torch.from_numpy(np.concatenate([svec, Avec]).astype(np.float32)).float().to(self.device)
                        q_online = self.net(xin.unsqueeze(0)).item()
                        if best_q_online is None or q_online > best_q_online:
                            best_q_online = q_online
                            best_idx = i
                # evaluate chosen action with target net
                with torch.no_grad():
                    cmd, ns, nt = next_candidates[best_idx]
                    Avec = featurize_action(next_state_raw, cmd, ns, nt)
                    xin = torch.from_numpy(np.concatenate([svec, Avec]).astype(np.float32)).float().to(self.device)
                    q_target = self.target_net(xin.unsqueeze(0)).item()
                targets.append(float(rwd) + gamma * float(q_target))
                next_best_qs.append(float(q_target))
            tgt = torch.tensor(targets, dtype=torch.float32).to(self.device)
            # importance-weighted MSE
            w = torch.from_numpy(iw).to(self.device)
            loss = ((pred_q - tgt) ** 2 * w).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
            # update PER priorities using absolute TD error
            td_err = (pred_q.detach() - tgt).cpu().numpy()
            self.replay.update_priorities(idxs, td_err)
            # soft update target network
            with torch.no_grad():
                for tp, p in zip(self.target_net.parameters(), self.net.parameters()):
                    tp.data.copy_(tp.data * (1.0 - self.target_tau) + p.data * self.target_tau)
            self._train_steps += 1

    def save(self, path: str):
        if torch is None or self.net is None:
            return
        torch.save(self.net.state_dict(), path)
