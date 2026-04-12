import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
#SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

DEFAULT_DOMAIN = os.getenv("DEFAULT_DOMAIN", "Artificial Intelligence")
MAX_ARTICLES = int(os.getenv("MAX_ARTICLES", 10))