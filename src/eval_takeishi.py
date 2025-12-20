r"""
Evaluate a saved Takeishi LearningAgent model vs ClaudePlayer.
Usage:
  .venv\Scripts\Activate.ps1
  python src\eval_takeishi.py --model models\takeishi_final.pt --episodes 10 --window False
"""
import argparse
from tcg import config as cfg
from tcg.game import Game
from tcg.controller import Controller
from tcg.players.claude_player import ClaudePlayer
from tcg.players.sample_random import RandomPlayer
from tcg.players.strategy_economist import DefensiveEconomist
from tcg.players.player_takeishi.strategies.learning import LearningAgent

class LearningController(Controller):
    def __init__(self, agent: LearningAgent):
        super().__init__()
        self.agent = agent
    def team_name(self) -> str:
        return "TakeishiRL"
    def update(self, info):
        return self.agent.select_action(info)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", type=str, default="models/takeishi_final.pt")
    ap.add_argument("--episodes", type=int, default=10)
    ap.add_argument("--window", type=str, default="False")
    ap.add_argument("--opponent", type=str, default="claude", choices=["claude","random","economist"]) 
    ap.add_argument("--quiet", type=str, default="True")
    args = ap.parse_args()
    window = (args.window.lower() == "true")
    cfg.QUIET = (args.quiet.lower() == "true")

    wins = 0
    for i in range(args.episodes):
        agent = LearningAgent(model_path=args.model)
        # deterministic evaluation
        agent.epsilon = 0.0
        blue = LearningController(agent)
        if args.opponent == "claude":
            red = ClaudePlayer()
        elif args.opponent == "random":
            red = RandomPlayer()
        else:
            red = DefensiveEconomist()
        g = Game(blue, red, window=window)
        g.run()
        print(f"Episode {i+1}: winner={g.win_team}")
        if g.win_team == "Blue":
            wins += 1
    print(f"Summary: wins={wins}/{args.episodes}")

if __name__ == "__main__":
    main()
