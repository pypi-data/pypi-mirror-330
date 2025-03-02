import typer
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown

app = typer.Typer(
    add_completion=True
)
console = Console()

@app.command()
def cat_readme(
        readme_file: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False, resolve_path=True, help="Path to the dependency file to export")
    ):
    with open(readme_file) as f:
        readme = f.read()
    console.print(Markdown(readme))

if __name__ == "__main__":
    app()