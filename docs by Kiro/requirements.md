# Requirements Document

## Introduction

百人一首の和歌を使った学習・練習ゲームをStreamlitで開発します。ユーザーが上の句を見て下の句を選択したり、作者を当てたりする複数のゲームモードを提供し、日本の古典文学に親しみながら楽しく学習できるWebアプリケーションを作成します。

## Requirements

### Requirement 1

**User Story:** ユーザーとして、上の句から下の句を選ぶゲームをプレイしたい。正解・不正解の判定と解説を見て学習を深めたい。

#### Acceptance Criteria

1. WHEN ユーザーがゲームを開始する THEN システムは百人一首からランダムに1首を選択して上の句を表示する SHALL
2. WHEN 上の句が表示される THEN システムは正解の下の句を含む4つの選択肢を表示する SHALL
3. WHEN ユーザーが選択肢をクリックする THEN システムは正解・不正解を判定して結果を表示する SHALL
4. WHEN 正解・不正解が表示される THEN システムは該当する歌の作者、読み方、解説を表示する SHALL
5. WHEN 結果が表示される THEN システムは「次の問題」ボタンを表示する SHALL

### Requirement 2

**User Story:** ユーザーとして、作者名を当てるゲームもプレイしたい。和歌の知識を多角的に学習したい。

#### Acceptance Criteria

1. WHEN ユーザーが作者当てモードを選択する THEN システムは上の句と下の句を表示する SHALL
2. WHEN 歌が表示される THEN システムは正解の作者を含む4つの作者名選択肢を表示する SHALL
3. WHEN ユーザーが作者を選択する THEN システムは正解・不正解を判定して結果を表示する SHALL
4. WHEN 結果が表示される THEN システムは歌の読み方と解説を表示する SHALL

### Requirement 3

**User Story:** ユーザーとして、自分の学習進捗を把握したい。正解率や学習した歌の数を確認したい。

#### Acceptance Criteria

1. WHEN ユーザーがゲームをプレイする THEN システムは正解数と総問題数をカウントする SHALL
2. WHEN 問題に回答する THEN システムは正解率を計算して表示する SHALL
3. WHEN セッション中 THEN システムは現在の正解率をリアルタイムで更新表示する SHALL
4. WHEN ゲーム画面 THEN システムは現在のスコア（正解数/総問題数）を常に表示する SHALL

### Requirement 4

**User Story:** ユーザーとして、ゲームの難易度や設定を調整したい。自分のレベルに合わせて学習したい。

#### Acceptance Criteria

1. WHEN ユーザーがサイドバーを開く THEN システムはゲームモード選択オプションを表示する SHALL
2. WHEN ユーザーがゲームモードを変更する THEN システムは選択されたモードでゲームを開始する SHALL
3. WHEN ユーザーがリセットボタンを押す THEN システムはスコアと進捗をリセットする SHALL
4. WHEN アプリケーション起動時 THEN システムはデフォルトで「下の句当て」モードを選択する SHALL

### Requirement 5

**User Story:** ユーザーとして、美しく使いやすいインターフェースでゲームを楽しみたい。日本の古典的な雰囲気を感じたい。

#### Acceptance Criteria

1. WHEN アプリケーションが表示される THEN システムは和風のデザインテーマを適用する SHALL
2. WHEN 歌が表示される THEN システムは読みやすいフォントサイズと適切な行間で表示する SHALL
3. WHEN 選択肢が表示される THEN システムはボタンを見やすく配置する SHALL
4. WHEN 正解時 THEN システムは緑色で成功を示す SHALL
5. WHEN 不正解時 THEN システムは赤色で失敗を示し、正解を強調表示する SHALL