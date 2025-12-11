from tcg.players.player_takeishi.strategies.heuristic import evaluate_game_state

def test_evaluate_game_state():
    # Test case 1: Basic game state with clear winning move
    game_state = (
        1,  # team
        [[1, 0, 1, 10, 0, [1, 2]],  # fortress 0
         [2, 0, 1, 5, 0, [0, 3]],   # fortress 1
         [0, 0, 1, 0, 0, [0, 1]],   # fortress 2
         [0, 0, 1, 0, 0, [0, 1]],   # fortress 3
         [1, 0, 1, 15, 0, [5]],      # fortress 4
         [0, 0, 1, 0, 0, [0, 1]],   # fortress 5
         [0, 0, 1, 0, 0, [0, 1]],   # fortress 6
         [0, 0, 1, 0, 0, [0, 1]],   # fortress 7
         [0, 0, 1, 0, 0, [0, 1]],   # fortress 8
         [0, 0, 1, 0, 0, [0, 1]],   # fortress 9
         [0, 0, 1, 0, 0, [0, 1]],   # fortress 10
         [0, 0, 1, 0, 0, [0, 1]]]   # fortress 11
    )
    result = evaluate_game_state(game_state)
    assert result == expected_result_1, f"Expected {expected_result_1}, got {result}"

    # Test case 2: Game state with no available moves
    game_state = (
        1,
        [[1, 0, 1, 0, 0, [1, 2]],  # fortress 0
         [1, 0, 1, 0, 0, [0, 3]],  # fortress 1
         [1, 0, 1, 0, 0, [0, 1]],  # fortress 2
         [1, 0, 1, 0, 0, [0, 1]],  # fortress 3
         [1, 0, 1, 0, 0, [5]],     # fortress 4
         [1, 0, 1, 0, 0, [0, 1]],  # fortress 5
         [1, 0, 1, 0, 0, [0, 1]],  # fortress 6
         [1, 0, 1, 0, 0, [0, 1]],  # fortress 7
         [1, 0, 1, 0, 0, [0, 1]],  # fortress 8
         [1, 0, 1, 0, 0, [0, 1]],  # fortress 9
         [1, 0, 1, 0, 0, [0, 1]],  # fortress 10
         [1, 0, 1, 0, 0, [0, 1]]]  # fortress 11
    )
    result = evaluate_game_state(game_state)
    assert result == expected_result_2, f"Expected {expected_result_2}, got {result}"

    # Additional test cases can be added here

if __name__ == "__main__":
    test_evaluate_game_state()
    print("All tests passed!")