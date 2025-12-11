from tcg.players.player_takeishi.models.policy import Policy

def test_policy_decision_making():
    # Create a mock game state for testing
    mock_state = {
        'team': 1,
        'state': [
            [1, 'fortress', 1, 15, 0, [1, 2]],  # Our fortress
            [2, 'fortress', 1, 5, 0, [0, 3]],   # Enemy fortress
            [0, 'fortress', 1, 10, 0, [0, 1]],  # Neutral fortress
        ],
        'moving_pawns': [],
        'spawning_pawns': [],
        'done': False
    }

    policy = Policy()

    # Test decision making for attacking an enemy fortress
    command, subject, to = policy.decide(mock_state)
    assert command == 1  # Expecting an attack command
    assert subject == 0  # Our fortress
    assert to == 1      # Enemy fortress

def test_policy_upgrade_decision():
    # Create a mock game state for testing
    mock_state = {
        'team': 1,
        'state': [
            [1, 'fortress', 1, 20, 0, []],  # Our fortress ready for upgrade
            [2, 'fortress', 1, 5, 0, []],   # Enemy fortress
        ],
        'moving_pawns': [],
        'spawning_pawns': [],
        'done': False
    }

    policy = Policy()

    # Test decision making for upgrading a fortress
    command, subject, to = policy.decide(mock_state)
    assert command == 2  # Expecting an upgrade command
    assert subject == 0  # Our fortress
    assert to == 0      # Upgrade action does not require a target

def test_policy_no_action():
    # Create a mock game state for testing
    mock_state = {
        'team': 1,
        'state': [
            [1, 'fortress', 1, 5, 0, []],  # Our fortress with insufficient troops
            [2, 'fortress', 1, 5, 0, []],  # Enemy fortress
        ],
        'moving_pawns': [],
        'spawning_pawns': [],
        'done': False
    }

    policy = Policy()

    # Test decision making for no action
    command, subject, to = policy.decide(mock_state)
    assert command == 0  # Expecting no action
    assert subject == 0  # No specific fortress
    assert to == 0      # No target needed