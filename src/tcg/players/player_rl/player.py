from tcg.controller import Controller
from tcg.players.player_takeishi.strategies.learning import LearningAgent

class RLPlayer(Controller):
    """
    Controller wrapper for the Takeishi LearningAgent to run
    windowed or headless games with a trained checkpoint.
    """
    def __init__(self, model_path: str, epsilon: float = 0.0, device: str = "cpu"):
        self.agent = LearningAgent(model_path=model_path, device=device)
        self.agent.epsilon = epsilon

    def team_name(self) -> str:
        return "TakeishiRL"

    def update(self, info):
        return self.agent.select_action(info)
