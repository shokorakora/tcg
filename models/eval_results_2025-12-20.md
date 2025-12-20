# Evaluation Results (2025-12-20)

Model: models/takeishi_final.pt
Window: False
Episodes per run: as noted
Environment: Windows, Python venv

## Summaries
- Claude (200 games): wins=200/200
- DefensiveEconomist (200 games): wins=186/200
- Random (200 games): wins=200/200

### Post economist-weighted training (quick checks)
- Economist (100 games): wins=93/100
- Claude (100 games): wins=100/100

## Notes
- Strategy prioritizes capturing/upgrading forts 9 and 11; RL fallback enforces target-first behavior.
- Training excludes ml_player.py and players_kishida; whitelist is enforced in training.
- For further robustness, consider training with weights `[0.15, 0.55, 0.30]` to increase Economist exposure.
[2025-12-20 20:48:53] model=models\takeishi_final.pt episodes=30 Opponent=bulwark Summary: wins=3/30
[2025-12-20 20:49:48] model=models\takeishi_final.pt episodes=10 Opponent=bulwark Summary: wins=0/10
[2025-12-20 20:51:15] model=models\takeishi_final.pt episodes=5 Opponent=bulwark Summary: wins=1/5
