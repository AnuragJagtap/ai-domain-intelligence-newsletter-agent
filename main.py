from agents.news_agent import NewsAgent
from agents.research_agent import ResearchAgent
from agents.filter_agent import FilterAgent
from config.settings import DEFAULT_DOMAIN


def main():
    print(f"\n🚀 Running Test Pipeline for: {DEFAULT_DOMAIN}\n")

    # Initialize agents
    news_agent = NewsAgent()
    research_agent = ResearchAgent()
    filter_agent = FilterAgent()

    # Step 1: Fetch data
    news = news_agent.fetch_news(DEFAULT_DOMAIN)
    papers = research_agent.fetch_papers(DEFAULT_DOMAIN)

    print(f"📰 News fetched: {len(news)}")
    print(f"📄 Papers fetched: {len(papers)}")

    # Step 2: Normalize (important)
    combined = []

    for article in news:
        combined.append({
            "type": "news",
            "title": article["title"],
            "content": article["description"]
        })

    for paper in papers:
        combined.append({
            "type": "research",
            "title": paper["title"],
            "content": paper["summary"]
        })

    print(f"📊 Total combined items: {len(combined)}")

    # Step 3: Apply filtering
    filtered = filter_agent.filter_relevant(
        combined,
        query=DEFAULT_DOMAIN,
        top_k=5
    )

    print(f"\n✅ Filtered Results:\n")

    for i, item in enumerate(filtered, 1):
        print(f"{i}. [{item['type'].upper()}] {item['title']}")
        print(f"   {item['content'][:150]}...")
        print("-" * 60)


if __name__ == "__main__":
    main()