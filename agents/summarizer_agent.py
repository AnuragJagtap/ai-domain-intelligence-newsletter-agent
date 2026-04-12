from groq import Groq
from typing import List, Dict
import re
from sympy import re
from config.settings import GROQ_API_KEY
import json
import time


class SummarizerAgent:
    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("❌ GROQ_API_KEY not found")

        self.client = Groq(api_key=GROQ_API_KEY)

    def summarize(self, items: List[Dict]) -> List[Dict]:

        results = []

        for item in items:
            try:
                summary_data = self._summarize_single(item)

                results.append({
                    **item,
                    "summary": summary_data["summary"],
                    "insight": summary_data["insight"]
                })

                time.sleep(1)  # avoid rate limits

            except Exception as e:
                print(f"❌ Error summarizing: {e}")

                # 🔥 Fallback (VERY IMPORTANT)
                results.append({
                    **item,
                    "summary": item.get("content", "")[:200],
                    "insight": "Fallback summary due to API issue"
                })

        return results

    def _summarize_single(self, item: Dict) -> Dict:

        prompt = f"""
You are an AI research assistant.

Analyze the following content and generate:

1. A concise summary (2-3 lines)
2. Why this is important (impact or insight)

Content:
Title: {item.get('title')}
Text: {item.get('content')}

Return ONLY valid JSON with keys "summary" and "insight".
Do NOT include markdown, code blocks, or explanations.:
{{
  "summary": "...",
  "insight": "..."
}}
"""

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a precise AI analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        text = response.choices[0].message.content.strip()

        return self._parse_response(text)

    def _parse_response(self, text: str) -> Dict:
        import json
        import re

        try:
        # 🔹 Remove markdown/code blocks
            cleaned = re.sub(r"```json|```", "", text).strip()

        # 🔹 Extract JSON part
            json_match = re.search(r"\{.*\}", cleaned, re.DOTALL)

            if json_match:
                data = json.loads(json_match.group())

                return {
                "summary": data.get("summary", "").strip(),
                "insight": data.get("insight", "").strip()
                }

            raise ValueError("No JSON found")

        except Exception:
        # 🔥 Intelligent fallback
            return {
            "summary": cleaned[:200],
            "insight": "Key takeaway extraction unavailable"
            }