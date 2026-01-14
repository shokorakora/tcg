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
}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--opponent", type=str, default="claude", choices=list(OPTS.keys()))
    ap.add_argument("--window", type=str, default="True")
    ap.add_argument("--blue", type=str, default="takeishi", choices=["takeishi", "rl"])
    ap.add_argument("--model", type=str, default="models/takeishi_final.pt")
    args = ap.parse_args()
    window = (args.window.lower() == "true")

    RedClass = OPTS.get(args.opponent, ClaudePlayer)
    red = RedClass()
    if args.blue == "rl":
        blue = RLPlayer(model_path=args.model, epsilon=0.0)
    else:
        blue = TakeishiPlayer()
    print(f"=== {blue.team_name()} (Blue) vs {red.team_name()} (Red) ===")

    Game(blue, red, window=window).run()
    pygame.quit()
