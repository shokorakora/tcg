import pygame

from tcg.game import Game
from tcg.players.sample_random import RandomPlayer
from tcg.players.strategy_economist import DefensiveEconomist
from tcg.players.claude_player import ClaudePlayer
from tcg.players.player_takeishi import TakeishiPlayer
from tcg.players.players_kishida.ml_player import MLPlayer

if __name__ == "__main__":
    # Blue vs Red で対戦
    print("=== TakeishiPlayer (Blue) vs ClaudePlayer (Red) ===")

    # デフォルト: ウィンドウ表示あり
    #Game(TakeishiPlayer(), ClaudePlayer()).run()

    # ウィンドウ表示なし（高速実行）の場合:
    Game(TakeishiPlayer(), ClaudePlayer(), window=False).run()

    pygame.quit()
