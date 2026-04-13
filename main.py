from agents.autonomous_orchestrator import AutonomousSystem

def main():
    system = AutonomousSystem()

    goal = "Generate an AI newsletter with insights and learning suggestions"

    results = system.run(goal)

    print("\n🧠 AUTONOMOUS OUTPUT:\n")

    for item in results:
        print(item["title"])
        print(item.get("summary"))
        print(item.get("learning"))
        print("-" * 50)


if __name__ == "__main__":
    main()