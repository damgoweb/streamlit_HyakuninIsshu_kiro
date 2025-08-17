# Design Document

## Overview

百人一首ゲームは、Streamlitを使用したWebアプリケーションとして実装します。JSONデータから百人一首の情報を読み込み、複数のゲームモードを提供する学習支援ツールです。シンプルで直感的なUIと、日本の古典文学に適した和風デザインを採用します。

## Architecture

### システム構成
```
hyakunin_isshu_game.py (メインアプリケーション)
├── データ層: data/hyakunin_isshu.json
├── ビジネスロジック層: ゲーム管理、問題生成、スコア管理
├── プレゼンテーション層: Streamlit UI コンポーネント
└── 状態管理: Streamlit Session State
```

### データフロー
1. アプリ起動時にJSONデータを読み込み
2. ユーザーがゲームモードを選択
3. ランダムに問題を生成し、選択肢を作成
4. ユーザーの回答を処理し、結果を表示
5. スコアを更新し、次の問題へ進行

## Components and Interfaces

### 1. データ管理コンポーネント
```python
class HyakuninIsshuData:
    def __init__(self, json_path: str)
    def load_data(self) -> List[Dict]
    def get_random_poem(self) -> Dict
    def get_random_poems(self, count: int) -> List[Dict]
```

### 2. ゲーム管理コンポーネント
```python
class GameManager:
    def __init__(self, data: HyakuninIsshuData)
    def generate_lower_verse_question(self) -> Dict
    def generate_author_question(self) -> Dict
    def check_answer(self, user_answer: str, correct_answer: str) -> bool
    def update_score(self, is_correct: bool)
    def reset_game(self)
```

### 3. UI コンポーネント
```python
def render_header()
def render_sidebar()
def render_game_area(game_mode: str)
def render_question_display(question_data: Dict)
def render_choices(choices: List[str])
def render_result(is_correct: bool, poem_data: Dict)
def render_score_display()
```

### 4. 状態管理
Streamlit Session Stateを使用して以下の状態を管理：
- `current_poem`: 現在の問題の歌データ
- `game_mode`: 選択されたゲームモード
- `score`: 正解数
- `total_questions`: 総問題数
- `show_result`: 結果表示フラグ
- `user_answer`: ユーザーの回答
- `question_data`: 現在の問題データ

## Data Models

### 歌データモデル
```python
@dataclass
class Poem:
    id: int
    author: str
    upper: str  # 上の句
    lower: str  # 下の句
    reading_upper: str  # 上の句読み
    reading_lower: str  # 下の句読み
    description: str  # 解説
```

### 問題データモデル
```python
@dataclass
class Question:
    poem: Poem
    question_text: str  # 問題文（上の句 or 全句）
    choices: List[str]  # 選択肢
    correct_answer: str  # 正解
    question_type: str  # "lower_verse" or "author"
```

### スコアデータモデル
```python
@dataclass
class Score:
    correct: int
    total: int
    
    @property
    def percentage(self) -> float:
        return (self.correct / self.total * 100) if self.total > 0 else 0
```

## Error Handling

### データ読み込みエラー
- JSONファイルが見つからない場合: エラーメッセージを表示し、アプリを停止
- JSONデータが不正な場合: エラーメッセージを表示し、デフォルトデータを使用

### ゲーム実行エラー
- 選択肢生成時のエラー: 再試行またはスキップ
- 状態管理エラー: セッション状態をリセット

### UI表示エラー
- 文字化けや表示崩れ: UTF-8エンコーディングを確保
- レスポンシブ対応: モバイル表示での崩れを防止

## Testing Strategy

### 単体テスト
- データ読み込み機能のテスト
- 問題生成ロジックのテスト
- スコア計算機能のテスト
- 回答判定機能のテスト

### 統合テスト
- ゲームフロー全体のテスト
- 状態管理の整合性テスト
- UI操作とデータ更新の連携テスト

### ユーザビリティテスト
- 直感的な操作性の確認
- 和風デザインの適切性
- レスポンシブデザインの動作確認

### パフォーマンステスト
- 大量データ読み込み時の応答性
- 連続操作時のメモリ使用量
- ページ読み込み速度の測定

## UI/UX Design Specifications

### カラーパレット
- プライマリ: 深い藍色 (#1e3a8a)
- セカンダリ: 金色 (#fbbf24)
- 成功: 緑色 (#10b981)
- エラー: 赤色 (#ef4444)
- 背景: 薄いベージュ (#fef7ed)

### タイポグラフィ
- 見出し: 大きめのフォントサイズ（24px-32px）
- 本文: 読みやすいサイズ（16px-18px）
- 和歌表示: 縦書き風の配置を意識した表示

### レイアウト
- サイドバー: ゲーム設定とスコア表示
- メインエリア: 問題表示と選択肢
- フッター: 解説と次の問題ボタン

### インタラクション
- ボタンホバー効果
- 選択時のフィードバック
- アニメーション効果（控えめ）