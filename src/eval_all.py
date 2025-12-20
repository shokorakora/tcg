r"""
Batch evaluation for Takeishi LearningAgent across opponents.
Usage:
  .venv\Scripts\Activate.ps1
  python src\eval_all.py --model models\takeishi_final.pt --episodes 200 --window False
"""
import argparse
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

def eval_vs(opponent_name: str, episodes: int, model: str, window: bool):
    wins = 0
    for i in range(episodes):
        agent = LearningAgent(model_path=model)
        agent.epsilon = 0.0
        blue = LearningController(agent)
        if opponent_name == "claude":
            red = ClaudePlayer()
        elif opponent_name == "random":
            red = RandomPlayer()
        elif opponent_name == "economist":
            red = DefensiveEconomist()
        else:
            raise ValueError(f"Unknown opponent: {opponent_name}")
        g = Game(blue, red, window=window)
        g.run()
        if g.win_team == "Blue":
            wins += 1
    print(f"Opponent={opponent_name} Summary: wins={wins}/{episodes}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", type=str, default="models/takeishi_final.pt")
    ap.add_argument("--episodes", type=int, default=200)
    ap.add_argument("--window", type=str, default="False")
    args = ap.parse_args()
    window = (args.window.lower() == "true")

    for opp in ["claude", "economist", "random"]:
        eval_vs(opp, args.episodes, args.model, window)

if __name__ == "__main__":
    main()
