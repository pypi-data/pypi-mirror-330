import typer
from rich.console import Console
from rich.table import Table
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

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Welcome to aws-connect CLI App.
    """
    if ctx.invoked_subcommand is None:
        # Display the banner
        print_banner()
        console.print("\n[bold cyan]Welcome to AWS CONNECT CLI App[/bold cyan]\n")
        
        # Dynamically generate command table
        table = Table(title="Available Commands", header_style="bold magenta")
        table.add_column("Command", style="green")
        table.add_column("Description", style="cyan")
        
        commands = [
            {"name": "login", "desc": "Choose an existing AWS profile or add a new account"},
            {"name": "billing", "desc": "View AWS billing & cost management info"},
            {"name": "ec2", "desc": "Manage EC2 instances"},
            {"name": "s3", "desc": "Manage S3 operations"},
        ]
        
        for command in commands:
            table.add_row(command["name"], command["desc"])
        
        console.print(table)
        raise typer.Exit()

if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")

