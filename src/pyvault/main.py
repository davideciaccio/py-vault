import os
import time
import secrets
import string
import questionary
import click
from rich.console import Console
from rich.panel import Panel

# Local imports
from pyvault.crypto import CryptoManager
from pyvault.storage import VaultStorage
from pyvault.protections import SecurityProtections

console = Console()


class OrderedUsageCommand(click.Command):
    def format_usage(self, ctx, formatter):
        # Collect default usage pieces (e.g., ['[OPTIONS]', 'SERVICE'])
        pieces = self.collect_usage_pieces(ctx)

        # If there are at least two pieces (options and arguments), swap them
        if len(pieces) >= 2:
            # Remove the last element (the SERVICE argument)
            arg = pieces.pop()
            # Insert it at the beginning of the list
            pieces.insert(0, arg)

        # Write the modified usage line to the help output
        formatter.write_usage(ctx.command_path, " ".join(pieces))


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
@click.version_option(version="0.1.0-alpha", prog_name="Py-Vault")
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
    crypto = CryptoManager()  # Inizializziamo il gestore crittografico

    # 1. Check if vault already exists
    if os.path.exists(db_path) and storage.get_master_salt():
        console.print("[bold red]Error:[/bold red] Vault already initialized.")
        return

    show_banner()
    console.print("[bold cyan]Starting Vault Initialization...[/bold cyan]\n")

    # 2. Master Password Input
    start_time = time.time()
    master_pwd = questionary.password(
        "Set your Master Password:", instruction=" (Choose a strong, unique password)"
    ).ask()

    if not master_pwd:
        console.print("[red]Password cannot be empty.[/red]")
        return

    # 3. Security Protections (Typing Speed & Challenge)
    if not SecurityProtections.check_input_speed(master_pwd, start_time):
        return
    if not SecurityProtections.random_confirmation_challenge():
        return

    # 4. Cryptographic Setup
    console.print(
        "\n[yellow]Generating unique security salt and initializing database...[/yellow]"
    )

    try:
        # A. Generiamo il Salt
        salt = os.urandom(16)

        # B. Deriviamo la Master Key dalla password (KDF Argon2id)
        # Questa chiave servirà per cifrare il verificatore
        key = crypto.derive_key(master_pwd, salt)

        # C. Creiamo il VERIFIER (Canary)
        # Cifriamo una stringa fissa: se in futuro riusciremo a decifrarla,
        # la Master Password inserita sarà corretta.
        verifier_blob = crypto.encrypt("PYVAULT_VERIFIER", key)

        # D. Salvataggio atomico nel nuovo database
        # Il nuovo storage.py gestisce la creazione tabelle nel suo __init__
        storage.store_master_data(salt, verifier_blob)

        console.print(
            "[bold green]Success![/bold green] Your vault has been initialized."
        )
        console.print(
            "[dim]A unique master salt and verifier have been stored in vault.db.[/dim]"
        )

    except Exception as e:
        console.print(f"[bold red]Critical Error during initialization:[/bold red] {e}")


@cli.command(
    cls=OrderedUsageCommand
)  # Apply the orderUsageCommand class to the command
@click.argument("service")
@click.option(
    "--username", prompt="Username for the service", help="The username to store."
)
@click.option("--gen", is_flag=True, help="Generate a secure random password.")
@click.option("--length", default=20, help="Length of the password to generate.")
def add(service, username, gen, length):
    """Add a new credential to the vault."""
    db_path = "vault.db"
    storage = VaultStorage(db_path)
    crypto = CryptoManager()

    if not os.path.exists(db_path):
        console.print(
            "[bold red]Error:[/bold red] Vault not initialized. Run 'pyvault init' first."
        )
        return

    # 1. Input Master Password con analisi della velocità (Anti-Ducky)
    start_time = time.time()
    master_pwd = questionary.password("Enter your Master Password:").ask()

    if not master_pwd or not SecurityProtections.check_input_speed(
        master_pwd, start_time
    ):
        return

    try:
        # 2. Derivazione della chiave sessione
        salt = storage.get_master_salt()
        verifier_blob = storage.get_verifier()
        key = crypto.derive_key(master_pwd, salt)
        crypto.decrypt(verifier_blob, key)

    except Exception:
        console.print("\n[bold red]ACCESS DENIED:[/bold red] Invalid Master Password.")
        return

    # 3. Gestione Password: Generazione o Input manuale
    if gen:
        alphabet = string.ascii_letters + string.digits + string.punctuation
        target_password = "".join(secrets.choice(alphabet) for _ in range(length))
        console.print(f"[bold green]Generated password:[/bold green] {target_password}")
    else:
        target_password = questionary.password(f"Enter password for {service}:").ask()
    # 4. Cifratura e Salvataggio
    if target_password:
        encrypted_blob = crypto.encrypt(target_password, key)
        storage.add_credential(service, username, encrypted_blob)
        console.print(
            f"\n[bold green]✔[/bold green] Credentials for [bold cyan]{service}[/bold cyan] saved successfully!"
        )


if __name__ == "__main__":
    cli()
