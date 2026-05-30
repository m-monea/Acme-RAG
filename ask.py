import sys
from src.rag import answer_question


def main():
    if len(sys.argv) < 2:
        print('Usage: python ask.py "Your question here"')
        return

    question = " ".join(sys.argv[1:])
    result = answer_question(question)

    print("\nAnswer:\n")
    print(result["answer"])

    print("\nSources:")
    for source in result["sources"]:
        print(f"- {source}")


if __name__ == "__main__":
    main()
