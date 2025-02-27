import typer
from rich.console import Console
from rich.panel import Panel
from services import login, billing, ec2, s3

app = typer.Typer()
console = Console()

# Add commands from each module as sub-commands
app.add_typer(login.app)
app.add_typer(billing.app, name="billing")
app.add_typer(ec2.app, name="ec2")
app.add_typer(s3.app, name="s3")

def print_banner():
    # ASCII art for "AWS CONNECT"
    banner = r"""
                                                               __   
_____ __  _  ________   ____  ____   ____   ____   ____  _____/  |_ 
\__  \\ \/ \/ /  ___/ _/ ___\/  _ \ /    \ /    \_/ __ \/ ___\   __\
 / __ \\     /\___ \  \  \__(  <_> )   |  \   |  \  ___|  \___|  |  
(____  /\/\_//____  >  \___  >____/|___|  /___|  /\___  >___  >__|  
     \/           \/       \/           \/     \/     \/    \/      
    """
    panel = Panel(banner, border_style="bright_blue")
    console.print(panel)

if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")

