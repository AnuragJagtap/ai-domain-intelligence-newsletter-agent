from groq import Groq
from typing import List, Dict
from config.settings import GROQ_API_KEY
import json
import re
import time


class LearningAgent:
    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("❌ GROQ_API_KEY not found")

        self.client = Groq(api_key=GROQ_API_KEY)

    def generate_learning(self, items: List[Dict]) -> List[Dict]:

        results = []

        for item in items:
            try:
                learning_data = self._generate_single(item)

                results.append({
                    **item,
                    "learning": learning_data
                })

                time.sleep(1)

            except Exception as e:
                print(f"❌ Learning agent error: {e}")

                # 🔥 Fallback
                results.append({
                    **item,
                    "learning": {
                        "concepts": ["Explore topic manually"],
                        "resources": ["Search on Google"],
                        "next_steps": ["Read more about this topic"]
                    }
                })

        return results

    def _generate_single(self, item: Dict) -> Dict:

        prompt = f"""
You are an AI mentor.

Based on the following content, suggest:

1. Key concepts to learn
2. Useful resources/topics
3. Practical next steps

Content:
Title: {item.get('title')}
Summary: {item.get('summary')}

Return ONLY JSON:
{{
  "concepts": ["..."],
  "resources": ["..."],
  "next_steps": ["..."]
}}

Respond in English only. Do not include markdown.
"""

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a precise AI mentor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        text = response.choices[0].message.content.strip()

        return self._parse_response(text)

    def _parse_response(self, text: str) -> Dict:
        try:
            cleaned = re.sub(r"```json|```", "", text).strip()
            json_match = re.search(r"\{.*\}", cleaned, re.DOTALL)

            if json_match:
                data = json.loads(json_match.group())

                return {
                    "concepts": data.get("concepts", []),
                    "resources": data.get("resources", []),
                    "next_steps": data.get("next_steps", [])
                }

            raise ValueError("Invalid JSON")

        except:
            return {
                "concepts": ["Explore topic"],
                "resources": ["Search online"],
                "next_steps": ["Study fundamentals"]
            }