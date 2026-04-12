import feedparser
from typing import List, Dict
from urllib.parse import urlencode
from config.settings import MAX_ARTICLES


class ResearchAgent:
    BASE_URL = "http://export.arxiv.org/api/query"

    def fetch_papers(self, domain: str) -> List[Dict]:

        query = f"(cat:cs.AI OR cat:cs.LG) AND all:{domain}"

        params = {
            "search_query": query,
            "start": 0,
            "max_results": MAX_ARTICLES,
            "sortBy": "lastUpdatedDate"
        }

        url = f"{self.BASE_URL}?{urlencode(params)}"

        try:
            feed = feedparser.parse(url)

            if not feed.entries:
                print("⚠️ No research papers found")
                return []

            return self._parse_entries(feed.entries)

        except Exception as e:
            print(f"❌ Error fetching research papers: {e}")
            return []

    def _parse_entries(self, entries) -> List[Dict]:
        """
        Clean and structure arXiv response
        """

        papers = []

        for entry in entries:
            paper = {
                "title": entry.title,
                "summary": entry.summary,
                "authors": [author.name for author in entry.authors],
                "link": entry.link,
                "published": entry.published
            }

            papers.append(paper)

        return papers