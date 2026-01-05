import os
import time
import click
import questionary
from rich.console import Console
from rich.panel import Panel

# Local imports
from pyvault.storage import VaultStorage
from pyvault.protections import SecurityProtections

console = Console()


def show_banner():
    """Displays a professional ASCII banner."""
    banner = """
    ██████╗ ██╗   ██╗      ██╗   ██╗ █████╗ ██╗   ██╗██╗     ████████╗
    ██╔══██╗╚██╗ ██╔╝      ██║   ██║██╔══██╗██║   ██║██║     ╚══██╔══╝
    ██████╔╝ ╚████╔╝ █████╗██║   ██║███████║██║   ██║██║        ██║
    ██╔═══╝   ╚██╔╝  ╚════╝╚██╗ ██╔╝██╔══██║██║   ██║██║        ██║
    ██║        ██║          ╚████╔╝ ██║  ██║╚██████╔╝███████╗   ██║
    ╚═╝        ╚═╝           ╚═══╝  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝
    """
    console.print(
        Panel(banner, subtitle="Secure CLI Password Manager", style="bold blue")
    )


@click.group(invoke_without_command=True)
@click.version_option(version="0.1.0", prog_name="Py-Vault")
@click.pass_context
def cli(ctx):
    """Py-Vault: A zero-knowledge, cross-platform password manager."""
    if ctx.invoked_subcommand is None:
        show_banner()
        click.echo(ctx.get_help())


@cli.command()
def init():
    """Initialize the secure vault and set the Master Password."""
    db_path = "vault.db"
    storage = VaultStorage(db_path)

    # 1. Check if vault already exists
    if os.path.exists(db_path) and storage.get_master_salt():
        console.print(
            "[bold red]Error:[/bold red] Vault already initialized. Use 'pyvault config' to change settings."
        )
        return

    show_banner()
    console.print("[bold cyan]Starting Vault Initialization...[/bold cyan]\n")

    # 2. Master Password Input with Timing Check
    start_time = time.time()
    master_pwd = questionary.password(
        "Set your Master Password:", instruction=" (Choose a strong, unique password)"
    ).ask()

    if not master_pwd:
        console.print("[red]Password cannot be empty.[/red]")
        return

    # 3. Security Protection: Typing Speed (Anti-Rubber Ducky)
    if not SecurityProtections.check_input_speed(master_pwd, start_time):
        return

    # 4. Security Protection: Random Challenge (Anti-Automation)
    if not SecurityProtections.random_confirmation_challenge():
        return

    # 5. Cryptographic Setup
    console.print(
        "\n[yellow]Generating unique security salt and initializing database...[/yellow]"
    )

    try:
        # Generate a unique salt for this installation
        salt = os.urandom(16)

        # Initialize DB and save salt
        storage.initialize_db()
        storage.save_master_salt(salt)

        console.print(
            "[bold green]Success![/bold green] Your vault has been initialized."
        )
        console.print(
            "[dim]A unique master salt has been generated and stored securely in vault.db.[/dim]"
        )
    except Exception as e:
        console.print(f"[bold red]Critical Error during initialization:[/bold red] {e}")


if __name__ == "__main__":
    cli()
