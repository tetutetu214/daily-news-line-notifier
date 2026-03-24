# TODO.md - daily-news-line-notifier

## Phase 1: AI論文レコメンダー（基本機能）

- [x] HF Daily Papers API連携（hf_daily_papers.py）
- [x] LINE Messaging API通知（line_notify.py）
- [x] エントリポイント（main.py）
- [x] GitHub Actions ワークフロー作成
- [x] .gitignore 設定
- [x] 新リポジトリ作成・push
- [ ] GitHub Secretsの登録（LINE_CHANNEL_ACCESS_TOKEN, LINE_USER_ID）
- [ ] workflow_dispatch で手動実行テスト

## Phase 2: 機能強化（未着手）

- [ ] カテゴリフィルタリング
- [ ] 重複排除（同じ論文を2日連続で通知しない）
- [ ] エラーハンドリング強化（API障害時のリトライ等）

## Phase 3: AI要約（未着手）

- [ ] Claude/OpenAI APIによる日本語要約機能
