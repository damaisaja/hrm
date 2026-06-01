import typer
from rich.console import Console

app = typer.Typer(name="haulling", help="Mine Road Intelligence Platform")
console = Console()


@app.command()
def process(
    las: str = typer.Option(..., "--las", help="Path to LAS/LAZ point cloud file"),
    dtm: str = typer.Option(None, "--dtm", help="Path to DTM raster file"),
    road: str = typer.Option(None, "--road", help="Path to haul road DXF file"),
    fleet: str = typer.Option(None, "--fleet", help="Path to fleet data CSV file"),
):
    console.print("[bold green]Haulling - Road Intelligence Engine[/bold green]")
    console.print(f"  LAS: {las}")
    console.print(f"  DTM: {dtm or '(auto from LAS)'}")
    console.print(f"  Road: {road or '(not specified)'}")
    console.print(f"  Fleet: {fleet or '(not specified)'}")


@app.command()
def dashboard():
    """Launch the Streamlit dashboard."""
    import subprocess, sys
    subprocess.run([sys.executable, "-m", "streamlit", "run",
                    "src/dashboard/app.py"])


@app.command()
def version():
    """Show version info."""
    console.print("Haulling v0.1.0 - Mine Road Intelligence Platform")


if __name__ == "__main__":
    app()
