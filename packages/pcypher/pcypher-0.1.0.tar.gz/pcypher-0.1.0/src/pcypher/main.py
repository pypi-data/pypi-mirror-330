from pcypher import CypherParser, CypherLexer
import argparse


def main():
    args = argparse.ArgumentParser()
    args.add_argument("query", help="Query to parse")
    args = args.parse_args()

    parser = CypherParser()
    result = parser.parse(args.query)
    print(f"{str(result)}")


if __name__ == "__main__":
    main()
