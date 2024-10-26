import argparse
from pathlib import Path
from functools import wraps


def validate_path(func):
    @wraps(func)
    def wrapper(source: Path, output: Path):
        if not source.exists():
            raise FileNotFoundError(f"Error: dir {source} not found.")
        if not source.is_dir():
            raise NotADirectoryError(f"Error: {source} not is dir.")
        if output.exists() and not output.is_dir():
            raise NotADirectoryError(f"Error: {output} not is dir.")
        return func(source, output)
    return wrapper

@validate_path
def process_paths(source: Path, output: Path) -> tuple[Path, Path]:
    return source, output

def parse_args()->tuple[Path,Path]:
    parser = argparse.ArgumentParser(description="Sorting folder")
    parser.add_argument("--source", "-s", help="Source folder", required=True)
    parser.add_argument("--output", "-o", help="Output folder", default="dist")

    args = parser.parse_args()

    source = Path(args.source)
    output = Path(args.output)

    return process_paths(source, output)
