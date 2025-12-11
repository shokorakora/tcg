from tcg.controller import Controller
from tcg.players.player_takeishi.strategies.heuristic import heuristic_strategy
# from tcg.players.player_takeishi.strategies.learning import LearningStrategy
# from tcg.players.player_takeishi.models.policy import PolicyModel

class TakeishiPlayer(Controller):
    """
    Takeishi AI Player

    This class implements a strong AI player using heuristic and learning strategies.
    """

    def __init__(self) -> None:
        super().__init__()
        self.step = 0
        # self.heuristic_strategy = HeuristicStrategy()
        # self.learning_strategy = LearningStrategy()
        # self.policy_model = PolicyModel()

    def team_name(self) -> str:
        """
        Returns the player name for tournament display.

        Returns:
            str: Player name
        """
        return "TakeishiAI"

    def update(self, info) -> tuple[int, int, int]:
        """
        Called every step to update the player's strategy based on game information.

        Args:
            info: Game information tuple
                - team (int): Self 1, opponent 2, neutral 0
                - state (list): State of 12 fortresses
                - moving_pawns (list): Information of moving units
                - spawning_pawns (list): Units waiting to spawn
                - done (bool): Game end flag

        Returns:
            tuple[int, int, int]: (command, subject, to)
        """
        # team, state, moving_pawns, spawning_pawns, done = info
        self.step += 1

        # Implementing strategy selection
        # if self.step < 10:
        #     command, subject, to = self.heuristic_strategy.decide(state)
        # else:
        #     command, subject, to = self.learning_strategy.decide(state, self.policy_model)

        # return command, subject, to

        return heuristic_strategy(info)