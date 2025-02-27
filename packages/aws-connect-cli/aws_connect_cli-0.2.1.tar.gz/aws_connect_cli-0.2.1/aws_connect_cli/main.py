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
        table = Table(title="Available Commands", header_style="bold magenta")
        table.add_column("Command", style="green")
        table.add_column("Description", style="cyan")
        table.add_row("login", "Choose an existing AWS profile or add a new account")
        table.add_row("billing", "View AWS billing & cost management info")
        table.add_row("ec2", "Manage EC2 instances")
        table.add_row("s3", "Manage S3 operations")
        console.print(table)
        raise typer.Exit()

if __name__ == "__main__":
    app()
