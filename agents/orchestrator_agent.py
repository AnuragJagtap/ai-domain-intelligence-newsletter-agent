from google.adk.agents import Agent
from agents.news_agent import NewsAgent
from agents.research_agent import ResearchAgent
from agents.filter_agent import FilterAgent
from agents.summarizer_agent import SummarizerAgent
from agents.learning_agent import LearningAgent


class OrchestratorAgent:
    def __init__(self):
        self.news_agent = NewsAgent()
        self.research_agent = ResearchAgent()
        self.filter_agent = FilterAgent()
        self.summarizer_agent = SummarizerAgent()
        self.learning_agent = LearningAgent()

    def run(self, domain: str):

        print(f"\n🚀 Running ADK Orchestrated Flow for: {domain}\n")

        # Step 1: Fetch
        news = self.news_agent.fetch_news(domain)
        papers = self.research_agent.fetch_papers(domain)

        # Step 2: Normalize
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

        # Step 3: Filter
        filtered = self.filter_agent.filter_relevant(combined, domain, top_k=8)

        # Step 4: Summarize
        summarized = self.summarizer_agent.summarize(filtered)

        # Step 5: Learning
        final = self.learning_agent.generate_learning(summarized)

        return final