import os
import time
import secrets
import string
import questionary
import click
import pyperclip
import threading
from rich.table import Table
from rich.console import Console
from rich.panel import Panel

# Local imports
from pyvault.crypto import CryptoManager
from pyvault.storage import VaultStorage
from pyvault.protections import SecurityProtections

console = Console()

# --- UI UTILITIES ---


def print_security_error(message="Invalid Master Password. Authorization failed."):
    """Standardized security error message for failed authentication."""
    console.print("\n")
    console.print(
        Panel(
            f"[bold red]ACCESS DENIED[/bold red]\n{message}",
            border_style="red",
            expand=False,
            title="[bold red]Security Notification",
            padding=(1, 2),
        )
    )


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


# --- CLICK CUSTOMIZATIONS ---


class OrderedUsageGroup(click.Group):
    def format_usage(self, ctx, formatter):
        pieces = self.collect_usage_pieces(ctx)
        pieces = [p.replace(" [ARGS]...", "") for p in pieces]
        if len(pieces) >= 2:
            opts = pieces.pop(0)
            pieces.insert(1, opts)
        formatter.write_usage(ctx.command_path, " ".join(pieces))


class OrderedUsageCommand(click.Command):
    def format_usage(self, ctx, formatter):
        pieces = self.collect_usage_pieces(ctx)
        if len(pieces) >= 2:
            arg = pieces.pop()
            pieces.insert(0, arg)
        formatter.write_usage(ctx.command_path, " ".join(pieces))


# --- CLI CORE ---


@click.group(cls=OrderedUsageGroup, invoke_without_command=True)
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
    crypto = CryptoManager()

    if os.path.exists(db_path) and storage.get_master_salt():
        console.print(
            Panel(
                "[bold red]Error:[/bold red] Vault already initialized.",
                border_style="red",
                expand=False,
            )
        )
        return

    show_banner()
    console.print("[bold cyan]Starting Vault Initialization...[/bold cyan]\n")

    # 1. Primo inserimento (Nascosto)
    start_time = time.time()
    master_pwd_first = questionary.password(
        "Set your Master Password:", instruction=" (Choose a strong, unique password)"
    ).ask()

    if not master_pwd_first:
        console.print("[red]Password cannot be empty.[/red]")
        return

    # 2. Conferma (Nascosto)
    master_pwd_confirm = questionary.password(
        "Confirm your Master Password:", instruction=" (Must match exactly)"
    ).ask()

    if master_pwd_first != master_pwd_confirm:
        console.print(
            Panel(
                "[bold red]Error:[/bold red] Passwords do not match. Initialization aborted.",
                border_style="red",
                expand=False,
            )
        )
        # Rimuoviamo il file database se è stato creato per errore
        if os.path.exists(db_path):
            os.remove(db_path)
        return

    master_pwd = master_pwd_first

    # 3. Security Protections (Velocità e Sfida Casuale)
    if not SecurityProtections.check_input_speed(master_pwd, start_time):
        if os.path.exists(db_path):
            os.remove(db_path)
        return
    if not SecurityProtections.random_confirmation_challenge():
        if os.path.exists(db_path):
            os.remove(db_path)
        return

    # 4. Cryptographic Setup
    console.print(
        "\n[yellow]Generating unique security salt and initializing database...[/yellow]"
    )

    try:
        salt = os.urandom(16)
        key = crypto.derive_key(master_pwd, salt)
        verifier_blob = crypto.encrypt("PYVAULT_VERIFIER", key)
        storage.store_master_data(salt, verifier_blob)

        console.print(
            Panel(
                "[bold green]Success![/bold green] Your vault has been initialized.",
                border_style="green",
                expand=False,
            )
        )
    except Exception as e:
        console.print(f"[bold red]Critical Error during initialization:[/bold red] {e}")
        if os.path.exists(db_path):
            os.remove(db_path)


@cli.command(cls=OrderedUsageCommand)
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
            Panel(
                "[bold red]Error:[/bold red] Vault not initialized. Run 'pyvault init' first.",
                border_style="red",
                expand=False,
            )
        )
        return

    start_time = time.time()
    master_pwd = questionary.password("Enter your Master Password:").ask()

    if not master_pwd or not SecurityProtections.check_input_speed(
        master_pwd, start_time
    ):
        return

    try:
        salt = storage.get_master_salt()
        verifier_blob = storage.get_verifier()
        key = crypto.derive_key(master_pwd, salt)
        crypto.decrypt(verifier_blob, key)
    except Exception:
        print_security_error()
        return

    if gen:
        alphabet = string.ascii_letters + string.digits + string.punctuation
        target_password = "".join(secrets.choice(alphabet) for _ in range(length))
        console.print(f"[bold green]Generated password:[/bold green] {target_password}")
    else:
        target_password = questionary.password(f"Enter password for {service}:").ask()

    if target_password:
        encrypted_blob = crypto.encrypt(target_password, key)
        storage.add_credential(service, username, encrypted_blob)
        console.print(
            f"\n[bold green]✔[/bold green] Credentials for [bold cyan]{service}[/bold cyan] saved successfully!"
        )


def delayed_clipboard_clear(delay):
    """Wait for 'delay' seconds and then clear the clipboard content."""
    time.sleep(delay)
    pyperclip.copy("")


@cli.command(cls=OrderedUsageCommand)
@click.argument("service")
@click.option("--copy", is_flag=True, help="Copy the password to the clipboard.")
def get(service, copy):
    """Retrieve and decrypt credentials for a specific service."""
    db_path = "vault.db"
    storage = VaultStorage(db_path)
    crypto = CryptoManager()

    if not os.path.exists(db_path):
        console.print(
            Panel(
                "[bold red]Error:[/bold red] Vault not initialized.",
                border_style="red",
                expand=False,
            )
        )
        return

    start_time = time.time()
    master_pwd = questionary.password("Enter your Master Password:").ask()

    if not master_pwd or not SecurityProtections.check_input_speed(
        master_pwd, start_time
    ):
        return

    try:
        salt = storage.get_master_salt()
        verifier_blob = storage.get_verifier()
        key = crypto.derive_key(master_pwd, salt)
        crypto.decrypt(verifier_blob, key)
    except Exception:
        print_security_error()
        return

    credential = storage.get_credential(service)
    if not credential:
        console.print(
            f"\n[bold yellow]No credentials found for service:[/bold yellow] {service}"
        )
        return

    try:
        username = credential[0]
        password_blob = credential[1]
        decrypted_password = crypto.decrypt(password_blob, key)

        if copy:
            pyperclip.copy(decrypted_password)
            console.print(
                f"\n[bold green]✔[/bold green] Password for [bold cyan]{service}[/bold cyan] copied to clipboard for 30s!"
            )
            threading.Thread(
                target=delayed_clipboard_clear, args=(30,), daemon=True
            ).start()
        else:
            console.print(f"\n[bold green]Credentials for {service}:[/bold green]")
            console.print(f"Username: [bold cyan]{username}[/bold cyan]")
            console.print(f"Password: [bold red]{decrypted_password}[/bold red]")
    except Exception as e:
        console.print(
            f"\n[bold red]Error:[/bold red] Could not decrypt the credential. Details: {e}"
        )


@cli.command(cls=OrderedUsageCommand)
def list():
    """List all stored services in the vault."""
    db_path = "vault.db"
    storage = VaultStorage(db_path)
    crypto = CryptoManager()

    if not os.path.exists(db_path):
        console.print(
            Panel(
                "[bold red]Error:[/bold red] Vault not initialized.",
                border_style="red",
                expand=False,
            )
        )
        return

    start_time = time.time()
    master_pwd = questionary.password("Enter your Master Password:").ask()

    if not master_pwd or not SecurityProtections.check_input_speed(
        master_pwd, start_time
    ):
        return

    try:
        salt = storage.get_master_salt()
        verifier_blob = storage.get_verifier()
        key = crypto.derive_key(master_pwd, salt)
        crypto.decrypt(verifier_blob, key)
    except Exception:
        print_security_error()
        return

    try:
        credentials = storage.get_all_credentials()
        if not credentials:
            console.print(
                Panel(
                    "[yellow]The vault is currently empty.[/yellow]",
                    title="Info",
                    expand=False,
                )
            )
            return

        table = Table(
            title="Stored Credentials", border_style="blue", header_style="bold magenta"
        )
        table.add_column("Service", style="cyan", no_wrap=True)
        table.add_column("Username", style="green")

        for cred in credentials:
            table.add_row(str(cred[0]), str(cred[1]))

        console.print("\n")
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Developer Error:[/bold red] {e}")


@cli.command(cls=OrderedUsageCommand)
@click.argument("service")
def rm(service):
    """Delete a stored service from the vault."""
    db_path = "vault.db"
    storage = VaultStorage(db_path)
    crypto = CryptoManager()

    if not os.path.exists(db_path):
        console.print(
            Panel(
                "[bold red]Error:[/bold red] Vault not initialized.",
                border_style="red",
                expand=False,
            )
        )
        return

    start_time = time.time()
    master_pwd = questionary.password("Enter your Master Password:").ask()

    if not master_pwd or not SecurityProtections.check_input_speed(
        master_pwd, start_time
    ):
        return

    try:
        salt = storage.get_master_salt()
        verifier_blob = storage.get_verifier()
        key = crypto.derive_key(master_pwd, salt)
        crypto.decrypt(verifier_blob, key)
    except Exception:
        print_security_error()
        return

    credential = storage.get_credential(service)
    if not credential:
        console.print(f"\n[bold yellow]Service '{service}' not found.[/bold yellow]")
        return

    if questionary.confirm(
        f"Are you sure you want to PERMANENTLY delete '{service}'?"
    ).ask():
        try:
            storage.delete_credential(service)
            console.print(
                Panel(
                    f"[bold green]✔ Success:[/bold green] '{service}' has been removed.",
                    border_style="green",
                    expand=False,
                )
            )
        except Exception as e:
            console.print(f"[bold red]Error during deletion:[/bold red] {e}")


@cli.command(cls=OrderedUsageCommand)
def audit():
    """Scan the vault for weak or reused passwords."""
    db_path = "vault.db"
    storage = VaultStorage(db_path)
    crypto = CryptoManager()

    if not os.path.exists(db_path):
        console.print(
            Panel(
                "[bold red]Error:[/bold red] Vault not initialized.",
                border_style="red",
                expand=False,
            )
        )
        return

    start_time = time.time()
    master_pwd = questionary.password("Enter Master Password:").ask()

    if not master_pwd or not SecurityProtections.check_input_speed(
        master_pwd, start_time
    ):
        return

    try:
        salt = storage.get_master_salt()
        verifier_blob = storage.get_verifier()
        key = crypto.derive_key(master_pwd, salt)
        crypto.decrypt(verifier_blob, key)
    except Exception:
        print_security_error()
        return

    try:
        items = storage.get_full_inventory()
        if not items:
            console.print("[yellow]Vault is empty. Nothing to audit.[/yellow]")
            return

        total_count = len(items)
        weak_passwords = []
        passwords_map = {}

        with console.status("[bold green]Analyzing credentials..."):
            for service, username, blob in items:
                raw_pwd = crypto.decrypt(blob, key)
                if len(raw_pwd) < 12:
                    weak_passwords.append(service)
                if raw_pwd not in passwords_map:
                    passwords_map[raw_pwd] = []
                passwords_map[raw_pwd].append(service)

        reused_groups = {
            pwd: svcs for pwd, svcs in passwords_map.items() if len(svcs) > 1
        }

        console.print(
            Panel(
                f"[bold]Security Audit Report[/bold]\nTotal Credentials Scanned: {total_count}",
                expand=False,
            )
        )

        if weak_passwords:
            weak_table = Table(title="Weak Passwords (Length < 12)", border_style="red")
            weak_table.add_column("Service", style="bold red")
            for s in weak_passwords:
                weak_table.add_row(s)
            console.print(weak_table)
        else:
            console.print("[bold green]✔ No weak passwords found.[/bold green]")

        if reused_groups:
            reuse_table = Table(title="Password Reuse Detected", border_style="yellow")
            reuse_table.add_column("Reused Services", style="bold yellow")
            for svcs in reused_groups.values():
                reuse_table.add_row(", ".join(svcs))
            console.print(reuse_table)
        else:
            console.print("[bold green]✔ No password reuse detected.[/bold green]")

    except Exception as e:
        console.print(f"[bold red]Audit Error:[/bold red] {e}")


if __name__ == "__main__":
    cli()
