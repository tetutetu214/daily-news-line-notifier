# PLAN.md - daily-news-line-notifier

## きっかけ

毎朝、AI/ML分野の注目論文をキャッチアップしたい。
Hugging Faceで話題の論文を自動で拾ってLINEに通知してくれる仕組みがあれば、通勤中にサクッと確認できる。

## やりたいこと

- Hugging Face Daily Papers APIからHotな論文Top5を毎朝取得
- LINE Messaging APIで自分に通知
- GitHub Actionsで月〜金の朝7時（JST）に自動実行
- 将来的にはカテゴリフィルタや日本語要約も追加したい

## ゴールのイメージ

- 平日朝7時にLINEに「今日のAI注目論文 Top5」が届く
- 各論文のタイトル・upvote数・arXivリンクが一目でわかる
- workflow_dispatchで手動実行もできる
