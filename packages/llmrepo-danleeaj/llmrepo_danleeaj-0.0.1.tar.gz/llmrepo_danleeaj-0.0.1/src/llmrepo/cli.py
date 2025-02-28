from utils.parse_directory import parse_directory

import typer

app = typer.Typer()

@app.command()
def main(dir: str, tree_only: bool=False):
    parse_directory(dir, tree_only)

# def main():
#     parser = argparse.ArgumentParser(description='A command-line tool that parses directories in an LLM-friendly format')
#     parser.add_argument('directory', type=str, nargs=1, help='The directory to parse')
#     parser.add_argument('--tree-only', '-t', action='store_true', help='Only output the directory structure, not file contents')
#
#     args = parser.parse_args()
#
#     parse_directory(args.directory[0], tree_only=args.tree_only)

if __name__ == "__main__":
    app()
