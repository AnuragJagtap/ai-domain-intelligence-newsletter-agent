from groq import Groq
from config.settings import GROQ_API_KEY
import json


class PlannerAgent:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def plan(self, goal, state, tools):

        prompt = f"""
You are an autonomous AI planner.

Your job is to COMPLETE the goal step-by-step.

Goal:
{goal}

You MUST follow this workflow:
1. fetch → get data
2. filter → remove irrelevant data
3. summarize → generate insights
4. learn → generate learning recommendations
5. stop → ONLY when everything is done

Current State:
{state}

Available Tools:
{tools}

Rules:
- Do NOT stop early
- Only choose "stop" if final output exists
- Always pick the NEXT missing step

Return ONLY JSON:
{{
  "action": "fetch | filter | summarize | learn | stop",
  "reason": "short explanation"
}}
"""
        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        text = response.choices[0].message.content.strip()

        try:
            return json.loads(text)
        except:
            return {"action": "fetch"}