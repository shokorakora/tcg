r"""
Batch evaluation for Takeishi LearningAgent across multiple opponents.
Usage:
    .venv\Scripts\Activate.ps1
    python src\eval_all.py --model models\takeishi_final.pt --episodes 300 --window False \
        --opponents claude,economist,random,splitpush,harasser,bulwark
"""
import argparse
from datetime import datetime
import os
from tcg.game import Game
from tcg.controller import Controller
from tcg.players.claude_player import ClaudePlayer
from tcg.players.sample_random import RandomPlayer
from tcg.players.strategy_economist import DefensiveEconomist
from tcg.players.strategy_splitpush import SplitPusher
from tcg.players.strategy_harasser import Harasser
from tcg.players.strategy_bulwark import Bulwark
from tcg.players.strategy_anchor import Anchor
from tcg.players.strategy_feeder import Feeder
from tcg.players.strategy_rusher import Rusher
from tcg.players.strategy_opportunist import Opportunist
from tcg.players.strategy_counter import Counter
from tcg.players.strategy_flow import Flow
from tcg.players.player_takeishi.strategies.learning import LearningAgent
from tcg import config as cfg

class LearningController(Controller):
    def __init__(self, agent: LearningAgent):
        super().__init__()
        self.agent = agent
    def team_name(self) -> str:
        return "TakeishiRL"
    def update(self, info):
        return self.agent.select_action(info)

OPPONENTS = {
    "claude": ClaudePlayer,
    "economist": DefensiveEconomist,
    "random": RandomPlayer,
    "splitpush": SplitPusher,
    "harasser": Harasser,
    "bulwark": Bulwark,
    "anchor": Anchor,
    "feeder": Feeder,
    "rusher": Rusher,
    "opportunist": Opportunist,
    "counter": Counter,
    "flow": Flow,
}

def eval_vs(opponent_name: str, episodes: int, model: str, window: bool, results_path: str | None = None):
    wins = 0
    for i in range(episodes):
        agent = LearningAgent(model_path=model)
        agent.epsilon = 0.0
        blue = LearningController(agent)
        Opp = OPPONENTS.get(opponent_name)
        if Opp is None:
            raise ValueError(f"Unknown opponent: {opponent_name}. Options: {', '.join(OPPONENTS.keys())}")
        red = Opp()
        g = Game(blue, red, window=window)
        g.run()
        if g.win_team == "Blue":
            wins += 1
    summary = f"Opponent={opponent_name} Summary: wins={wins}/{episodes}"
    print(summary)
    if results_path:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] model={model} episodes={episodes} {summary}\n"
        with open(results_path, "a", encoding="utf-8") as f:
            f.write(line)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", type=str, default="models/takeishi_final.pt")
    ap.add_argument("--episodes", type=int, default=300)
    ap.add_argument("--window", type=str, default="False")
    ap.add_argument("--opponents", type=str, default=",".join(OPPONENTS.keys()))
    ap.add_argument("--quiet", type=str, default="True")
    ap.add_argument("--save-results", type=str, default="True")
    args = ap.parse_args()
    window = (args.window.lower() == "true")
    cfg.QUIET = (args.quiet.lower() == "true")
    results_path = None
    if args.save_results.lower() == "true":
        # default daily results file under models/
        results_path = os.path.join("models", "eval_results_2025-12-20.md")

    opps = [o.strip().lower() for o in args.opponents.split(",") if o.strip()]
    for opp in opps:
        eval_vs(opp, args.episodes, args.model, window, results_path)

if __name__ == "__main__":
    main()
