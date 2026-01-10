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
[2025-12-23 00:44:55] model=models\takeishi_final.pt episodes=100 Opponent=claude Summary: wins=100/100
[2025-12-23 00:48:26] model=models\takeishi_final.pt episodes=100 Opponent=economist Summary: wins=93/100
[2025-12-23 00:50:37] model=models\takeishi_final.pt episodes=100 Opponent=random Summary: wins=100/100
[2025-12-23 10:29:51] model=models\takeishi_final.pt episodes=100 Opponent=claude Summary: wins=100/100
[2025-12-23 10:33:52] model=models\takeishi_final.pt episodes=100 Opponent=economist Summary: wins=95/100
[2025-12-23 10:36:20] model=models\takeishi_final.pt episodes=100 Opponent=random Summary: wins=100/100
[2025-12-23 10:41:17] model=models\takeishi_final.pt episodes=100 Opponent=splitpush Summary: wins=100/100
[2025-12-23 10:45:12] model=models\takeishi_final.pt episodes=100 Opponent=harasser Summary: wins=39/100
[2025-12-23 10:48:38] model=models\takeishi_final.pt episodes=100 Opponent=bulwark Summary: wins=8/100
[2025-12-23 11:03:27] model=models\takeishi_final.pt episodes=100 Opponent=anchor Summary: wins=18/100
[2025-12-23 11:05:48] model=models\takeishi_final.pt episodes=100 Opponent=feeder Summary: wins=2/100
[2025-12-23 11:08:05] model=models\takeishi_final.pt episodes=100 Opponent=rusher Summary: wins=100/100
[2025-12-23 11:11:42] model=models\takeishi_final.pt episodes=100 Opponent=opportunist Summary: wins=87/100
[2025-12-23 11:15:45] model=models\takeishi_final.pt episodes=100 Opponent=counter Summary: wins=42/100
[2025-12-23 11:28:58] model=models\takeishi_final.pt episodes=100 Opponent=flow Summary: wins=100/100
[2025-12-23 12:28:22] model=models\takeishi_final.pt episodes=100 Opponent=claude Summary: wins=100/100 draws=0 losses=0 timeouts=0
[2025-12-23 12:32:17] model=models\takeishi_final.pt episodes=100 Opponent=economist Summary: wins=99/100 draws=0 losses=1 timeouts=0
[2025-12-23 12:34:37] model=models\takeishi_final.pt episodes=100 Opponent=random Summary: wins=100/100 draws=0 losses=0 timeouts=0
[2025-12-23 12:45:52] model=models\takeishi_final.pt episodes=100 Opponent=splitpush Summary: wins=100/100 draws=0 losses=0 timeouts=27
[2025-12-23 12:49:07] model=models\takeishi_final.pt episodes=100 Opponent=harasser Summary: wins=43/100 draws=0 losses=57 timeouts=0
[2025-12-23 12:52:22] model=models\takeishi_final.pt episodes=100 Opponent=bulwark Summary: wins=10/100 draws=0 losses=90 timeouts=0
[2025-12-23 13:13:35] model=models\takeishi_final.pt episodes=100 Opponent=anchor Summary: wins=10/100 draws=0 losses=90 timeouts=25
[2025-12-23 13:15:54] model=models\takeishi_final.pt episodes=100 Opponent=feeder Summary: wins=0/100 draws=0 losses=100 timeouts=0
[2025-12-23 13:17:59] model=models\takeishi_final.pt episodes=100 Opponent=rusher Summary: wins=100/100 draws=0 losses=0 timeouts=0
[2025-12-23 13:21:25] model=models\takeishi_final.pt episodes=100 Opponent=opportunist Summary: wins=91/100 draws=0 losses=9 timeouts=0
[2025-12-23 13:25:17] model=models\takeishi_final.pt episodes=100 Opponent=counter Summary: wins=52/100 draws=0 losses=48 timeouts=0
[2025-12-23 14:06:50] model=models\takeishi_final.pt episodes=100 Opponent=flow Summary: wins=100/100 draws=0 losses=0 timeouts=78
[2025-12-23 18:56:27] model=models\takeishi_final.pt episodes=50 Opponent=claude Summary: wins=50/50 draws=0 losses=0 timeouts=0
[2025-12-23 18:59:04] model=models\takeishi_final.pt episodes=50 Opponent=economist Summary: wins=49/50 draws=0 losses=1 timeouts=0
[2025-12-23 19:00:48] model=models\takeishi_final.pt episodes=50 Opponent=random Summary: wins=50/50 draws=0 losses=0 timeouts=0
[2025-12-23 19:05:02] model=models\takeishi_final.pt episodes=50 Opponent=splitpush Summary: wins=50/50 draws=0 losses=0 timeouts=0
[2025-12-23 19:07:52] model=models\takeishi_final.pt episodes=50 Opponent=harasser Summary: wins=18/50 draws=0 losses=32 timeouts=0
[2025-12-23 19:09:50] model=models\takeishi_final.pt episodes=50 Opponent=bulwark Summary: wins=3/50 draws=0 losses=47 timeouts=0
[2025-12-23 19:27:58] model=models\takeishi_final.pt episodes=50 Opponent=anchor Summary: wins=10/50 draws=0 losses=40 timeouts=15
[2025-12-23 19:29:38] model=models\takeishi_final.pt episodes=50 Opponent=feeder Summary: wins=0/50 draws=0 losses=50 timeouts=0
[2025-12-23 19:31:26] model=models\takeishi_final.pt episodes=50 Opponent=rusher Summary: wins=50/50 draws=0 losses=0 timeouts=0
[2025-12-23 19:34:02] model=models\takeishi_final.pt episodes=50 Opponent=opportunist Summary: wins=46/50 draws=0 losses=4 timeouts=0
[2025-12-23 19:37:14] model=models\takeishi_final.pt episodes=50 Opponent=counter Summary: wins=16/50 draws=0 losses=34 timeouts=0
[2025-12-23 19:44:58] model=models\takeishi_final.pt episodes=50 Opponent=flow Summary: wins=50/50 draws=0 losses=0 timeouts=0
[2025-12-24 16:41:00] model=models\takeishi_final.pt episodes=50 Opponent=claude Summary: wins=50/50 draws=0 losses=0 timeouts=0
[2025-12-24 16:42:51] model=models\takeishi_final.pt episodes=50 Opponent=economist Summary: wins=47/50 draws=0 losses=3 timeouts=0
[2025-12-24 16:43:52] model=models\takeishi_final.pt episodes=50 Opponent=random Summary: wins=50/50 draws=0 losses=0 timeouts=0
[2025-12-24 16:46:23] model=models\takeishi_final.pt episodes=50 Opponent=splitpush Summary: wins=50/50 draws=0 losses=0 timeouts=0
[2025-12-24 16:48:03] model=models\takeishi_final.pt episodes=50 Opponent=harasser Summary: wins=21/50 draws=0 losses=29 timeouts=0
[2025-12-24 16:49:32] model=models\takeishi_final.pt episodes=50 Opponent=bulwark Summary: wins=4/50 draws=0 losses=46 timeouts=0
[2025-12-24 16:55:16] model=models\takeishi_final.pt episodes=50 Opponent=anchor Summary: wins=10/50 draws=0 losses=40 timeouts=7
[2025-12-24 16:56:16] model=models\takeishi_final.pt episodes=50 Opponent=feeder Summary: wins=0/50 draws=0 losses=50 timeouts=0
[2025-12-24 16:57:08] model=models\takeishi_final.pt episodes=50 Opponent=rusher Summary: wins=50/50 draws=0 losses=0 timeouts=0
[2025-12-24 16:58:28] model=models\takeishi_final.pt episodes=50 Opponent=opportunist Summary: wins=49/50 draws=0 losses=1 timeouts=0
[2025-12-24 17:00:28] model=models\takeishi_final.pt episodes=50 Opponent=counter Summary: wins=26/50 draws=0 losses=24 timeouts=0
[2025-12-24 17:04:55] model=models\takeishi_final.pt episodes=50 Opponent=flow Summary: wins=50/50 draws=0 losses=0 timeouts=0
[2025-12-25 09:43:12] model=models\takeishi_final.pt episodes=50 Opponent=claude Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=12743
[2025-12-25 09:44:41] model=models\takeishi_final.pt episodes=50 Opponent=economist Summary: wins=46/50 draws=0 losses=4 timeouts=0 avg_steps=18386
[2025-12-25 09:45:37] model=models\takeishi_final.pt episodes=50 Opponent=random Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=13330
[2025-12-25 09:47:53] model=models\takeishi_final.pt episodes=50 Opponent=splitpush Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=18048
[2025-12-25 09:49:19] model=models\takeishi_final.pt episodes=50 Opponent=harasser Summary: wins=20/50 draws=0 losses=30 timeouts=0 avg_steps=16331
[2025-12-25 09:50:33] model=models\takeishi_final.pt episodes=50 Opponent=bulwark Summary: wins=2/50 draws=0 losses=48 timeouts=0 avg_steps=14672
[2025-12-25 10:02:38] model=models\takeishi_final.pt episodes=50 Opponent=anchor Summary: wins=11/50 draws=0 losses=39 timeouts=19 avg_steps=30193
[2025-12-25 10:03:29] model=models\takeishi_final.pt episodes=50 Opponent=feeder Summary: wins=0/50 draws=0 losses=50 timeouts=0 avg_steps=10149
[2025-12-25 10:04:16] model=models\takeishi_final.pt episodes=50 Opponent=rusher Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=13140
[2025-12-25 10:05:25] model=models\takeishi_final.pt episodes=50 Opponent=opportunist Summary: wins=45/50 draws=0 losses=5 timeouts=0 avg_steps=16028
[2025-12-25 10:06:47] model=models\takeishi_final.pt episodes=50 Opponent=counter Summary: wins=18/50 draws=0 losses=32 timeouts=0 avg_steps=15359
[2025-12-25 10:11:14] model=models\takeishi_final.pt episodes=50 Opponent=flow Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=22042
[2025-12-25 23:01:31] model=models\takeishi_final.pt episodes=50 Opponent=claude Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=12553
[2025-12-25 23:03:01] model=models\takeishi_final.pt episodes=50 Opponent=economist Summary: wins=46/50 draws=0 losses=4 timeouts=0 avg_steps=17819
[2025-12-25 23:04:00] model=models\takeishi_final.pt episodes=50 Opponent=random Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=13680
[2025-12-25 23:06:33] model=models\takeishi_final.pt episodes=50 Opponent=splitpush Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=18422
[2025-12-25 23:08:15] model=models\takeishi_final.pt episodes=50 Opponent=harasser Summary: wins=16/50 draws=0 losses=34 timeouts=0 avg_steps=16390
[2025-12-25 23:10:17] model=models\takeishi_final.pt episodes=50 Opponent=bulwark Summary: wins=5/50 draws=0 losses=45 timeouts=0 avg_steps=14014
[2025-12-25 23:22:22] model=models\takeishi_final.pt episodes=50 Opponent=anchor Summary: wins=8/50 draws=0 losses=42 timeouts=17 avg_steps=28488
[2025-12-25 23:23:16] model=models\takeishi_final.pt episodes=50 Opponent=feeder Summary: wins=0/50 draws=0 losses=50 timeouts=0 avg_steps=10295
[2025-12-25 23:24:12] model=models\takeishi_final.pt episodes=50 Opponent=rusher Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=13428
[2025-12-25 23:25:40] model=models\takeishi_final.pt episodes=50 Opponent=opportunist Summary: wins=46/50 draws=0 losses=4 timeouts=0 avg_steps=16251
[2025-12-25 23:27:30] model=models\takeishi_final.pt episodes=50 Opponent=counter Summary: wins=21/50 draws=0 losses=29 timeouts=0 avg_steps=15281
[2025-12-25 23:32:49] model=models\takeishi_final.pt episodes=50 Opponent=flow Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=22301
[2025-12-26 23:19:29] model=models\takeishi_ep50000.pt episodes=50 Opponent=claude Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=11817
[2025-12-26 23:21:24] model=models\takeishi_ep50000.pt episodes=50 Opponent=economist Summary: wins=48/50 draws=0 losses=2 timeouts=0 avg_steps=18525
[2025-12-26 23:22:27] model=models\takeishi_ep50000.pt episodes=50 Opponent=random Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=13011
[2025-12-26 23:24:28] model=models\takeishi_ep50000.pt episodes=50 Opponent=splitpush Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=16808
[2025-12-26 23:25:58] model=models\takeishi_ep50000.pt episodes=50 Opponent=harasser Summary: wins=29/50 draws=0 losses=21 timeouts=0 avg_steps=16494
[2025-12-26 23:27:00] model=models\takeishi_ep50000.pt episodes=50 Opponent=bulwark Summary: wins=2/50 draws=0 losses=48 timeouts=0 avg_steps=12063
[2025-12-26 23:38:50] model=models\takeishi_ep50000.pt episodes=50 Opponent=anchor Summary: wins=7/50 draws=0 losses=43 timeouts=17 avg_steps=27693
[2025-12-26 23:39:39] model=models\takeishi_ep50000.pt episodes=50 Opponent=feeder Summary: wins=0/50 draws=0 losses=50 timeouts=0 avg_steps=9483
[2025-12-26 23:40:35] model=models\takeishi_ep50000.pt episodes=50 Opponent=rusher Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=13375
[2025-12-26 23:41:45] model=models\takeishi_ep50000.pt episodes=50 Opponent=opportunist Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=15117
[2025-12-26 23:43:08] model=models\takeishi_ep50000.pt episodes=50 Opponent=counter Summary: wins=11/50 draws=0 losses=39 timeouts=0 avg_steps=15008
[2025-12-26 23:46:35] model=models\takeishi_ep50000.pt episodes=50 Opponent=flow Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=19696
[2025-12-27 11:06:23] model=models\takeishi_ep55000.pt episodes=50 Opponent=claude Summary: wins=49/50 draws=0 losses=1 timeouts=0 avg_steps=12819
[2025-12-27 11:08:12] model=models\takeishi_ep55000.pt episodes=50 Opponent=economist Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=18641
[2025-12-27 11:09:16] model=models\takeishi_ep55000.pt episodes=50 Opponent=random Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=12948
[2025-12-27 11:11:26] model=models\takeishi_ep55000.pt episodes=50 Opponent=splitpush Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=16564
[2025-12-27 11:12:59] model=models\takeishi_ep55000.pt episodes=50 Opponent=harasser Summary: wins=18/50 draws=0 losses=32 timeouts=0 avg_steps=15943
[2025-12-27 11:14:14] model=models\takeishi_ep55000.pt episodes=50 Opponent=bulwark Summary: wins=4/50 draws=0 losses=46 timeouts=0 avg_steps=13018
[2025-12-27 11:24:52] model=models\takeishi_ep55000.pt episodes=50 Opponent=anchor Summary: wins=12/50 draws=0 losses=38 timeouts=15 avg_steps=26013
[2025-12-27 11:25:49] model=models\takeishi_ep55000.pt episodes=50 Opponent=feeder Summary: wins=0/50 draws=0 losses=50 timeouts=0 avg_steps=9806
[2025-12-27 11:26:56] model=models\takeishi_ep55000.pt episodes=50 Opponent=rusher Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=13148
[2025-12-27 11:28:06] model=models\takeishi_ep55000.pt episodes=50 Opponent=opportunist Summary: wins=49/50 draws=0 losses=1 timeouts=0 avg_steps=13937
[2025-12-27 11:29:40] model=models\takeishi_ep55000.pt episodes=50 Opponent=counter Summary: wins=23/50 draws=0 losses=27 timeouts=0 avg_steps=15606
[2025-12-27 11:33:48] model=models\takeishi_ep55000.pt episodes=50 Opponent=flow Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=20173
[2025-12-29 21:45:15] model=models\takeishi_ep72000.pt episodes=50 Opponent=claude Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=12064
[2025-12-29 21:47:01] model=models\takeishi_ep72000.pt episodes=50 Opponent=economist Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=18243
[2025-12-29 21:48:12] model=models\takeishi_ep72000.pt episodes=50 Opponent=random Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=13875
[2025-12-29 21:50:34] model=models\takeishi_ep72000.pt episodes=50 Opponent=splitpush Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=16994
[2025-12-29 21:52:01] model=models\takeishi_ep72000.pt episodes=50 Opponent=harasser Summary: wins=21/50 draws=0 losses=29 timeouts=0 avg_steps=14857
[2025-12-29 21:53:09] model=models\takeishi_ep72000.pt episodes=50 Opponent=bulwark Summary: wins=2/50 draws=0 losses=48 timeouts=0 avg_steps=12693
[2025-12-29 22:05:48] model=models\takeishi_ep72000.pt episodes=50 Opponent=anchor Summary: wins=8/50 draws=0 losses=42 timeouts=18 avg_steps=29726
[2025-12-29 22:06:41] model=models\takeishi_ep72000.pt episodes=50 Opponent=feeder Summary: wins=0/50 draws=0 losses=50 timeouts=0 avg_steps=9648
[2025-12-29 22:07:49] model=models\takeishi_ep72000.pt episodes=50 Opponent=rusher Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=13500
[2025-12-29 22:09:00] model=models\takeishi_ep72000.pt episodes=50 Opponent=opportunist Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=14019
[2025-12-29 22:10:28] model=models\takeishi_ep72000.pt episodes=50 Opponent=counter Summary: wins=22/50 draws=0 losses=28 timeouts=0 avg_steps=14477
[2025-12-29 22:14:25] model=models\takeishi_ep72000.pt episodes=50 Opponent=flow Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=19891
[2025-12-31 10:55:02] model=models\takeishi_ep93000.pt episodes=50 Opponent=claude Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=11635
[2025-12-31 10:56:49] model=models\takeishi_ep93000.pt episodes=50 Opponent=economist Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=18002
[2025-12-31 10:57:52] model=models\takeishi_ep93000.pt episodes=50 Opponent=random Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=13146
[2025-12-31 11:00:17] model=models\takeishi_ep93000.pt episodes=50 Opponent=splitpush Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=17064
[2025-12-31 11:01:48] model=models\takeishi_ep93000.pt episodes=50 Opponent=harasser Summary: wins=21/50 draws=0 losses=29 timeouts=0 avg_steps=15198
[2025-12-31 11:03:01] model=models\takeishi_ep93000.pt episodes=50 Opponent=bulwark Summary: wins=2/50 draws=0 losses=48 timeouts=0 avg_steps=13227
[2025-12-31 11:12:48] model=models\takeishi_ep93000.pt episodes=50 Opponent=anchor Summary: wins=9/50 draws=0 losses=41 timeouts=14 avg_steps=25504
[2025-12-31 11:13:37] model=models\takeishi_ep93000.pt episodes=50 Opponent=feeder Summary: wins=0/50 draws=0 losses=50 timeouts=0 avg_steps=9423
[2025-12-31 11:14:37] model=models\takeishi_ep93000.pt episodes=50 Opponent=rusher Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=13088
[2025-12-31 11:15:45] model=models\takeishi_ep93000.pt episodes=50 Opponent=opportunist Summary: wins=49/50 draws=0 losses=1 timeouts=0 avg_steps=13968
[2025-12-31 11:17:22] model=models\takeishi_ep93000.pt episodes=50 Opponent=counter Summary: wins=20/50 draws=0 losses=30 timeouts=0 avg_steps=15859
[2025-12-31 11:21:30] model=models\takeishi_ep93000.pt episodes=50 Opponent=flow Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=19971
[2025-12-31 15:51:18] model=models\takeishi_ep95000.pt episodes=50 Opponent=claude Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=11929
[2025-12-31 15:53:26] model=models\takeishi_ep95000.pt episodes=50 Opponent=economist Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=18833
[2025-12-31 15:54:29] model=models\takeishi_ep95000.pt episodes=50 Opponent=random Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=12975
[2025-12-31 15:57:00] model=models\takeishi_ep95000.pt episodes=50 Opponent=splitpush Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=17260
[2025-12-31 15:58:43] model=models\takeishi_ep95000.pt episodes=50 Opponent=harasser Summary: wins=25/50 draws=0 losses=25 timeouts=0 avg_steps=16823
[2025-12-31 15:59:46] model=models\takeishi_ep95000.pt episodes=50 Opponent=bulwark Summary: wins=1/50 draws=0 losses=49 timeouts=0 avg_steps=11926
[2025-12-31 16:11:10] model=models\takeishi_ep95000.pt episodes=50 Opponent=anchor Summary: wins=7/50 draws=0 losses=43 timeouts=15 avg_steps=27190
[2025-12-31 16:12:03] model=models\takeishi_ep95000.pt episodes=50 Opponent=feeder Summary: wins=1/50 draws=0 losses=49 timeouts=0 avg_steps=9680
[2025-12-31 16:13:00] model=models\takeishi_ep95000.pt episodes=50 Opponent=rusher Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=12861
[2025-12-31 16:14:24] model=models\takeishi_ep95000.pt episodes=50 Opponent=opportunist Summary: wins=49/50 draws=0 losses=1 timeouts=0 avg_steps=14180
[2025-12-31 16:15:59] model=models\takeishi_ep95000.pt episodes=50 Opponent=counter Summary: wins=22/50 draws=0 losses=28 timeouts=0 avg_steps=15832
[2025-12-31 16:20:00] model=models\takeishi_ep95000.pt episodes=50 Opponent=flow Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=19853
[2026-01-04 09:15:26] model=models\takeishi_ep114000.pt episodes=50 Opponent=claude Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=12048
[2026-01-04 09:17:07] model=models\takeishi_ep114000.pt episodes=50 Opponent=economist Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=17863
[2026-01-04 09:18:09] model=models\takeishi_ep114000.pt episodes=50 Opponent=random Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=13359
[2026-01-04 09:20:22] model=models\takeishi_ep114000.pt episodes=50 Opponent=splitpush Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=16729
[2026-01-04 09:21:49] model=models\takeishi_ep114000.pt episodes=50 Opponent=harasser Summary: wins=16/50 draws=0 losses=34 timeouts=0 avg_steps=15772
[2026-01-04 09:22:50] model=models\takeishi_ep114000.pt episodes=50 Opponent=bulwark Summary: wins=2/50 draws=0 losses=48 timeouts=0 avg_steps=12088
[2026-01-04 09:34:02] model=models\takeishi_ep114000.pt episodes=50 Opponent=anchor Summary: wins=9/50 draws=0 losses=41 timeouts=16 avg_steps=27648
[2026-01-04 09:34:56] model=models\takeishi_ep114000.pt episodes=50 Opponent=feeder Summary: wins=0/50 draws=0 losses=50 timeouts=0 avg_steps=9614
[2026-01-04 09:35:52] model=models\takeishi_ep114000.pt episodes=50 Opponent=rusher Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=12850
[2026-01-04 09:37:02] model=models\takeishi_ep114000.pt episodes=50 Opponent=opportunist Summary: wins=44/50 draws=0 losses=6 timeouts=0 avg_steps=14401
[2026-01-04 09:38:36] model=models\takeishi_ep114000.pt episodes=50 Opponent=counter Summary: wins=22/50 draws=0 losses=28 timeouts=0 avg_steps=15479
[2026-01-04 09:42:24] model=models\takeishi_ep114000.pt episodes=50 Opponent=flow Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=19848
[2026-01-05 00:11:27] model=models\takeishi_ep98000.pt episodes=50 Opponent=claude Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=12570
[2026-01-05 00:13:14] model=models\takeishi_ep98000.pt episodes=50 Opponent=economist Summary: wins=49/50 draws=0 losses=1 timeouts=0 avg_steps=17719
[2026-01-05 00:14:35] model=models\takeishi_ep98000.pt episodes=50 Opponent=random Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=13511
[2026-01-05 00:32:35] model=models\takeishi_ep98000.pt episodes=50 Opponent=splitpush Summary: wins=50/50 draws=0 losses=0 timeouts=40 avg_steps=43915
[2026-01-05 00:35:36] model=models\takeishi_ep98000.pt episodes=50 Opponent=harasser Summary: wins=24/50 draws=0 losses=26 timeouts=3 avg_steps=17512
[2026-01-05 00:36:51] model=models\takeishi_ep98000.pt episodes=50 Opponent=bulwark Summary: wins=4/50 draws=0 losses=46 timeouts=0 avg_steps=12713
[2026-01-05 00:50:49] model=models\takeishi_ep98000.pt episodes=50 Opponent=anchor Summary: wins=6/50 draws=0 losses=44 timeouts=21 avg_steps=30549
[2026-01-05 00:51:46] model=models\takeishi_ep98000.pt episodes=50 Opponent=feeder Summary: wins=0/50 draws=0 losses=50 timeouts=0 avg_steps=9747
[2026-01-05 00:52:58] model=models\takeishi_ep98000.pt episodes=50 Opponent=rusher Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=13274
[2026-01-05 00:54:22] model=models\takeishi_ep98000.pt episodes=50 Opponent=opportunist Summary: wins=47/50 draws=0 losses=3 timeouts=0 avg_steps=15314
[2026-01-05 00:57:28] model=models\takeishi_ep98000.pt episodes=50 Opponent=counter Summary: wins=22/50 draws=0 losses=28 timeouts=4 avg_steps=17167
[2026-01-05 01:06:40] model=models\takeishi_ep98000.pt episodes=50 Opponent=flow Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=26235
[2026-01-05 15:59:48] model=models\takeishi_ep100000.pt episodes=50 Opponent=claude Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=11958
[2026-01-05 16:02:53] model=models\takeishi_ep100000.pt episodes=50 Opponent=economist Summary: wins=50/50 draws=0 losses=0 timeouts=1 avg_steps=19684
[2026-01-05 16:04:45] model=models\takeishi_ep100000.pt episodes=50 Opponent=random Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=14198
[2026-01-05 16:24:27] model=models\takeishi_ep100000.pt episodes=50 Opponent=splitpush Summary: wins=50/50 draws=0 losses=0 timeouts=41 avg_steps=45967
[2026-01-05 16:26:45] model=models\takeishi_ep100000.pt episodes=50 Opponent=harasser Summary: wins=25/50 draws=0 losses=25 timeouts=1 avg_steps=16872
[2026-01-05 16:27:59] model=models\takeishi_ep100000.pt episodes=50 Opponent=bulwark Summary: wins=1/50 draws=0 losses=49 timeouts=0 avg_steps=13022
[2026-01-05 16:38:26] model=models\takeishi_ep100000.pt episodes=50 Opponent=anchor Summary: wins=11/50 draws=0 losses=39 timeouts=15 avg_steps=26757
[2026-01-05 16:39:19] model=models\takeishi_ep100000.pt episodes=50 Opponent=feeder Summary: wins=0/50 draws=0 losses=50 timeouts=0 avg_steps=9501
[2026-01-05 16:40:56] model=models\takeishi_ep100000.pt episodes=50 Opponent=rusher Summary: wins=50/50 draws=0 losses=0 timeouts=1 avg_steps=13948
[2026-01-05 16:42:59] model=models\takeishi_ep100000.pt episodes=50 Opponent=opportunist Summary: wins=49/50 draws=0 losses=1 timeouts=1 avg_steps=15901
[2026-01-05 16:44:29] model=models\takeishi_ep100000.pt episodes=50 Opponent=counter Summary: wins=20/50 draws=0 losses=30 timeouts=0 avg_steps=14430
[2026-01-05 17:08:49] model=models\takeishi_ep100000.pt episodes=50 Opponent=flow Summary: wins=50/50 draws=0 losses=0 timeouts=20 avg_steps=39542
[2026-01-06 17:15:49] model=models\takeishi_ep105000.pt episodes=50 Opponent=claude Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=12128
[2026-01-06 17:20:25] model=models\takeishi_ep105000.pt episodes=50 Opponent=economist Summary: wins=50/50 draws=0 losses=0 timeouts=4 avg_steps=22053
[2026-01-06 17:21:59] model=models\takeishi_ep105000.pt episodes=50 Opponent=random Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=13490
[2026-01-06 17:28:01] model=models\takeishi_ep105000.pt episodes=50 Opponent=splitpush Summary: wins=50/50 draws=0 losses=0 timeouts=5 avg_steps=21765
[2026-01-06 17:30:05] model=models\takeishi_ep105000.pt episodes=50 Opponent=harasser Summary: wins=26/50 draws=0 losses=24 timeouts=1 avg_steps=15626
[2026-01-06 17:31:29] model=models\takeishi_ep105000.pt episodes=50 Opponent=bulwark Summary: wins=3/50 draws=0 losses=47 timeouts=0 avg_steps=14010
[2026-01-06 17:43:26] model=models\takeishi_ep105000.pt episodes=50 Opponent=anchor Summary: wins=6/50 draws=0 losses=44 timeouts=19 avg_steps=27930
[2026-01-06 17:44:19] model=models\takeishi_ep105000.pt episodes=50 Opponent=feeder Summary: wins=0/50 draws=0 losses=50 timeouts=0 avg_steps=9563
[2026-01-06 17:46:39] model=models\takeishi_ep105000.pt episodes=50 Opponent=rusher Summary: wins=50/50 draws=0 losses=0 timeouts=2 avg_steps=14863
[2026-01-06 17:48:24] model=models\takeishi_ep105000.pt episodes=50 Opponent=opportunist Summary: wins=49/50 draws=0 losses=1 timeouts=0 avg_steps=14456
[2026-01-06 17:51:47] model=models\takeishi_ep105000.pt episodes=50 Opponent=counter Summary: wins=28/50 draws=0 losses=22 timeouts=3 avg_steps=17961
[2026-01-06 18:01:26] model=models\takeishi_ep105000.pt episodes=50 Opponent=flow Summary: wins=50/50 draws=0 losses=0 timeouts=3 avg_steps=26962

## Delta summary (ep100000 → ep105000)
- SplitPush: timeouts 41 → 5 (−36), avg_steps 45,967 → 21,765 (−24,202); wins unchanged 50/50.
- Flow: timeouts 20 → 3 (−17), avg_steps 39,542 → 26,962 (−12,580); wins unchanged 50/50.
- Counter: wins 20 → 28 (+8), timeouts 0 → 3 (+3), avg_steps 14,430 → 17,961 (+3,531).
- Anchor: wins 11 → 6 (−5), timeouts 15 → 19 (+4), avg_steps 26,757 → 27,930 (+1,173).
- Bulwark: wins 1 → 3 (+2), avg_steps 13,022 → 14,010 (+988).
- Harasser: wins 25 → 26 (+1), avg_steps 16,872 → 15,626 (−1,246); timeouts unchanged.
- Opportunist: wins 49 → 49 (±0), avg_steps 15,901 → 14,456 (−1,445).
- Economist: wins 50 → 50 (±0), timeouts 1 → 4 (+3), avg_steps 19,684 → 22,053 (+2,369).
- Rusher: wins 50 → 50 (±0), timeouts 1 → 2 (+1), avg_steps 13,948 → 14,863 (+915).
- Claude/Random: wins unchanged 50/50; Random avg_steps 14,198 → 13,490 (−708).
- Feeder: unchanged at 0/50.
[2026-01-07 20:25:51] model=models\takeishi_ep115000.pt episodes=50 Opponent=claude Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=12012
[2026-01-07 20:27:35] model=models\takeishi_ep115000.pt episodes=50 Opponent=economist Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=17908
[2026-01-07 20:28:38] model=models\takeishi_ep115000.pt episodes=50 Opponent=random Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=12831
[2026-01-07 20:30:58] model=models\takeishi_ep115000.pt episodes=50 Opponent=splitpush Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=16758
[2026-01-07 20:32:33] model=models\takeishi_ep115000.pt episodes=50 Opponent=harasser Summary: wins=30/50 draws=0 losses=20 timeouts=0 avg_steps=15425
[2026-01-07 20:33:47] model=models\takeishi_ep115000.pt episodes=50 Opponent=bulwark Summary: wins=1/50 draws=0 losses=49 timeouts=0 avg_steps=13308
[2026-01-07 20:41:17] model=models\takeishi_ep115000.pt episodes=50 Opponent=anchor Summary: wins=13/50 draws=0 losses=37 timeouts=11 avg_steps=22137
[2026-01-07 20:42:08] model=models\takeishi_ep115000.pt episodes=50 Opponent=feeder Summary: wins=0/50 draws=0 losses=50 timeouts=0 avg_steps=9376
[2026-01-07 20:43:13] model=models\takeishi_ep115000.pt episodes=50 Opponent=rusher Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=13062
[2026-01-07 20:44:28] model=models\takeishi_ep115000.pt episodes=50 Opponent=opportunist Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=14121
[2026-01-07 20:46:01] model=models\takeishi_ep115000.pt episodes=50 Opponent=counter Summary: wins=21/50 draws=0 losses=29 timeouts=0 avg_steps=15294
[2026-01-07 20:49:41] model=models\takeishi_ep115000.pt episodes=50 Opponent=flow Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=19056

## Delta summary (ep105000 → ep115000)
- SplitPush: timeouts 5 → 0 (−5), avg_steps 21,765 → 16,758 (−5,007); wins 50/50 → 50/50.
- Flow: timeouts 3 → 0 (−3), avg_steps 26,962 → 19,056 (−7,906); wins 50/50 → 50/50.
- Anchor: wins 6 → 13 (+7), timeouts 19 → 11 (−8), avg_steps 27,930 → 22,137 (−5,793).
- Bulwark: wins 3 → 1 (−2), avg_steps 14,010 → 13,308 (−702); 依然として弱い。
- Harasser: wins 26 → 30 (+4), timeouts 1 → 0 (−1), avg_steps 15,626 → 15,425 (−201).
- Counter: wins 28 → 21 (−7), timeouts 3 → 0 (−3), avg_steps 17,961 → 15,294 (−2,667)。勝率は低下。
- Opportunist: wins 49 → 50 (+1), avg_steps 14,456 → 14,121 (−335).
- Economist: wins 50 → 50 (±0), timeouts 4 → 0 (−4), avg_steps 22,053 → 17,908 (−4,145)。
- Rusher: wins 50 → 50 (±0), timeouts 2 → 0 (−2), avg_steps 14,863 → 13,062 (−1,801)。
- Claude/Random: 勝率維持、avg_steps わずかに改善。
[2026-01-08 12:42:05] model=models\takeishi_ep120000.pt episodes=50 Opponent=claude Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=11618
[2026-01-08 12:43:56] model=models\takeishi_ep120000.pt episodes=50 Opponent=economist Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=17920
[2026-01-08 12:44:59] model=models\takeishi_ep120000.pt episodes=50 Opponent=random Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=13005
[2026-01-08 12:47:09] model=models\takeishi_ep120000.pt episodes=50 Opponent=splitpush Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=16346
[2026-01-08 12:48:41] model=models\takeishi_ep120000.pt episodes=50 Opponent=harasser Summary: wins=28/50 draws=0 losses=22 timeouts=0 avg_steps=15731
[2026-01-08 12:49:41] model=models\takeishi_ep120000.pt episodes=50 Opponent=bulwark Summary: wins=0/50 draws=0 losses=50 timeouts=0 avg_steps=11677
[2026-01-08 12:57:13] model=models\takeishi_ep120000.pt episodes=50 Opponent=anchor Summary: wins=12/50 draws=0 losses=38 timeouts=11 avg_steps=21880
[2026-01-08 12:57:59] model=models\takeishi_ep120000.pt episodes=50 Opponent=feeder Summary: wins=0/50 draws=0 losses=50 timeouts=0 avg_steps=9200
[2026-01-08 12:59:02] model=models\takeishi_ep120000.pt episodes=50 Opponent=rusher Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=13043
[2026-01-08 13:00:14] model=models\takeishi_ep120000.pt episodes=50 Opponent=opportunist Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=14204
[2026-01-08 13:01:44] model=models\takeishi_ep120000.pt episodes=50 Opponent=counter Summary: wins=25/50 draws=0 losses=25 timeouts=0 avg_steps=15251
[2026-01-08 13:05:32] model=models\takeishi_ep120000.pt episodes=50 Opponent=flow Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=19182
[2026-01-09 23:29:03] model=models\takeishi_ep125000.pt episodes=50 Opponent=claude Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=12309
[2026-01-09 23:30:48] model=models\takeishi_ep125000.pt episodes=50 Opponent=economist Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=18052
[2026-01-09 23:31:50] model=models\takeishi_ep125000.pt episodes=50 Opponent=random Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=12915
[2026-01-09 23:34:15] model=models\takeishi_ep125000.pt episodes=50 Opponent=splitpush Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=16858
[2026-01-09 23:35:46] model=models\takeishi_ep125000.pt episodes=50 Opponent=harasser Summary: wins=28/50 draws=0 losses=22 timeouts=0 avg_steps=15744
[2026-01-09 23:36:51] model=models\takeishi_ep125000.pt episodes=50 Opponent=bulwark Summary: wins=1/50 draws=0 losses=49 timeouts=0 avg_steps=12307
[2026-01-09 23:46:40] model=models\takeishi_ep125000.pt episodes=50 Opponent=anchor Summary: wins=8/50 draws=0 losses=42 timeouts=13 avg_steps=25314
[2026-01-09 23:47:33] model=models\takeishi_ep125000.pt episodes=50 Opponent=feeder Summary: wins=0/50 draws=0 losses=50 timeouts=0 avg_steps=9510
[2026-01-09 23:48:35] model=models\takeishi_ep125000.pt episodes=50 Opponent=rusher Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=12983
[2026-01-09 23:49:57] model=models\takeishi_ep125000.pt episodes=50 Opponent=opportunist Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=15502
[2026-01-09 23:51:34] model=models\takeishi_ep125000.pt episodes=50 Opponent=counter Summary: wins=32/50 draws=0 losses=18 timeouts=0 avg_steps=15644
[2026-01-09 23:55:55] model=models\takeishi_ep125000.pt episodes=50 Opponent=flow Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=19873

## Delta summary (ep120000 → ep125000)
- SplitPush: wins 50→50 (±0), avg_steps 16,346→16,858 (+512), timeouts 0→0。
- Flow: wins 50→50 (±0), avg_steps 19,182→19,873 (+691), timeouts 0→0。
- Anchor: wins 12→8 (−4), timeouts 11→13 (+2), avg_steps 21,880→25,314 (+3,434)。後退。
- Bulwark: wins 0→1 (+1), avg_steps 11,677→12,307 (+630)。勝率は依然低い。
- Harasser: wins 28→28 (±0)、avg_steps 15,731→15,744 (+13)。横ばい。
- Counter: wins 25→32 (+7)、avg_steps 15,251→15,644 (+393)。勝率改善。
- Opportunist: wins 50→50 (±0)、avg_steps 14,204→15,502 (+1,298)。やや長期化。
- Economist: wins 50→50 (±0)、avg_steps 17,920→18,052 (+132)。微増。
- Claude: wins 50→50 (±0)、avg_steps 11,618→12,309 (+691)。
- Random: wins 50→50 (±0)、avg_steps 13,005→12,915 (−90)。
- Feeder: wins 0→0 (±0)、avg_steps 9,200→9,510 (+310)。

## Delta summary (ep115000 → ep120000)
- SplitPush: timeouts 0 → 0 (±0), avg_steps 16,758 → 16,346 (−412); wins 50/50 → 50/50。
- Flow: timeouts 0 → 0 (±0), avg_steps 19,056 → 19,182 (+126); wins 50/50 → 50/50。
- Anchor: wins 13 → 12 (−1), timeouts 11 → 11 (±0), avg_steps 22,137 → 21,880 (−257)。
- Bulwark: wins 1 → 0 (−1), avg_steps 13,308 → 11,677 (−1,631)。勝率は低下、展開は速くなったが負けが増加。
- Harasser: wins 30 → 28 (−2), avg_steps 15,425 → 15,731 (+306)。
- Counter: wins 21 → 25 (+4), avg_steps 15,294 → 15,251 (−43)。
- Opportunist: wins 50 → 50 (±0), avg_steps 14,121 → 14,204 (+83)。
- Economist: wins 50 → 50 (±0), timeouts 0 → 0 (±0), avg_steps 17,908 → 17,920 (+12)。
- Rusher: wins 50 → 50 (±0), timeouts 0 → 0 (±0), avg_steps 13,062 → 13,043 (−19)。
- Claude: wins 50 → 50 (±0), avg_steps 12,012 → 11,618 (−394)。
- Random: wins 50 → 50 (±0), avg_steps 12,831 → 13,005 (+174)。
- Feeder: wins 0 → 0 (±0), avg_steps 9,376 → 9,200 (−176)。
[2026-01-09 23:29:03] model=models\takeishi_ep125000.pt episodes=50 Opponent=claude Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=12309
[2026-01-09 23:30:48] model=models\takeishi_ep125000.pt episodes=50 Opponent=economist Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=18052
[2026-01-09 23:31:50] model=models\takeishi_ep125000.pt episodes=50 Opponent=random Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=12915
[2026-01-09 23:34:15] model=models\takeishi_ep125000.pt episodes=50 Opponent=splitpush Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=16858
[2026-01-09 23:35:46] model=models\takeishi_ep125000.pt episodes=50 Opponent=harasser Summary: wins=28/50 draws=0 losses=22 timeouts=0 avg_steps=15744
[2026-01-09 23:36:51] model=models\takeishi_ep125000.pt episodes=50 Opponent=bulwark Summary: wins=1/50 draws=0 losses=49 timeouts=0 avg_steps=12307
[2026-01-09 23:46:40] model=models\takeishi_ep125000.pt episodes=50 Opponent=anchor Summary: wins=8/50 draws=0 losses=42 timeouts=13 avg_steps=25314
[2026-01-09 23:47:33] model=models\takeishi_ep125000.pt episodes=50 Opponent=feeder Summary: wins=0/50 draws=0 losses=50 timeouts=0 avg_steps=9510
[2026-01-09 23:48:35] model=models\takeishi_ep125000.pt episodes=50 Opponent=rusher Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=12983
[2026-01-09 23:49:57] model=models\takeishi_ep125000.pt episodes=50 Opponent=opportunist Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=15502
[2026-01-09 23:51:34] model=models\takeishi_ep125000.pt episodes=50 Opponent=counter Summary: wins=32/50 draws=0 losses=18 timeouts=0 avg_steps=15644
[2026-01-09 23:55:55] model=models\takeishi_ep125000.pt episodes=50 Opponent=flow Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=19873
[2026-01-10 11:09:41] model=models\takeishi_ep130000.pt episodes=50 Opponent=claude Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=11985
[2026-01-10 11:11:16] model=models\takeishi_ep130000.pt episodes=50 Opponent=economist Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=17222
[2026-01-10 11:12:17] model=models\takeishi_ep130000.pt episodes=50 Opponent=random Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=13007
[2026-01-10 11:14:29] model=models\takeishi_ep130000.pt episodes=50 Opponent=splitpush Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=16577
[2026-01-10 11:15:53] model=models\takeishi_ep130000.pt episodes=50 Opponent=harasser Summary: wins=25/50 draws=0 losses=25 timeouts=0 avg_steps=15040
[2026-01-10 11:16:58] model=models\takeishi_ep130000.pt episodes=50 Opponent=bulwark Summary: wins=3/50 draws=0 losses=47 timeouts=0 avg_steps=12608
[2026-01-10 11:26:39] model=models\takeishi_ep130000.pt episodes=50 Opponent=anchor Summary: wins=12/50 draws=0 losses=38 timeouts=13 avg_steps=25338
[2026-01-10 11:27:28] model=models\takeishi_ep130000.pt episodes=50 Opponent=feeder Summary: wins=0/50 draws=0 losses=50 timeouts=0 avg_steps=9379
[2026-01-10 11:28:26] model=models\takeishi_ep130000.pt episodes=50 Opponent=rusher Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=13185
[2026-01-10 11:29:39] model=models\takeishi_ep130000.pt episodes=50 Opponent=opportunist Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=14391
[2026-01-10 11:31:07] model=models\takeishi_ep130000.pt episodes=50 Opponent=counter Summary: wins=27/50 draws=0 losses=23 timeouts=0 avg_steps=15300
[2026-01-10 11:34:43] model=models\takeishi_ep130000.pt episodes=50 Opponent=flow Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=19258
[2026-01-10 13:46:12] model=models\takeishi_ep126000.pt episodes=50 Opponent=claude Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=11657
[2026-01-10 13:47:56] model=models\takeishi_ep126000.pt episodes=50 Opponent=economist Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=18119
[2026-01-10 13:49:03] model=models\takeishi_ep126000.pt episodes=50 Opponent=random Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=13177
[2026-01-10 13:51:31] model=models\takeishi_ep126000.pt episodes=50 Opponent=splitpush Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=16954
[2026-01-10 13:52:59] model=models\takeishi_ep126000.pt episodes=50 Opponent=harasser Summary: wins=28/50 draws=0 losses=22 timeouts=0 avg_steps=15037
[2026-01-10 13:54:06] model=models\takeishi_ep126000.pt episodes=50 Opponent=bulwark Summary: wins=1/50 draws=0 losses=49 timeouts=0 avg_steps=12498
[2026-01-10 14:02:16] model=models\takeishi_ep126000.pt episodes=50 Opponent=anchor Summary: wins=12/50 draws=0 losses=38 timeouts=9 avg_steps=23704
[2026-01-10 14:03:08] model=models\takeishi_ep126000.pt episodes=50 Opponent=feeder Summary: wins=0/50 draws=0 losses=50 timeouts=0 avg_steps=9453
[2026-01-10 14:04:13] model=models\takeishi_ep126000.pt episodes=50 Opponent=rusher Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=13183
[2026-01-10 14:05:33] model=models\takeishi_ep126000.pt episodes=50 Opponent=opportunist Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=14730
[2026-01-10 14:07:02] model=models\takeishi_ep126000.pt episodes=50 Opponent=counter Summary: wins=23/50 draws=0 losses=27 timeouts=0 avg_steps=14959
[2026-01-10 14:11:19] model=models\takeishi_ep126000.pt episodes=50 Opponent=flow Summary: wins=50/50 draws=0 losses=0 timeouts=0 avg_steps=20171
