from agents.news_agent import NewsAgent
from agents.research_agent import ResearchAgent
from agents.filter_agent import FilterAgent
from agents.summarizer_agent import SummarizerAgent
from agents.learning_agent import LearningAgent


news_agent = NewsAgent()
research_agent = ResearchAgent()
filter_agent = FilterAgent()
summarizer_agent = SummarizerAgent()
learning_agent = LearningAgent()


def fetch_data(domain):
    news = news_agent.fetch_news(domain)
    papers = research_agent.fetch_papers(domain)

    combined = []

    for n in news:
        combined.append({"title": n["title"], "content": n["description"]})

    for p in papers:
        combined.append({"title": p["title"], "content": p["summary"]})

    return combined


def filter_data(data):
    return filter_agent.filter_relevant(data, "Artificial Intelligence", 8)


def summarize_data(data):
    return summarizer_agent.summarize(data)


def learning_data(data):
    return learning_agent.generate_learning(data)