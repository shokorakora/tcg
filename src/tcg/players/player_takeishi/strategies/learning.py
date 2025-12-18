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

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
except Exception:
    torch = None

# State featurizer
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
    vec = [my_pawns, en_pawns, my_count, en_count]
    vec.append(my_level / max(1, my_count))
    vec.append(en_level / max(1, en_count))
    return np.array(vec, dtype=np.float32)

# Candidate actions generator (src, target)
def generate_action_candidates(state) -> List[Tuple[int,int]]:
    my_forts = [i for i,f in enumerate(state) if f[0] == 1]
    if not my_forts:
        return []
    candidates = []
    # expansions and attacks from owned forts
    for s in my_forts:
        pawns = state[s][3]
        if pawns < 2:
            continue
        for n in state[s][5]:
            if state[n][0] == 0:
                candidates.append((s,n))
            elif state[n][0] != 1:
                candidates.append((s,n))
    # concentrates
    frontlines = [f for f in my_forts if any(state[n][0] != 1 for n in state[f][5])]
    if frontlines:
        for s in my_forts:
            if s not in frontlines and state[s][3] >= 2:
                candidates.append((s, frontlines[0]))
    # dedupe while preserving order
    seen = set()
    out = []
    for a in candidates:
        if a not in seen:
            seen.add(a)
            out.append(a)
    return out

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
        self.replay = ReplayBuffer()
        self.epsilon = 0.2
        if torch is not None:
            self.net = QNet(inp_dim=6).to(self.device)
            if model_path is not None:
                try:
                    self.net.load_state_dict(torch.load(model_path, map_location=self.device))
                except Exception:
                    pass

    def select_action(self, info) -> Tuple[int,int,int]:
        team, state, moving_pawns, spawning_pawns, done = info
        candidates = generate_action_candidates(state)
        if not candidates:
            return (0,0,0)
        state_vec = featurize_state(state)
        # if no model, random
        if self.net is None or torch is None or random.random() < self.epsilon:
            s,t = random.choice(candidates)
            return (1, s, t)
        st = torch.from_numpy(state_vec).float().to(self.device)
        best_val = None
        best_action = None
        with torch.no_grad():
            for (s,t) in candidates:
                # for simplicity, evaluate same state vector; action-specific features not used
                val = self.net(st.unsqueeze(0)).item()
                if best_val is None or val > best_val:
                    best_val = val
                    best_action = (s,t)
        if best_action is None:
            s,t = random.choice(candidates)
            return (1,s,t)
        return (1, best_action[0], best_action[1])

    def observe(self, prev_state_vec, action, reward, next_state_vec, done):
        # store for replay; agent does not train here (trainer will sample replay)
        self.replay.push((prev_state_vec, action, reward, next_state_vec, done))

    def train_from_replay(self, epochs: int = 1, batch_size: int = 64, lr: float = 1e-3, gamma: float = 0.99):
        if torch is None or self.net is None:
            return
        opt = optim.Adam(self.net.parameters(), lr=lr)
        for _ in range(epochs):
            if len(self.replay) < batch_size:
                return
            batch = self.replay.sample(batch_size)
            st = torch.stack([torch.from_numpy(x[0]).float() for x in batch]).to(self.device)
            r = torch.tensor([x[2] for x in batch], dtype=torch.float32).to(self.device)
            pred = self.net(st)
            loss = nn.functional.mse_loss(pred, r)
            opt.zero_grad()
            loss.backward()
            opt.step()

    def save(self, path: str):
        if torch is None or self.net is None:
            return
        torch.save(self.net.state_dict(), path)
