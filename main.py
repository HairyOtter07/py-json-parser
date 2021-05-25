from parse import Lexer, Parser
from sys import argv

def main():
    args = argv[1:]
    if len(args) < 1:
        args.append("--help")

    if args[0] == "--help":
        print("usage: python main.py <filename> | -c <json>")

    elif args[0] == "-c":
        json = args[1]
        print(parse(json))

    else:
        file = open(args[0], "r")
        i = file.read()
        json = parse(i)
        file.read()
        print(json)

def parse(text):
    lexer = Lexer(text)
    parser = Parser(lexer)
    return parser.parse()

if __name__ == "__main__":
    main()
