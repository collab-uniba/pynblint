from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax


def main():

    python_code = """
    import prova

    {...}

    print("prova")
    """

    console = Console()
    group = Columns(
        [
            "\nIn [1]:",
            Panel(Syntax(python_code, "python"), width=int(console.size[0] * 0.90)),
        ]
    )

    console.print(group)


if __name__ == "__main__":
    main()
