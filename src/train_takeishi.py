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

def choose_opponent(weights=None):
    # weighted sampling to see Claude more often while keeping diversity
    pool = [RandomPlayer, ClaudePlayer, DefensiveEconomist]
    # default bias: increase Claude exposure (0.65) with some diversity
    default_weights = [0.15, 0.65, 0.20]
    w = default_weights if weights is None else list(weights)
    return random.choices(pool, weights=w, k=1)[0]

def run(n_episodes: int = 100, save_every: int = 50, epsilon_min: float = 0.02, tau: float = 0.01, opponent_weights=None):
    agent = LearningAgent()
    # allow tuning target network soft-update rate
    agent.target_tau = tau
    for ep in range(1, n_episodes+1):
        Opp = choose_opponent(opponent_weights)
        env = TCGEnv(Opp)
        obs, _ = env.reset()
        done = False
        truncated = False
        steps = 0
        # small per-episode epsilon decay with configurable floor
        agent.epsilon = max(epsilon_min, agent.epsilon * 0.995)
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
            # build action feature vector (supports upgrade and move)
            cmd, s, t = action
            act_feat = featurize_action(raw_state, cmd, s, t)
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
