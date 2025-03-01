import argparse
from modelscout.engine import load_models, scout_models, interactive_args


def main():
    parser = argparse.ArgumentParser(
        description="ModelScout: Find the best LLM for your needs."
    )
    parser.add_argument(
        "file",
        nargs="?",
        default=None,
        help="Path to the CSV file (default: ./models.csv)",
    )
    parser.add_argument(
        "--scout",
        action="store_true",
        help="Launch interactive mode for selecting filters (Recommended)",
    )
    parser.add_argument(
        "--top",
        default=5,
        type=int,
        help="Number of recommended models to display (5 by default)",
    )
    parser.add_argument(
        "--license",
        default=0,
        type=int,
        help="Ideal license (1 for open source, 0 for no preference)",
    )
    parser.add_argument(
        "--performance",
        default=None,
        type=float,
        help="Ideal performance rating (1.0-10.0)",
    )
    parser.add_argument(
        "--cost", default=None, type=float, help="Ideal cost per million tokens"
    )
    parser.add_argument(
        "--context_length", default=None, type=int, help="Ideal context length"
    )
    parser.add_argument(
        "--support",
        default=None,
        type=float,
        help="Ideal API/tools availability (1.0-10.0)",
    )

    args = parser.parse_args()
    df = load_models(args.file)

    if args.scout:
        print(scout_models(*interactive_args(df)))
    else:
        print("\nMatching Models:")
        print(
            scout_models(
                df,
                args.top,
                args.license,
                args.performance,
                args.cost,
                args.context_length,
                args.support,
            )
        )


if __name__ == "__main__":
    main()
