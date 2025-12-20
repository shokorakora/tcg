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
    # 0) Upgrades where possible
    for s in my_forts:
        team, kind, lvl, pawns, upg, _ = state[s]
        # upgrade possible: enough pawns, not already upgrading, level 1..4
        # fortress_limit index by level
        from tcg.config import fortress_limit
        if upg == -1 and 1 <= lvl <= 4 and pawns >= fortress_limit[lvl] // 2:
            candidates.append((2, s, s))
    # 1) Feasible expansions and attacks from owned forts
    for s in my_forts:
        pawns = state[s][3]
        if pawns < 2:
            continue
        half_send = pawns // 2
        for n in state[s][5]:
            d_team, _, d_lvl, d_pawns, _, _ = state[n]
            needed = d_pawns + d_lvl * 2 + 1
            if half_send < needed:
                continue
            if d_team == 0:
                candidates.append((1, s, n))
            elif d_team != 1:
                candidates.append((1, s, n))
    # 2) Concentrates toward a frontline if no feasible attack/capture
    frontlines = [f for f in my_forts if any(state[n][0] != 1 for n in state[f][5])]
    if frontlines:
        for s in my_forts:
            if s not in frontlines and state[s][3] >= 2:
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

class ReplayBuffer:
    def __init__(self, capacity: int = 20000):
        self.buffer = collections.deque(maxlen=capacity)
    def push(self, experience):
        self.buffer.append(experience)
    def sample(self, batch_size: int):
        batch = random.sample(self.buffer, batch_size)
        return batch
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
        self.replay = ReplayBuffer()
        self.epsilon = 0.2
        self._train_steps = 0
        self.target_tau = 0.01  # soft update rate
        if torch is not None:
            from tcg import config as cfg
            # input is state(6) + action(9) = 15 dims
            self.net = QNet(inp_dim=15).to(self.device)
            self.target_net = QNet(inp_dim=15).to(self.device)
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
        # store for replay (keep next raw state to compute max_a' Q(s',a'))
        self.replay.push((prev_state_vec, action_vec, reward, next_raw_state, done))

    def train_from_replay(self, epochs: int = 1, batch_size: int = 64, lr: float = 1e-3, gamma: float = 0.99):
        if torch is None or self.net is None or self.target_net is None:
            return
        opt = optim.Adam(self.net.parameters(), lr=lr)
        for _ in range(epochs):
            if len(self.replay) < batch_size:
                return
            batch = self.replay.sample(batch_size)
            # current Q
            inp = torch.stack([torch.from_numpy(np.concatenate([x[0], x[1]]).astype(np.float32)) for x in batch]).to(self.device)
            pred_q = self.net(inp)
            # compute target = r + gamma * max_a' Q(s',a')
            targets = []
            for (_, _, rwd, next_state_raw, done_flag) in batch:
                if done_flag:
                    targets.append(float(rwd))
                    continue
                # max over next candidates
                next_candidates = generate_action_candidates(next_state_raw)
                if not next_candidates:
                    targets.append(float(rwd))
                    continue
                svec = featurize_state(next_state_raw)
                best_val = None
                with torch.no_grad():
                    for (cmd, ns, nt) in next_candidates:
                        Avec = featurize_action(next_state_raw, cmd, ns, nt)
                        xin = torch.from_numpy(np.concatenate([svec, Avec]).astype(np.float32)).float().to(self.device)
                        q = self.target_net(xin.unsqueeze(0)).item()
                        if best_val is None or q > best_val:
                            best_val = q
                next_q = 0.0 if best_val is None else float(best_val)
                targets.append(float(rwd) + gamma * next_q)
            tgt = torch.tensor(targets, dtype=torch.float32).to(self.device)
            loss = nn.functional.mse_loss(pred_q, tgt)
            opt.zero_grad()
            loss.backward()
            opt.step()
            # soft update target network
            with torch.no_grad():
                for tp, p in zip(self.target_net.parameters(), self.net.parameters()):
                    tp.data.copy_(tp.data * (1.0 - self.target_tau) + p.data * self.target_tau)
            self._train_steps += 1

    def save(self, path: str):
        if torch is None or self.net is None:
            return
        torch.save(self.net.state_dict(), path)
