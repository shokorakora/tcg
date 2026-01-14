import argparse
import pygame

from tcg.game import Game
from tcg.players.sample_random import RandomPlayer
from tcg.players.strategy_economist import DefensiveEconomist
from tcg.players.claude_player import ClaudePlayer
from tcg.players.player_takeishi import TakeishiPlayer
from tcg.players.strategy_splitpush import SplitPusher
from tcg.players.strategy_harasser import Harasser
from tcg.players.strategy_bulwark import Bulwark
from tcg.players.strategy_anchor import Anchor
from tcg.players.strategy_feeder import Feeder
from tcg.players.strategy_rusher import Rusher
from tcg.players.strategy_opportunist import Opportunist
from tcg.players.strategy_counter import Counter
from tcg.players.strategy_flow import Flow
from tcg.players.player_rl import RLPlayer
from tcg.players.player_ONCT import ONCT
from tcg.players.player_shota import ShotaPlayer

# Built-in player map (non-RL, non-Takeishi)
OPTS = {
    "claude": ClaudePlayer,
    "random": RandomPlayer,
    "economist": DefensiveEconomist,
    "splitpush": SplitPusher,
    "harasser": Harasser,
    "bulwark": Bulwark,
    "anchor": Anchor,
    "feeder": Feeder,
    "rusher": Rusher,
    "opportunist": Opportunist,
    "counter": Counter,
    "flow": Flow,
    "onct": ONCT,
    "shota": ShotaPlayer,
}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    # Backward-compat opponent flag (used if --red not provided)
    ap.add_argument("--opponent", type=str, default="claude", choices=list(OPTS.keys()))
    ap.add_argument("--window", type=str, default="True")
    # Flexible side selection: allow any named player, plus 'takeishi' and 'rl'
    player_choices = list(OPTS.keys()) + ["takeishi", "rl"]
    ap.add_argument("--blue", type=str, default="takeishi", choices=player_choices)
    ap.add_argument("--red", type=str, default="", choices=player_choices + [""])
    # Model path for RL
    ap.add_argument("--model", type=str, default="models/takeishi_final.pt")
    args = ap.parse_args()
    window = (args.window.lower() == "true")

    def make_player(name: str):
        if name == "rl":
            return RLPlayer(model_path=args.model, epsilon=0.0)
        if name == "takeishi":
            return TakeishiPlayer()
        cls = OPTS.get(name)
        if cls is None:
            raise ValueError(f"Unknown player: {name}")
        return cls()

    # Determine red side: prefer --red, fallback to --opponent
    red_name = args.red if args.red else args.opponent
    red = make_player(red_name)
    blue = make_player(args.blue)
    print(f"=== {blue.team_name()} (Blue) vs {red.team_name()} (Red) ===")

    Game(blue, red, window=window).run()
    pygame.quit()
