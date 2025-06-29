import argparse
from crew import create_pm_assistant_crew

def main():
    #CLI Setup
    parser = argparse.ArgumentParser(
        description="🧠 PM Assistant Crew"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        required=True,
        help="Product Manager's main objective (e.g., 'Explore adding AI data viz features')."
    )
    parser.add_argument(
        "--feedback",
        type=str,
        help="Optional path to a user feedback text file (e.g., user_feedback.txt)."
    )

    parser.add_argument("--context",
                        type=str,
                        help="Path to product context file.")

    args = parser.parse_args()

    print("\n🚀 Launching PM Assistant Crew...")
    print(f"📝 PM goal: {args.prompt}")
    if args.feedback:
        print(f"📂 Using user feedback from: {args.feedback}")
    if args.context:
        print(f"📂 Using user feedback from: {args.context}")
    #Create and run the crew
    crew = create_pm_assistant_crew(args.prompt, args.feedback, args.context)
    result = crew.kickoff()

    #Print output
    print("\n✅ Final Consolidated Report:\n")
    print(result)

if __name__ == "__main__":
    main()

