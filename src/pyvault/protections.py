import time
import random
import string
from rich.console import Console

console = Console()


class SecurityProtections:
    """
    Implements active defenses against automated hardware attacks (for example Rubber Ducky)
    and pre-programmed scripts.
    """

    @staticmethod
    def check_input_speed(input_text: str, start_time: float, threshold: float = 0.05):
        """
        Analyzes the typing speed. If a long password is entered too quickly,
        it triggers a security alert.
        """
        end_time = time.time()
        duration = end_time - start_time

        # If more than 5 chars are typed in less than 'threshold' seconds
        if len(input_text) > 5 and duration < threshold:
            console.print(
                "[bold red]SECURITY ALERT: Automated input detected (Rubber Ducky).[/bold red]"
            )
            console.print("[red]Access denied for security reasons.[/red]")
            return False
        return True

    @staticmethod
    def random_confirmation_challenge() -> bool:
        """
        Forces the user to solve a simple random challenge.
        """
        char = random.choice(string.ascii_uppercase)
        console.print(
            f"\n[bold yellow]SECURITY CHECK:[/bold yellow] Type the letter [bold cyan]{char}[/bold cyan] to confirm: ",
            end="",
        )

        user_input = input().strip().upper()

        if user_input != char:
            console.print("[bold red]Verification failed. Action aborted.[/bold red]")
            return False
        return True
