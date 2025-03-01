import aporia.parser.parser as parser
import aporia.interpreter as interpreter
import argparse
import sys
from pathlib import Path
from timeit import default_timer as timer

def cli():
    argparser = argparse.ArgumentParser(description="Run Aporia programs")
    argparser.add_argument('file', nargs='?', help="Source program which should be interpreted (has the .spp file extension)")
    argparser.add_argument('-a', '--ast', action='store_true', help="Prints the abstract syntax tree")
    argparser.add_argument('-t', '--time', action='store_true', help="Prints the elapsed time for parsing and interpreting")

    args = argparser.parse_args()

    if args.file:
        source_file = Path(args.file)
        if not source_file.exists():
            print(f"File was not found: {source_file}")
            exit(1)
        with open(source_file) as f:
            source_code = f.read()
    else:
        # Read from stdin if no file argument is given
        source_code = sys.stdin.read().strip()
        if not source_code:
            print("No source code provided.")
            exit(1)

    start_time = timer()
    ast = parser.parse(source_code)
    result = interpreter.InterpLcfi().interp(ast)
    end_time = timer()

    if args.ast:
        print(f"{"*" * 8} AST START {"*" * 8}")
        print(ast.pretty())
        print(f"{"*" * 8} AST END {"*" * 8}")

    if args.time:
        print(f"Elapsed time: {end_time-start_time}")

    print(result)

if __name__ == "__main__":
    cli()



if __name__ == "__main__":
    cli()

