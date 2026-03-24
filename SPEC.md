# SPEC.md - daily-news-line-notifier

## 全体構成

```
daily-news-line-notifier/
├── .github/workflows/ai-papers.yml   # GitHub Actions定義
├── ai_papers/
│   ├── main.py                        # エントリポイント
│   ├── hf_daily_papers.py            # HF API連携
│   └── line_notify.py                # LINE通知
├── requirements.txt
├── .gitignore
├── PLAN.md
├── SPEC.md
└── TODO.md
```

## 技術仕様

| 項目 | 内容 |
|---|---|
| データソース | Hugging Face Daily Papers API（認証不要） |
| 通知先 | LINE Messaging API（Push Message） |
| スケジュール | 月〜金 JST 07:00（cron: `0 22 * * 0-4`） |
| Python | 3.12 |
| 依存パッケージ | requests>=2.31.0, python-dotenv>=1.0.0 |

## GitHub Secrets（必須）

| Secret名 | 内容 |
|---|---|
| LINE_CHANNEL_ACCESS_TOKEN | LINE Messaging APIのチャネルアクセストークン |
| LINE_USER_ID | 通知先のLINEユーザーID |

## 処理フロー

1. HF Daily Papers APIから最新論文を取得（limit=100）
2. upvotesでソート済み（API側）のTop5を抽出
3. タイトル・upvote数・arXivリンクでメッセージ組み立て
4. LINE Messaging APIでプッシュ通知

## やること・やらないこと

### Phase 1（現在・完了）
- [x] HF Daily Papers APIからTop5取得
- [x] LINE Messaging APIでプッシュ通知
- [x] GitHub Actionsで定期実行

### Phase 2（将来）
- カテゴリフィルタリング
- 重複排除
- エラーハンドリング強化

### Phase 3（将来）
- Claude/OpenAI APIによる日本語要約
