# 百人一首ゲーム (Hyakunin Isshu Game)

百人一首の和歌を使った学習・練習ゲームです。Streamlitを使用したWebアプリケーションとして実装されています。

## 機能

- 上の句から下の句を選ぶゲーム
- 作者名を当てるゲーム
- スコア管理機能
- 和風デザインのUI

## セットアップ

1. 仮想環境の作成と有効化:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# または
venv\Scripts\activate  # Windows
```

2. 依存関係のインストール:
```bash
pip install -r requirements.txt
```

3. アプリケーションの実行:
```bash
streamlit run hyakunin_isshu_game.py
```

## データ構造

- `data/hyakunin_isshu.json`: 百人一首の歌データ
- 各歌には以下の情報が含まれます:
  - id: 歌番号
  - author: 作者名
  - upper: 上の句
  - lower: 下の句
  - reading_upper: 上の句の読み方
  - reading_lower: 下の句の読み方
  - description: 歌の解説

## 開発状況

現在、プロジェクトの基盤とデータ構造の実装が完了しています。