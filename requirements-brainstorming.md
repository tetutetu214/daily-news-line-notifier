# Daily News LINE Notifier - 要件壁打ち資料

## プロジェクト方針

**2つの独立したアプリとして開発する：**

| # | アプリ | 目的 |
|---|--------|------|
| A | **AI論文レコメンダー** | arXiv論文の当たり外れ問題を解決。注目度の高い論文だけを毎日通知 |
| B | **AWSニュース通知** | AWS最新情報を毎日通知（既存 `aws_get_rss.py` の発展版）※後日着手 |

### 決定済み事項

| 項目 | 決定 |
|------|------|
| 先に作るもの | **AI論文レコメンダー** |
| 通知手段 | **LINE Messaging API**（既に利用中） |
| 実行環境 | **GitHub Actions (cron)** |
| 土日の通知 | **土日は通知なし**（HF Daily Papersが平日のみ更新のため） |

---

# A. AI論文レコメンダー（実装対象）

## 1. 解決したい課題

- arXiv（例: [The Illusion of Thinking](https://arxiv.org/abs/2506.06941)）を毎日見ているが**当たり外れが大きい**
- 数百件/日の新着論文から良い論文を自力で選ぶのは非効率
- **コミュニティが評価した注目論文だけ**をLINEで受け取りたい

## 2. データソース: Hugging Face Daily Papers API

```
GET https://huggingface.co/api/daily_papers?limit=100
```

- 認証不要
- **平日（月〜金）毎日更新**（土日は更新なし）
- AK氏とコミュニティ研究者がキュレーション（年間3,700本以上、購読者12,000人超）
- **投稿から7日以内の論文のみ**掲載 → 古い論文が残り続けることはない
- arXiv IDが含まれるため、arXivの論文詳細ページへのリンクも生成可能

### 他ソース比較（参考）

| ソース | API | 人気度指標 | 特徴 |
|--------|-----|-----------|------|
| **HF Daily Papers** | `huggingface.co/api/daily_papers` | **upvote数** | **採用** |
| Semantic Scholar | `api.semanticscholar.org` | 被引用数 | 速報性に欠ける |
| Papers With Code | Web / API | Star数 | コード付き論文に強い |
| Reddit r/MachineLearning | Reddit API | upvote数 | ノイズも多い |

### APIのソート方式

| ソート | ロジック | 用途 |
|--------|---------|------|
| **Hot** | `upvotes / (経過時間+2)^1.5` | 今まさに話題の論文（**採用**） |
| New | `publishedAt`順 | 最新投稿順 |
| Rising | `upvotes / (経過時間+1)` | 急上昇中の論文 |

→ **Hot** を使えば「今日upvoteが集まっている論文Top5」が取れ、毎日異なる結果になる。

### 土日の扱い

HF Daily Papersは土日更新なし → **土日は通知しない**。

## 3. アーキテクチャ

```
[HF Daily Papers API] ──取得──→ [論文データ(JSON)]
  (sort=hot)                           │
                                  Hotスコア順Top5抽出
                                       │
                               [LINE Messaging API]
                                       │
                                  Push通知 → 📱 (毎日)
```

## 4. 通知メッセージフォーマット案

```
🧠 今日のAI注目論文 Top5 (2026-03-21)

1. ⬆️ 285 | The Illusion of Thinking: Understanding
   the Strengths and Limitations of Reasoning Models
   📄 https://arxiv.org/abs/2506.06941

2. ⬆️ 142 | [論文タイトル]
   📄 https://arxiv.org/abs/xxxx.xxxxx

3. ⬆️ 98 | [論文タイトル]
   📄 https://arxiv.org/abs/xxxx.xxxxx

4. ⬆️ 76 | [論文タイトル]
   📄 https://arxiv.org/abs/xxxx.xxxxx

5. ⬆️ 51 | [論文タイトル]
   📄 https://arxiv.org/abs/xxxx.xxxxx
```

### 拡張案: 日本語要約の付加（将来Phase）

```
1. ⬆️ 285 | The Illusion of Thinking
   💡 推論モデルのCoTは問題が複雑になると急激に性能低下する
      ことをパズル環境で実証した研究
   📄 https://arxiv.org/abs/2506.06941
```

→ Claude API / OpenAI API でabstractを日本語1行要約する（Phase2以降）

## 5. 対象カテゴリのフィルタリング

HF Daily PapersはML/AI全般をカバー。MVP段階ではフィルタなし。

| フィルタ方法 | 実装 | 備考 |
|-------------|------|------|
| フィルタなし（全体Top5） | そのまま | **MVP採用**（シンプル） |
| arXivカテゴリで絞る | `cs.AI`, `cs.CL`, `cs.LG` | Phase2で必要なら追加 |
| キーワードで絞る | `LLM`, `transformer`, etc. | Phase2で必要なら追加 |

---

## 6. 技術スタック

```
言語:        Python 3.12
パッケージ:
  - requests          ... HF API / LINE API 呼び出し
  - python-dotenv     ... 環境変数管理（ローカル実行時）

実行環境:    GitHub Actions (cron)
通知:        LINE Messaging API（既に利用中）
```

## 7. ディレクトリ構成

```
daily-news-line-notifier/
├── requirements-brainstorming.md   # この壁打ち資料
├── requirements.txt                # 依存パッケージ
│
├── ai_papers/                      # AI論文レコメンダー
│   ├── main.py                     #   エントリポイント
│   ├── hf_daily_papers.py          #   HF Daily Papers API取得・ランキング
│   └── line_notify.py              #   LINE Messaging API送信
│
└── .github/
    └── workflows/
        └── ai-papers.yml           # 定期実行（毎日）
```

## 8. 必要な外部設定

| サービス | 必要なもの | 備考 |
|----------|-----------|------|
| LINE Messaging API | Channel Access Token + User ID | 既に利用中 |
| HF Daily Papers API | 不要（認証なし） | |
| GitHub Secrets | `LINE_CHANNEL_ACCESS_TOKEN`, `LINE_USER_ID` | リポジトリSettings → Secrets |

## 9. GitHub Actions ワークフロー

```yaml
# .github/workflows/ai-papers.yml
name: AI Papers Daily Notifier

on:
  schedule:
    - cron: '0 22 * * 0-4'  # JST 07:00（月〜金のみ）
  workflow_dispatch:       # 手動実行も可能

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r daily-news-line-notifier/requirements.txt
      - run: python daily-news-line-notifier/ai_papers/main.py
        env:
          LINE_CHANNEL_ACCESS_TOKEN: ${{ secrets.LINE_CHANNEL_ACCESS_TOKEN }}
          LINE_USER_ID: ${{ secrets.LINE_USER_ID }}
```

---

## 10. MVP → Phase計画

### Phase 1: MVP（今回実装）

- HF Daily Papers API → Hotソート → Top5 → LINE通知
- GitHub Actionsで毎朝7時(JST)に定期実行（月〜金のみ）
- `workflow_dispatch` で手動テスト実行も可能

### Phase 2: 精度向上

- arXivカテゴリフィルタ追加（cs.AI, cs.CL等）
- 重複排除（前日送った論文は除外）
- エラーハンドリング強化（API障害時のリトライ等）

### Phase 3: リッチ化

- Claude API / OpenAI APIで論文abstractを日本語1行要約
- Flex Message（LINE）でリッチなカード表示
- LINEから「もっと見る」で追加論文を返す双方向Bot化

---

# B. AWSニュース通知（後日着手）

既存の `aws_get_rss.py` をベースに、LINE Messaging API対応 + GitHub Actions化。
詳細はAI論文レコメンダー完成後に設計する。

---

## 次のアクション

**すべての要件が確定。Phase1の実装に着手可能。**

実装タスク：
1. `ai_papers/hf_daily_papers.py` - HF Daily Papers API取得・Top5抽出
2. `ai_papers/line_notify.py` - LINE Messaging API送信
3. `ai_papers/main.py` - エントリポイント
4. `requirements.txt` - 依存パッケージ
5. `.github/workflows/ai-papers.yml` - 定期実行ワークフロー
6. GitHub SecretsにLINEトークン設定（ユーザー作業）
