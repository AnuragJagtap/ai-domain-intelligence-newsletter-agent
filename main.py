from agents.news_agent import NewsAgent
from config.settings import DEFAULT_DOMAIN


if __name__ == "__main__":
    agent = NewsAgent()

    news = agent.fetch_news(DEFAULT_DOMAIN)

    print(f"\n📰 Top News for: {DEFAULT_DOMAIN}\n")

    for i, article in enumerate(news, 1):
        print(f"{i}. {article['title']}")
        print(f"   {article['description']}")
        print(f"   Source: {article['source']}")
        print("-" * 50)