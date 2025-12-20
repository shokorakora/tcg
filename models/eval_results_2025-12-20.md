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
[2025-12-20 20:57:52] model=models\takeishi_final.pt episodes=10 Opponent=anchor Summary: wins=10/10
[2025-12-20 20:58:11] model=models\takeishi_final.pt episodes=10 Opponent=feeder Summary: wins=0/10
[2025-12-20 20:58:30] model=models\takeishi_final.pt episodes=10 Opponent=rusher Summary: wins=10/10
[2025-12-20 20:58:56] model=models\takeishi_final.pt episodes=10 Opponent=opportunist Summary: wins=7/10
[2025-12-20 20:59:08] model=models\takeishi_final.pt episodes=10 Opponent=counter Summary: wins=10/10
[2025-12-20 21:00:22] model=models\takeishi_final.pt episodes=10 Opponent=flow Summary: wins=10/10
[2025-12-20 21:30:16] model=models\takeishi_final.pt episodes=300 Opponent=claude Summary: wins=300/300
[2025-12-20 21:49:18] model=models\takeishi_final.pt episodes=300 Opponent=economist Summary: wins=286/300
[2025-12-20 22:00:57] model=models\takeishi_final.pt episodes=300 Opponent=random Summary: wins=300/300
[2025-12-20 22:05:00] model=models\takeishi_final.pt episodes=300 Opponent=splitpush Summary: wins=300/300
[2025-12-20 22:09:56] model=models\takeishi_final.pt episodes=300 Opponent=harasser Summary: wins=300/300
[2025-12-20 22:19:16] model=models\takeishi_final.pt episodes=300 Opponent=bulwark Summary: wins=21/300
[2025-12-20 22:23:02] model=models\takeishi_final.pt episodes=300 Opponent=anchor Summary: wins=300/300
[2025-12-20 22:29:20] model=models\takeishi_final.pt episodes=300 Opponent=feeder Summary: wins=1/300
[2025-12-20 22:36:14] model=models\takeishi_final.pt episodes=300 Opponent=rusher Summary: wins=300/300
[2025-12-20 22:46:50] model=models\takeishi_final.pt episodes=300 Opponent=opportunist Summary: wins=264/300
[2025-12-20 22:52:10] model=models\takeishi_final.pt episodes=300 Opponent=counter Summary: wins=300/300
[2025-12-20 23:16:56] model=models\takeishi_final.pt episodes=300 Opponent=flow Summary: wins=300/300
[2025-12-21 00:16:26] model=models\takeishi_final.pt episodes=10 Opponent=splitpush Summary: wins=10/10
[2025-12-21 00:16:36] model=models\takeishi_final.pt episodes=10 Opponent=anchor Summary: wins=10/10
[2025-12-21 00:16:42] model=models\takeishi_final.pt episodes=10 Opponent=harasser Summary: wins=10/10
[2025-12-21 00:16:54] model=models\takeishi_final.pt episodes=10 Opponent=counter Summary: wins=10/10
