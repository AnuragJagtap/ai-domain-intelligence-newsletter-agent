from pipelines.unified_pipeline import UnifiedPipeline
from config.settings import DEFAULT_DOMAIN


def main():
    pipeline = UnifiedPipeline()

    results = pipeline.run(DEFAULT_DOMAIN)

    print("\n🧠 FINAL NEWSLETTER CONTENT:\n")

    for i, item in enumerate(results, 1):
        print(f"{i}. [{item['type'].upper()}] {item['title']}")
        print(f"   📝 Summary: {item.get('summary')}")
        print(f"   💡 Insight: {item.get('insight')}")

        learning = item.get("learning", {})

        print("   📚 Learn:")
        print(f"      Concepts: {learning.get('concepts')}")
        print(f"      Resources: {learning.get('resources')}")
        print(f"      Next Steps: {learning.get('next_steps')}")
        
        print("-" * 60)


if __name__ == "__main__":
    main()