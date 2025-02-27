from typing import Annotated

import typer

from .rephraser import RephraseError, rephrase_text

app = typer.Typer(rich_markup_mode="rich")


@app.command()
def rephrase(
    text: Annotated[str, typer.Argument(help="Text to rephrase")],
    style: Annotated[
        str,
        typer.Option(
            "--style",
            "-s",
            help="Style: normal, casual, formal, academic, filipino",
        ),
    ] = "normal",
) -> None:
    """
    Rephrase text in a specified style using OpenAI's API.

    [bold green]Examples:[/bold green]

    [yellow]$ rephrase "I'm tired after work."[/yellow]
    $ I'm exhausted after work.

    [yellow]$ rephrase "I'm tired after work." --style casual[/yellow]
    $ I'm wiped out after work, dude.

    [yellow]$ rephrase "I'm tired after work." --style formal[/yellow]
    $ I find myself fatigued following work.

    [yellow]$ rephrase "I'm tired after work." -s academic[/yellow]
    $ I experience fatigue subsequent to my workday.

    [yellow]$ rephrase "I'm tired after work." -s filipino[/yellow]
    $ Napagod ako after work."
    """
    try:
        result = rephrase_text(text, style)
        typer.echo(result)
    except RephraseError as e:
        typer.echo(f"{e}", err=True)
        raise typer.Exit(code=1) from e


if __name__ == "__main__":
    app()
