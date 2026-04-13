from agents.tools_registry import ToolRegistry
from agents.memory import AgentMemory
from agents.planner_agent import PlannerAgent
from agents.executor_agent import ExecutorAgent
from agents.tool_wrappers import (
    fetch_data,
    filter_data,
    summarize_data,
    learning_data
)


class AutonomousSystem:
    def __init__(self):
        self.memory = AgentMemory()
        self.tools = ToolRegistry()

        # 🔧 Register tools
        self.tools.register("fetch", fetch_data)
        self.tools.register("filter", filter_data)
        self.tools.register("summarize", summarize_data)
        self.tools.register("learn", learning_data)

        self.planner = PlannerAgent()
        self.executor = ExecutorAgent(self.tools, self.memory)

    def run(self, goal: str):
        """
        Autonomous loop with planner + guardrails
        """

        for step in range(10):  # safety limit
            print(f"\n🧠 Step {step + 1}")

            # -------------------------------
            # 🔥 STATE-BASED CONTROL (CRITICAL)
            # -------------------------------
            if not self.memory.get("data"):
                action = "fetch"

            elif not self.memory.get("filtered"):
                action = "filter"

            elif not self.memory.get("summaries"):
                action = "summarize"

            elif not self.memory.get("final"):
                action = "learn"

            else:
                action = "stop"

            # -------------------------------
            # 🧠 Planner (for reasoning/logging)
            # -------------------------------
            compact_state = {
                "has_data": bool(self.memory.get("data")),
                "has_filtered": bool(self.memory.get("filtered")),
                "has_summaries": bool(self.memory.get("summaries")),
                "has_final": bool(self.memory.get("final"))
        }

            plan = self.planner.plan(
                goal,
                compact_state,
                self.tools.list_tools()
            )

            print(f"   🤖 Planner suggests: {plan.get('action')}")
            print(f"   ⚙️ Executing: {action}")

            # -------------------------------
            # 🛑 Stop condition
            # -------------------------------
            if action == "stop":
                print("✅ Goal completed")
                break

            # -------------------------------
            # ⚡ Execute action
            # -------------------------------
            try:
                if action == "fetch":
                    result = self.executor.execute(action, goal)
                    self.memory.update("data", result)
                    print(f"   📥 Data fetched: {len(result)} items")

                elif action == "filter":
                    data = self.memory.get("data")
                    result = self.executor.execute(action, data)
                    self.memory.update("filtered", result)
                    print(f"   🔍 Filtered: {len(result)} items")

                elif action == "summarize":
                    data = self.memory.get("filtered")
                    result = self.executor.execute(action, data)
                    self.memory.update("summaries", result)
                    print(f"   🧠 Summarized: {len(result)} items")

                elif action == "learn":
                    data = self.memory.get("summaries")
                    result = self.executor.execute(action, data)
                    self.memory.update("final", result)
                    print(f"   📚 Learning added: {len(result)} items")

            except Exception as e:
                print(f"❌ Execution error at step {step + 1}: {e}")
                break

        # -------------------------------
        # 📤 Final Output
        # -------------------------------
        final_output = self.memory.get("final")

        if not final_output:
            print("⚠️ No final output generated")
            return []

        return final_output