"""Hugging Face Daily Papers API からHotな論文Top5を取得する."""

import requests

HF_API_URL = "https://huggingface.co/api/daily_papers"
TOP_N = 5


def fetch_top_papers(limit: int = 100) -> list[dict]:
    """HF Daily Papers APIからHotソートでTop5論文を取得する.

    Returns:
        list[dict]: 各要素は title, upvotes, arxiv_url を持つ辞書
    """
    resp = requests.get(HF_API_URL, params={"limit": limit}, timeout=30)
    resp.raise_for_status()

    papers_raw = resp.json()

    papers = []
    for item in papers_raw[:TOP_N]:
        paper = item.get("paper", {})
        arxiv_id = paper.get("id", "")
        title = paper.get("title", "No Title")
        upvotes = item.get("paper", {}).get("upvotes", 0)

        papers.append({
            "title": title,
            "upvotes": upvotes,
            "arxiv_url": f"https://arxiv.org/abs/{arxiv_id}",
        })

    return papers
