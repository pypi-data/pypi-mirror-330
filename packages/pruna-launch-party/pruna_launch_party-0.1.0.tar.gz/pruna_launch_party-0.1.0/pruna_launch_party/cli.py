import random
import sys
import time

import colorama
from colorama import Fore, Style
from tqdm import tqdm

# Initialize colorama
colorama.init()

AI_JOKES = [
    "Why did the neural network break up? Too many local minima!",
    "What's an AI's favorite drink? Deep learning juice!",
    "Why don't neural networks tell dad jokes? Overfitting!",
    "What do you call a pruned model that won't shut up? Small talk!",
]

PARTY_MESSAGES = [
    "Initializing party protocols...",
    "Loading celebration modules...",
    "Quantizing the fun...",
    "Pruning boring moments...",
    "Optimizing party parameters...",
    "Calibrating dance moves...",
]

def print_with_effect(text: str, color: str = Fore.GREEN, delay: float = 0.03) -> None:
    """Print text with a typewriter effect."""
    for char in text:
        sys.stdout.write(f"{color}{char}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def show_progress(message: str, duration: float = 1.0) -> None:
    """Show a progress bar with a message."""
    fmt = '{l_bar}{bar}| {n_fmt}/{total_fmt}'
    with tqdm(total=100, desc=message, bar_format=fmt) as pbar:
        for _ in range(100):
            time.sleep(duration / 100)
            pbar.update(1)

def print_banner() -> None:
    """Print the Pruna party banner."""
    banner = """
    🎉 PRUNA LAUNCH PARTY 🎉
    ========================
    Open Source & Open Bar!
    ========================
    """
    print_with_effect(banner, Fore.CYAN, 0.01)

def print_compressed_joke() -> None:
    """Print a compressed AI joke."""
    joke = random.choice(AI_JOKES)
    print_with_effect(
        "[DEBUG] Compressing AI jokes... ERROR: Jokes already too lossy.",
        Fore.YELLOW
    )
    print_with_effect(f"Here's one anyway: {joke}", Fore.MAGENTA)

def main() -> None:
    """Main party function."""
    print_banner()
    
    # Show initialization progress
    for message in PARTY_MESSAGES:
        show_progress(message)
    
    # Launch confirmation
    print_with_effect(
        "[INFO] Pruna's Open-Source Repo successfully launched! 🚀",
        Fore.GREEN
    )
    
    # Compressed joke
    print_compressed_joke()
    
    # High energy vibes
    msg = "[LOG] Unzipping high-energy vibes... DONE ✅"
    print_with_effect(msg, Fore.BLUE)
    
    # Final message
    print_with_effect("\nTime to celebrate! 🎉 The party is ON! 🎊", Fore.MAGENTA)
    msg = "Remember: This is technically an activation function. 🤓"
    print_with_effect(msg, Fore.CYAN)

if __name__ == "__main__":
    main() 