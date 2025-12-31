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
