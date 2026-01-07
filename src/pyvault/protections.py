import time
import random
import string
import questionary
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
    def random_confirmation_challenge(length=5):
        """Generates a random alphanumeric challenge to prevent automated scripts."""
        # Genera una stringa casuale di lettere maiuscole e numeri
        challenge = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=length)
        )

        response = questionary.text(
            f"Security Check: Type '{challenge}' to confirm you are human:",
            instruction=" (Case sensitive)",
        ).ask()

        if response == challenge:
            return True
        else:
            console.print(
                "[bold red]Verification failed.[/bold red] Challenge string did not match."
            )
            return False
