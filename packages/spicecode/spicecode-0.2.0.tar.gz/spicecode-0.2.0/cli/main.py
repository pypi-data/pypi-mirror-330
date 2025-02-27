import typer
from rich import print
from spice.analyze import analyze_file

app = typer.Typer()

@app.command()
def analyze(file: str):
    """
    Analyze the given file.
    """
    try:
        analyze_file(file)
    except Exception as e:
        print(f"[red]Error:[/] {e}")

@app.command()
def hello():
    """
    Welcome message.
    """
    print("🌶️   Welcome to [bold red]SpiceCode[/]! 🌶️")
    print("🔥 The [yellow]CLI tool[/] that makes your code [yellow]spicier[/] 🥵")

def main():
    app()  # This will run your Typer app

if __name__ == "__main__":
    main()
