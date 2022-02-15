from rich.console import Console, ConsoleOptions, RenderResult
from rich.markdown import Heading, Markdown


class NotebookHeading(Heading):
    "A Markdown heading inside a notebook Markdown cell."

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        text = self.text
        if self.level == 1:
            # Double underline for h1s
            yield text
            yield "=" * len(text)
        # elif self.level == 2:
        #     # Single underline for h2s
        #     yield text
        #     yield "-" * len(text)
        else:
            # No underline for h3s and beyond
            yield text


class NotebookMarkdown(Markdown):
    "A renderable for Markdown text in Markdown cells."

    elements = Markdown.elements
    elements["heading"] = NotebookHeading
