from agents.news_agent import NewsAgent
from agents.research_agent import ResearchAgent
from agents.filter_agent import FilterAgent
from agents.summarizer_agent import SummarizerAgent
from config.settings import DEFAULT_DOMAIN


class UnifiedPipeline:
    def __init__(self):
        self.news_agent = NewsAgent()
        self.research_agent = ResearchAgent()
        self.filter_agent = FilterAgent()
        self.summarizer_agent = SummarizerAgent()

    def run(self, domain: str = DEFAULT_DOMAIN):
        print(f"\n🚀 Running Unified Pipeline for: {domain}\n")

        # -------------------------------
        # Step 1: Data Ingestion
        # -------------------------------
        news = self.news_agent.fetch_news(domain)
        papers = self.research_agent.fetch_papers(domain)

        print(f"📰 News fetched: {len(news)}")
        print(f"📄 Papers fetched: {len(papers)}")

        # -------------------------------
        # Step 2: Normalize (Unified Schema)
        # -------------------------------
        combined = self._normalize(news, papers)

        print(f"📊 Total combined items: {len(combined)}")

        # -------------------------------
        # Step 3: Semantic Filtering
        # -------------------------------
        filtered = self.filter_agent.filter_relevant(
            combined,
            query=domain,
            top_k=8
        )

        print(f"✅ After filtering: {len(filtered)}")

        # -------------------------------
        # Step 4: Summarization + Insight Generation
        # -------------------------------
        summarized = self.summarizer_agent.summarize(filtered)
        print(f"🧠 Summarized items: {len(summarized)}")

        return summarized

    def _normalize(self, news, papers):
        """
        Convert heterogeneous data into unified schema
        """

        normalized = []

        # 📰 News → Unified Schema
        for article in news:
            normalized.append({
                "type": "news",
                "title": article.get("title", ""),
                "content": article.get("description", ""),
                "source": article.get("source", ""),
                "url": article.get("url", "")
            })

        # 📄 Research → Unified Schema
        for paper in papers:
            normalized.append({
                "type": "research",
                "title": paper.get("title", ""),
                "content": paper.get("summary", ""),
                "source": "arXiv",
                "url": paper.get("link", "")
            })

        return normalized