import requests
from typing import List, Dict
from config.settings import NEWS_API_KEY, MAX_ARTICLES


class NewsAgent:
    BASE_URL = "https://newsapi.org/v2/everything"

    def __init__(self):
        if not NEWS_API_KEY:
            raise ValueError("❌ NEWS_API_KEY is missing in .env")

    def fetch_news(self, domain: str) -> List[Dict]:
        """
        Fetch news articles based on domain/topic.
        """

        params = {
            "q": domain,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": MAX_ARTICLES,
            "apiKey": NEWS_API_KEY
        }

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)

            if response.status_code != 200:
                raise Exception(f"API Error: {response.status_code} - {response.text}")

            data = response.json()

            if data.get("status") != "ok":
                raise Exception(f"API returned error: {data}")

            return self._parse_articles(data.get("articles", []))

        except requests.exceptions.Timeout:
            print("⏱️ Request timed out")
            return []

        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return []

        except Exception as e:
            print(f"❌ Error fetching news: {e}")
            return []

    def _parse_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Clean and structure raw API response.
        """

        cleaned_articles = []

        for article in articles:
            if not article.get("title") or not article.get("description"):
                continue  # skip incomplete data

            cleaned_articles.append({
                "title": article["title"],
                "description": article["description"],
                "content": article.get("content"),
                "url": article["url"],
                "source": article["source"]["name"],
                "published_at": article["publishedAt"]
            })

        return cleaned_articles