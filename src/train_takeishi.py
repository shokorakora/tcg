r"""
Minimal training runner for Takeishi LearningAgent using TCGEnv.

Usage:
  .venv\Scripts\Activate.ps1
  python src\train_takeishi.py

This script runs episodes against a sampled opponent from the pool and
trains the LearningAgent from collected experiences.
"""
from tcg.gym_env import TCGEnv
from tcg.players.sample_random import RandomPlayer
from tcg.players.claude_player import ClaudePlayer
from tcg.players.strategy_economist import DefensiveEconomist
from tcg.players.player_takeishi.strategies.learning import LearningAgent, featurize_state, featurize_action, generate_action_candidates
import random
import numpy as np
import os

def choose_opponent():
    # simple opponent pool
    pool = [RandomPlayer, ClaudePlayer, DefensiveEconomist]
    return random.choice(pool)

def run(n_episodes: int = 100, save_every: int = 50):
    agent = LearningAgent()
    for ep in range(1, n_episodes+1):
        Opp = choose_opponent()
        env = TCGEnv(Opp)
        obs, _ = env.reset()
        done = False
        truncated = False
        steps = 0
        # small per-episode epsilon decay
        agent.epsilon = max(0.05, agent.epsilon * 0.995)
        while not (done or truncated):
            # access raw state from env.game
            raw_state = env.game.state
            moving = env.game.moving_pawns
            spawning = getattr(env.game, 'spawning_pawns', [])
            info = (1, raw_state, moving, spawning, False)
            # select action via agent
            action = agent.select_action(info)
            # perform env step
            obs2, reward, done, truncated, info2 = env.step(action)
            next_raw_state = env.game.state
            # observe
            cur_feat = featurize_state(raw_state)
            # build action feature vector
            cmd, s, t = action
            act_feat = featurize_action(raw_state, s, t) if cmd == 1 else np.zeros(9, dtype=np.float32)
            agent.observe(cur_feat, act_feat, reward, next_raw_state, done)
            steps += 1
            # training step every 32 samples
            if len(agent.replay) >= 64:
                agent.train_from_replay(epochs=1, batch_size=64)
        print(f"Episode {ep} finished steps={steps} done={done} truncated={truncated} epsilon={agent.epsilon:.3f}")
        if ep % save_every == 0:
            os.makedirs("models", exist_ok=True)
            agent.save(f"models/takeishi_ep{ep}.pt")
    # final save
    os.makedirs("models", exist_ok=True)
    agent.save("models/takeishi_final.pt")

if __name__ == '__main__':
    run()
