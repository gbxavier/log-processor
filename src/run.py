import sys

from src.analyzer import Analyzer

if __name__ == "__main__":
    try:
        with open(sys.argv[1]) as f:
            analyzer = Analyzer()
            for line in f:
                analyzer.ingest_line(line)
            print(analyzer.get_all_sessions_string(only_failed=True))
    except IndexError:
        print("ERROR: Filename expected")
        print(f"Usage:\n{sys.argv[0]} filename ")
