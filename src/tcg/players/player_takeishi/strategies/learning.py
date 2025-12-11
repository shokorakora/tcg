from typing import List, Tuple, Dict
import random

Action = Tuple[int, int, int]  # (command, subject, to)

class LearningPlayer:
    """
    Q学習の簡易枠組み（行動は (command, subject, to) で扱う）。
    - 0: 何もしない -> (0, 0, 0)
    - 1: 部隊移動 -> (1, from_fortress, to_fortress) ただし to は隣接のみ
    - 2: アップグレード -> (2, fortress_id, 0)
    """

    def __init__(self):
        self.q_table: Dict[Tuple, Dict[Action, float]] = {}  # 状態 -> {行動: Q値}
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.exploration_rate = 1.0
        self.exploration_decay = 0.995
        self.min_exploration_rate = 0.05

    # ---- 公開API想定（ゲームのupdateから呼ぶ用） ----
    def select_action(self, info) -> Action:
        """
        info = (team, state, moving_pawns, spawning_pawns, done)
        """
        team, state, moving_pawns, spawning_pawns, done = info
        state_key = self._state_key(state)
        actions = self._legal_actions(state)

        # 探索
        if random.random() < self.exploration_rate:
            return random.choice(actions)

        # 利用
        return self._best_action(state_key, actions)

    def observe(self, prev_state, action: Action, reward: float, next_state):
        """
        学習更新（環境から報酬と次状態を受け取ったときに呼ぶ）
        """
        s_key = self._state_key(prev_state)
        ns_key = self._state_key(next_state)

        current_q = self._get_q(s_key, action)
        next_best_q = self._best_q(ns_key)

        new_q = (1 - self.learning_rate) * current_q + self.learning_rate * (reward + self.discount_factor * next_best_q)
        self._set_q(s_key, action, new_q)

        # ε減衰
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)

    # ---- 内部ヘルパー ----
    def _state_key(self, state: List[List[int]]) -> Tuple:
        """
        Qテーブル用の軽量キーを作る（teamはすでに自分視点=1で渡ってくる想定）
        形式: 各要塞につき (team, level, pawn_number, upgrade_time) のタプル列
        """
        return tuple((f[0], f[2], f[3], f[4]) for f in state)

    def _legal_actions(self, state: List[List[int]]) -> List[Action]:
        actions: List[Action] = []

        # 何もしない
        actions.append((0, 0, 0))

        # アップグレード候補（自軍、upgrade_time==0、兵数>=上限の半分）
        fortress_limit = [10, 10, 20, 30, 40, 50]
        for i in range(len(state)):
            team, _, level, pawn_number, upgrade_time, _ = state[i]
            if team == 1 and upgrade_time == 0 and pawn_number >= fortress_limit[level] // 2:
                actions.append((2, i, 0))

        # 移動候補（自軍から隣接へ）
        for i in range(len(state)):
            team, _, _, pawn_number, _, neighbors = state[i]
            if team != 1 or pawn_number <= 1:
                continue
            for n in neighbors:
                # subject=i から to=n へ
                actions.append((1, i, n))

        return actions if actions else [(0, 0, 0)]

    def _best_action(self, state_key: Tuple, actions: List[Action]) -> Action:
        # 未学習状態ならランダム
        if state_key not in self.q_table:
            return random.choice(actions)
        qdict = self.q_table[state_key]
        # 候補にない行動は0扱いで比較
        return max(actions, key=lambda a: qdict.get(a, 0.0))

    def _best_q(self, state_key: Tuple) -> float:
        qdict = self.q_table.get(state_key)
        if not qdict:
            return 0.0
        return max(qdict.values()) if qdict else 0.0

    def _get_q(self, state_key: Tuple, action: Action) -> float:
        qdict = self.q_table.get(state_key)
        if not qdict:
            return 0.0
        return qdict.get(action, 0.0)

    def _set_q(self, state_key: Tuple, action: Action, value: float):
        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        self.q_table[state_key][action] = value

    # ---- オフライン学習用（任意） ----
    def train_episode(self, env_step, reward_fn, max_steps: int = 200):
        """
        環境ステップ関数と報酬関数を渡して1エピソード分学習する簡易ループ。
        - env_step(action) -> (next_state, done) を想定
        - reward_fn(prev_state, action, next_state) -> float を想定
        """
        # 初期状態は呼び出し側で用意して、最初の env_step(None) などで返す設計でもOK
        # ここでは簡易に呼び出し側が最初に外から state を与える前提にする
        raise NotImplementedError("train_episode は、ゲーム環境に合わせて呼び出し側で実装してください。")