import pygame

from tcg.game import Game
from tcg.players.sample_random import RandomPlayer
from tcg.players.claude_player import ClaudePlayer

if __name__ == "__main__":
    # ClaudePlayer vs RandomPlayer で対戦
    print("=== ClaudePlayer (Blue) vs RandomPlayer (Red) ===")

    # デフォルト: ウィンドウ表示あり
    Game(ClaudePlayer(), RandomPlayer()).run()

    # ウィンドウ表示なし（高速実行）の場合:
    #Game(ClaudePlayer(), RandomPlayer(), window=False).run()

    pygame.quit()
