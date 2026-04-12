from agents.news_agent import NewsAgent
from agents.research_agent import ResearchAgent
from config.settings import DEFAULT_DOMAIN


if __name__ == "__main__":
    news_agent = NewsAgent()
    research_agent = ResearchAgent()

    print(f"\n🔍 Fetching data for: {DEFAULT_DOMAIN}\n")

    # News
    news = news_agent.fetch_news(DEFAULT_DOMAIN)

    print("\n📰 News Articles:\n")
    for i, article in enumerate(news[:3], 1):
        print(f"{i}. {article['title']}")

    # Research
    papers = research_agent.fetch_papers(DEFAULT_DOMAIN)

    print("\n📄 Research Papers:\n")
    for i, paper in enumerate(papers[:3], 1):
        print(f"{i}. {paper['title']}")
        print(f"   Authors: {', '.join(paper['authors'][:3])}")
        print("-" * 50)