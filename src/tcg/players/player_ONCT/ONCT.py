
from pathlib import Path
import numpy as np
from sb3_contrib import MaskablePPO
from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from tcg.controller import Controller
from tcg.config import fortress_limit, A_coordinate
from tcg.utils import flip_board_view

class ONCT(Controller):
    """
    AI Player using the trained Counter-ML MaskablePPO model.
    Trained against: ML_PPO, RightFlankAggressive, SecureHomeAggressive, AntiMLPlayer, 
                     EconomistAggressive, RightHeavyAggressive, RightFlank, AggressiveCenter
    """
    # Static cache to prevent reloading the model every time
    _cached_model = None
    _cached_model_path = None

    def __init__(self, model_path=None):
        self.team = "ONCT"
        self.obs_rms = None # For normalization
        
        if model_path is None:
            # Only use the final model. If not found, do not load any model.
            player_dir = Path(__file__).parents[0] # src/tcg/players/ -> src/
            # final_model = Path("/home/s2017/work/tcg/logs_counter_finetune/counter_ml_finetuned_6000000_steps.zip")
            final_model = player_dir / "counter_ml_finetuned_ver3.zip"
            if final_model.exists():
                # print(f"Loading TrainedCounter model from {final_model}")
                self.model_path = final_model
            else:
                print("Warning: No trained model found for TrainedCounterPlayer!")
                self.model_path = None
        else:
            self.model_path = Path(model_path)

        self.model = None
        if self.model_path and self.model_path.exists():
            # Check Cache
            if ONCT._cached_model and ONCT._cached_model_path == self.model_path:
                self.model = ONCT._cached_model
                self.obs_rms = getattr(ONCT, "_cached_obs_rms", None)
                return

            try:
                # print(f"Loading ONCT model from {self.model_path}")
                self.model = MaskablePPO.load(
                    self.model_path,
                    custom_objects={
                        "policy_class": MaskableActorCriticPolicy,
                        "learning_rate": 0.0,
                        "clip_range": 0.0,
                    }
                )
                
                # Load Normalization Stats
                # Assumes the pickle file has the same stem but ends in _vecnormalize.pkl
                # Or try the standard simple name if main model
                possible_norm_paths = [
                    self.model_path.parent / (self.model_path.stem + "_vecnormalize.pkl"),   # e.g. model_123_vecnormalize.pkl
                    self.model_path.parent / "counter_ml_finetuned_vecnormalize_6000000_steps.pkl"        # Standard name
                ]
                print(f"Attempting to load normalization stats from possible paths: {possible_norm_paths}")
                
                for norm_path in possible_norm_paths:
                    if norm_path.exists():
                        # print(f"Loading normalization stats from {norm_path}")
                        import pickle
                        with open(norm_path, "rb") as f:
                            vec_normalize = pickle.load(f)
                            # vec_normalize is a VecNormalize object (or similar wrapper dump)
                            # We need the running mean and variance
                            self.obs_rms = vec_normalize.obs_rms
                        break
                        
                if self.obs_rms is None:
                    print("Warning: No normalization stats found. Inference may be inaccurate.")
                
                # Update Cache
                ONCT._cached_model = self.model
                ONCT._cached_model_path = self.model_path
                ONCT._cached_obs_rms = self.obs_rms
                
            except Exception as e:
                print(f"Error loading model: {e}")

    def team_name(self) -> str:
        return self.team

    def action_masks(self, state):
        # state is list of [team, kind, level, pawn_number, upgrade_time, neighbors]
        # 432 actions
        mask = [False] * 432
        mask[0] = True # Wait is always valid
        
        # Move: 144 + subject*12 + target
        for s in range(12):
            # Check ownership (Team 1 is Me)
            if state[s][0] != 1: 
                continue
            
            # Check pawns >= 2
            if state[s][3] < 2:
                continue
                
            for t in range(12):
                # Check connection
                if A_coordinate[s][t] != 0:
                    idx = 144 + s * 12 + t
                    mask[idx] = True
                    
        # Upgrade: 288 + subject*12 + target
        for s in range(12):
             # Check ownership
            if state[s][0] != 1:
                continue
            
            # Check level < 5
            level = state[s][2]
            if level >= 5:
                continue
                
            # Check cost
            cost = fortress_limit[level] // 2
            if state[s][3] < cost:
                continue
                
            # Check not upgrading
            if state[s][4] != -1:
                continue
                
            # Target must be self for upgrade
            idx = 288 + s * 12 + s
            mask[idx] = True
            
        return mask

    def _get_obs(self, state, moving_pawns):
        # Construct observation vector matching the Gym environment
        # 1. Fortress State (12 * 5)
        state_obs = []
        for s in state:
            team_val = 0.0
            if s[0] == 1: team_val = 1.0
            elif s[0] == 2: team_val = -1.0
            
            kind = float(s[1])
            level = s[2] * 0.2
            pawns = np.log1p(s[3]) * 0.1
            upgrade = s[4] * 0.005 if s[4] != -1 else -1.0
            
            state_obs.extend([team_val, kind, level, pawns, upgrade])
        
        # 2. Edge Traffic (12 * 12 * 2)
        edge_traffic = np.zeros((12, 12, 2), dtype=np.float32)
        
        for pawn in moving_pawns:
            # pawn: [team, kind, from_, to, pos]
            team = pawn[0]
            from_ = pawn[2]
            to = pawn[3]
            
            # Team 1 is index 0, Team 2 is index 1
            team_idx = 0 if team == 1 else 1
            
            edge_traffic[from_][to][team_idx] += 0.01
            
        obs = np.concatenate([
            np.array(state_obs, dtype=np.float32),
            edge_traffic.flatten()
        ])
        
        # Apply Normalization if stats are available
        if self.obs_rms is not None:
            # Formula: (x - mean) / sqrt(var + epsilon)
            # Clip result to [-10, 10]
            epsilon = 1e-8
            obs = (obs - self.obs_rms.mean) / np.sqrt(self.obs_rms.var + epsilon)
            obs = np.clip(obs, -10.0, 10.0)
            
        return obs

    def update(self, info):
        if self.model is None:
            return 0, 0, 0 # Wait
            
        # Flip view so we are always Team 1
        flipped_info = flip_board_view(info)
        _, state, moving_pawns, spawning_pawns, done = flipped_info
        
        # Get observation
        obs = self._get_obs(state, moving_pawns)
        
        # Get action mask
        mask = self.action_masks(state)
        
        # Predict
        action, _ = self.model.predict(obs, action_masks=mask, deterministic=True)
        
        # Decode action
        action = int(action)
        
        if action == 0:
            return 0, 0, 0
        elif action < 144:
            return 0, 0, 0 # Should be masked out
        elif action < 288:
            # Move
            idx = action - 144
            sub = idx // 12
            tgt = idx % 12
            return 1, sub, tgt
        else:
            # Upgrade
            idx = action - 288
            sub = idx // 12
            tgt = idx % 12
            return 2, sub, tgt
