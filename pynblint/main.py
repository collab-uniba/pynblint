""" Entry point of pynblint. Used when running pynblint from the command line. """

from pathlib import Path

import typer
from rich import print

from .notebook import Notebook

app = typer.Typer()


@app.command()
def main(path: Path = typer.Argument(..., exists=True)):
    with open(path) as notebook_file:
        nb = Notebook(Path(notebook_file.name), notebook_name=path.name)
        print(nb.get_pynblint_results())


if __name__ == "__main__":
    app()
