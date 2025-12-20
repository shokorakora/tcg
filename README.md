Territory Conquering Game
=========================
この実験では、陣取りゲームのAIプレイヤーを開発します。 

## 実験の準備

1. まずuvをインストールします。[uv](https://docs.astral.sh/uv/getting-started/installation/)を参考にしましょう。

2. リポジトリをクローンし、必要なライブラリをインストール:
```bash
git clone https://github.com/matt76k/tcg
cd tcg
uv sync
```

3. ゲームの実行:
```bash
uv run python src/main.py
```

## 実験内容

src/tcg/players以下のファイルを参考にして独自のAIプレイヤーを実装してください。

## トレーニングの方針と除外項目

- Takeishi の学習は `src/train_takeishi.py` を用います。
- 学習・評価では次の対戦相手のみを使用します: `ClaudePlayer`, `RandomPlayer`, `DefensiveEconomist`。
- 次のモジュール・フォルダは学習に使用しません（除外）:
	- `src/tcg/players/ml_player.py`
	- `src/tcg/players/players_kishida/`
- 旧来の `train_ml.py` は使用しません。

## 学習と評価の例

学習（例）:
```powershell
Push-Location "C:\Users\Owner\OneDrive\ドキュメント\情報電気電子工学創造実験\tcg"
$env:PYTHONPATH = (Resolve-Path ./src).Path
\.venv\Scripts\python.exe src\train_takeishi.py
Pop-Location
```

評価（例）:
```powershell
Push-Location "C:\Users\Owner\OneDrive\ドキュメント\情報電気電子工学創造実験\tcg"
$env:PYTHONPATH = (Resolve-Path ./src).Path
\.venv\Scripts\python.exe src\eval_takeishi.py --model models\takeishi_final.pt --episodes 100 --window False --opponent claude
\.venv\Scripts\python.exe src\eval_takeishi.py --model models\takeishi_final.pt --episodes 100 --window False --opponent economist
\.venv\Scripts\python.exe src\eval_takeishi.py --model models\takeishi_final.pt --episodes 100 --window False --opponent random
Pop-Location
```
