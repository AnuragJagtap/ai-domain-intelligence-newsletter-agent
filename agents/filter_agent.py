from sentence_transformers import SentenceTransformer
import numpy as np


class FilterAgent:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def filter_relevant(self, articles, query, top_k=5):
        """
        Filters top_k most relevant articles using semantic similarity
        """

        if not articles:
            return []

        query_embedding = self.model.encode(query)

        scores = []

        for article in articles:
            text = article["title"] + " " + article.get("content", "")
            article_embedding = self.model.encode(text)

            similarity = self._cosine_similarity(query_embedding, article_embedding)

            scores.append((similarity, article))

        # Sort by similarity (highest first)
        scores.sort(key=lambda x: x[0], reverse=True)

        return [article for _, article in scores[:top_k]]

    def _cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))