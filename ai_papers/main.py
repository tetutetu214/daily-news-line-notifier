"""AI論文レコメンダー - エントリポイント.

HF Daily PapersからHot論文Top5を取得し、LINE通知する.
"""

from datetime import datetime, timezone, timedelta

from hf_daily_papers import fetch_top_papers
from line_notify import send_line_message

JST = timezone(timedelta(hours=9))


def build_message(papers: list[dict]) -> str:
    """論文リストからLINE通知用メッセージを組み立てる."""
    today = datetime.now(JST).strftime("%Y-%m-%d")
    lines = [f"🧠 今日のAI注目論文 Top5 ({today})", ""]

    for i, paper in enumerate(papers, 1):
        lines.append(
            f"{i}. ⬆️ {paper['upvotes']} | {paper['title']}"
        )
        lines.append(f"   📄 {paper['arxiv_url']}")
        lines.append("")

    return "\n".join(lines).rstrip()


def main() -> None:
    papers = fetch_top_papers()

    if not papers:
        print("No papers found. Skipping notification.")
        return

    message = build_message(papers)
    print(message)
    print("---")

    send_line_message(message)
    print("LINE notification sent successfully.")


if __name__ == "__main__":
    main()
