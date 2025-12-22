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
[2025-12-21 11:55:09] model=models\takeishi_final.pt episodes=500 Opponent=claude Summary: wins=500/500
[2025-12-21 12:14:53] model=models\takeishi_final.pt episodes=500 Opponent=economist Summary: wins=484/500
[2025-12-21 12:27:45] model=models\takeishi_final.pt episodes=500 Opponent=random Summary: wins=500/500
[2025-12-21 12:53:31] model=models\takeishi_final.pt episodes=500 Opponent=splitpush Summary: wins=500/500
[2025-12-21 13:13:53] model=models\takeishi_final.pt episodes=500 Opponent=harasser Summary: wins=191/500
[2025-12-21 13:30:17] model=models\takeishi_final.pt episodes=500 Opponent=bulwark Summary: wins=32/500
[2025-12-21 14:54:12] model=models\takeishi_final.pt episodes=500 Opponent=anchor Summary: wins=128/500
[2025-12-21 15:05:18] model=models\takeishi_final.pt episodes=500 Opponent=feeder Summary: wins=1/500
[2025-12-21 15:17:40] model=models\takeishi_final.pt episodes=500 Opponent=rusher Summary: wins=500/500
[2025-12-21 15:35:37] model=models\takeishi_final.pt episodes=500 Opponent=opportunist Summary: wins=451/500
[2025-12-21 15:55:43] model=models\takeishi_final.pt episodes=500 Opponent=counter Summary: wins=200/500
[2025-12-21 16:39:01] model=models\takeishi_final.pt episodes=500 Opponent=flow Summary: wins=500/500
[2025-12-21 17:43:21] model=models\takeishi_final.pt episodes=100 Opponent=claude Summary: wins=100/100
[2025-12-21 17:47:13] model=models\takeishi_final.pt episodes=100 Opponent=economist Summary: wins=96/100
[2025-12-21 17:49:45] model=models\takeishi_final.pt episodes=100 Opponent=random Summary: wins=100/100
[2025-12-21 17:55:15] model=models\takeishi_final.pt episodes=100 Opponent=splitpush Summary: wins=100/100
[2025-12-21 18:00:12] model=models\takeishi_final.pt episodes=100 Opponent=harasser Summary: wins=40/100
[2025-12-21 18:05:37] model=models\takeishi_final.pt episodes=100 Opponent=bulwark Summary: wins=4/100
[2025-12-21 18:19:07] model=models\takeishi_final.pt episodes=100 Opponent=anchor Summary: wins=22/100
[2025-12-21 18:22:31] model=models\takeishi_final.pt episodes=100 Opponent=feeder Summary: wins=0/100
[2025-12-21 18:25:32] model=models\takeishi_final.pt episodes=100 Opponent=rusher Summary: wins=100/100
[2025-12-21 18:32:34] model=models\takeishi_final.pt episodes=100 Opponent=opportunist Summary: wins=91/100
[2025-12-21 18:40:33] model=models\takeishi_final.pt episodes=100 Opponent=counter Summary: wins=39/100
[2025-12-21 18:55:47] model=models\takeishi_final.pt episodes=100 Opponent=flow Summary: wins=100/100
[2025-12-22 15:21:41] model=models\takeishi_ep1200.pt episodes=100 Opponent=claude Summary: wins=100/100
[2025-12-22 15:25:22] model=models\takeishi_ep1200.pt episodes=100 Opponent=economist Summary: wins=98/100
[2025-12-22 15:27:41] model=models\takeishi_ep1200.pt episodes=100 Opponent=random Summary: wins=100/100
[2025-12-22 15:32:26] model=models\takeishi_ep1200.pt episodes=100 Opponent=splitpush Summary: wins=100/100
[2025-12-22 15:36:34] model=models\takeishi_ep1200.pt episodes=100 Opponent=harasser Summary: wins=58/100
[2025-12-22 15:39:47] model=models\takeishi_ep1200.pt episodes=100 Opponent=bulwark Summary: wins=6/100
[2025-12-22 15:54:06] model=models\takeishi_ep1200.pt episodes=100 Opponent=anchor Summary: wins=16/100
[2025-12-22 15:56:22] model=models\takeishi_ep1200.pt episodes=100 Opponent=feeder Summary: wins=0/100
[2025-12-22 15:58:42] model=models\takeishi_ep1200.pt episodes=100 Opponent=rusher Summary: wins=100/100
[2025-12-22 16:02:15] model=models\takeishi_ep1200.pt episodes=100 Opponent=opportunist Summary: wins=82/100
[2025-12-22 16:06:16] model=models\takeishi_ep1200.pt episodes=100 Opponent=counter Summary: wins=43/100
[2025-12-22 16:14:43] model=models\takeishi_ep1200.pt episodes=100 Opponent=flow Summary: wins=100/100
[2025-12-22 16:17:14] model=models\takeishi_ep2400.pt episodes=100 Opponent=claude Summary: wins=100/100
[2025-12-22 16:21:07] model=models\takeishi_ep2400.pt episodes=100 Opponent=economist Summary: wins=99/100
[2025-12-22 16:23:41] model=models\takeishi_ep2400.pt episodes=100 Opponent=random Summary: wins=100/100
[2025-12-22 16:28:30] model=models\takeishi_ep2400.pt episodes=100 Opponent=splitpush Summary: wins=100/100
[2025-12-22 16:32:07] model=models\takeishi_ep2400.pt episodes=100 Opponent=harasser Summary: wins=38/100
[2025-12-22 16:35:20] model=models\takeishi_ep2400.pt episodes=100 Opponent=bulwark Summary: wins=7/100
[2025-12-22 16:47:09] model=models\takeishi_ep2400.pt episodes=100 Opponent=anchor Summary: wins=21/100
[2025-12-22 16:49:20] model=models\takeishi_ep2400.pt episodes=100 Opponent=feeder Summary: wins=0/100
[2025-12-22 16:51:38] model=models\takeishi_ep2400.pt episodes=100 Opponent=rusher Summary: wins=100/100
[2025-12-22 16:55:40] model=models\takeishi_ep2400.pt episodes=100 Opponent=opportunist Summary: wins=86/100
[2025-12-22 16:59:55] model=models\takeishi_ep2400.pt episodes=100 Opponent=counter Summary: wins=45/100
[2025-12-22 17:09:51] model=models\takeishi_ep2400.pt episodes=100 Opponent=flow Summary: wins=100/100
[2025-12-22 17:11:59] model=models\takeishi_ep3600.pt episodes=100 Opponent=claude Summary: wins=100/100
[2025-12-22 17:15:48] model=models\takeishi_ep3600.pt episodes=100 Opponent=economist Summary: wins=95/100
[2025-12-22 17:17:57] model=models\takeishi_ep3600.pt episodes=100 Opponent=random Summary: wins=100/100
[2025-12-22 17:22:57] model=models\takeishi_ep3600.pt episodes=100 Opponent=splitpush Summary: wins=100/100
[2025-12-22 17:26:41] model=models\takeishi_ep3600.pt episodes=100 Opponent=harasser Summary: wins=53/100
[2025-12-22 17:30:19] model=models\takeishi_ep3600.pt episodes=100 Opponent=bulwark Summary: wins=13/100
[2025-12-22 17:45:40] model=models\takeishi_ep3600.pt episodes=100 Opponent=anchor Summary: wins=19/100
[2025-12-22 17:47:59] model=models\takeishi_ep3600.pt episodes=100 Opponent=feeder Summary: wins=0/100
[2025-12-22 17:50:22] model=models\takeishi_ep3600.pt episodes=100 Opponent=rusher Summary: wins=100/100
[2025-12-22 17:53:32] model=models\takeishi_ep3600.pt episodes=100 Opponent=opportunist Summary: wins=91/100
[2025-12-22 17:58:22] model=models\takeishi_ep3600.pt episodes=100 Opponent=counter Summary: wins=51/100
[2025-12-22 18:07:31] model=models\takeishi_ep3600.pt episodes=100 Opponent=flow Summary: wins=100/100
