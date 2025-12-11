from typing import List, Tuple
import random

class LearningPlayer:
    """
    AIプレイヤーの学習戦略モデルを定義するファイル
    """

    def __init__(self):
        self.q_table = {}  # 各行動のQ値を格納するテーブル
        self.learning_rate = 0.1  # 学習率
        self.discount_factor = 0.9  # 割引率
        self.exploration_rate = 1.0  # 探索率 (ε-greedy戦略用)
        self.exploration_decay = 0.99  # 探索率の減衰率 (ε-greedy戦略用)　更新ごとにεを減衰
        self.min_exploration_rate = 0.1  # 最小探索率 (ε-greedy戦略用)　εの下限値(完全に探索をやめないために設定)
    def choose_action(self, state: Tuple) -> int:
        """
       ε-greedy戦略に基づいて行動を選択する
        引数:
            state: ゲームの現在の状態

        返り値:
            int: 選択された行動
        """
        if random.uniform(0, 1) < self.exploration_rate: #0~1の一様乱数が探索率(ε)未満なら探索(ランダム行動)
            return random.choice([0, 1, 2])  # 探索: ランダムに行動を選択
        else:
            return self.best_action(state)  # 利用: Q値テーブルに基づいて最良の行動を選択

    def best_action(self, state: Tuple) -> int:
        """
        Q値テーブルに基づいて最良の行動を選択する

        引数:
            state: ゲームの現在の状態

        返り値:
            int: 最良の行動
        """

        # Q値が最大の行動を返す
        return max(self.q_table.get(state, {0: 0, 1: 0, 2: 0}), key=self.q_table.get(state, {0: 0, 1: 0, 2: 0}).get)

    def update_q_table(self, state: Tuple, action: int, reward: float, next_state: Tuple):
        """
        Q値テーブルを更新する

        引数:
            state: 直前のゲームの状態
            action: 取った行動
            reward: 行動後に得られた報酬
            next_state: 行動後の新しいゲームの状態
        """
        current_q = self.q_table.get(state, {0: 0, 1: 0, 2: 0}).get(action, 0)
        max_future_q = max(self.q_table.get(next_state, {0: 0, 1: 0, 2: 0}).values())
        new_q = (1 - self.learning_rate) * current_q + self.learning_rate * (reward + self.discount_factor * max_future_q)
        
        if state not in self.q_table:
            self.q_table[state] = {0: 0, 1: 0, 2: 0}
        self.q_table[state][action] = new_q

        # Decay exploration rate
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)

    def reset(self):
        """
       学習パラメータやQ値テーブルをリセットする
        """
        self.q_table.clear()
        self.exploration_rate = 1.0

    def train(self, episodes: int):
        """
        エピソード数を与えて学習を実行する

        引数:
            episodes: 学習エピソード数
        """
        for episode in range(episodes):
            state = self.reset_game()  # 各エピソードの開始にゲームをリセットして初期状態を取得
            done = False # エピソード終了フラグ
            
            while not done: # エピソードが終了するまでループ
                action = self.choose_action(state)
                next_state, reward, done = self.take_action(action)  # Implement this method to take action in the game
                self.update_q_table(state, action, reward, next_state)
                state = next_state

    def reset_game(self) -> Tuple:
        """
        状態を初期化して初期状態を返す

        返り値:
            Tuple: ゲームの初期状態
        """
        # Implement the logic to reset the game and return the initial state
        pass

    def take_action(self, action: int) -> Tuple[Tuple, float, bool]:
        """
       指定した行動を適用して、次の状態、報酬、終了フラグを返す
        引数:
            action: 取る行動

        返り値:
            Tuple[Tuple, float, bool]: 次の状態、報酬、終了フラグ
        """
        # Implement the logic to take action and return the next state, reward, and done flag
        pass