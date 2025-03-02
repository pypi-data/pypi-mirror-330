from os import system
from os import name
import time
import sys


def clear_screen() -> None:
    """
    Clear the screen.

    This function will clear the screen of the terminal or command prompt. It will use the 'cls' command on Windows and
    the 'clear' command on Unix-based systems.

    Returns:
         None
    """
    if name == 'nt':
        system('cls')
    else:
        system('clear')

    return


# Create a function that can print 'Exiting...' to the screen where the ellipsis is animated.
def print_exit_message(
        max_dots: int   = 3,
        interval: float = 0.5,
        run_time: float = 5.0,
) -> None:
    """
    Print an animated 'Exiting...' message to the screen.

    This function will print the message 'Exiting...' to the screen with an animated ellipsis. The ellipsis will
    animate by adding a period to the end of the message every 0.5 seconds. The message will be printed to the screen
    until the function is interrupted by the user.

    Parameters:
        max_dots:
            The maximum number of dots to display in the animated ellipsis. Defaults to 3.

        interval:
            The interval between each dot addition in seconds. Defaults to 0.5.

        run_time:
            The maximum amount of time to run the function in seconds. Defaults to 5.0.

    Returns:
        None
    """
    start_time = time.time()
    dots = 0
    while time.time() - start_time < run_time:
        # Cycle through 1 to max_dots dots.
        dots = (dots % max_dots) + 1
        # Build the display string with padding to avoid leftover characters.
        display_str = f'\rExiting{"." * dots}{" " * (max_dots - dots)}'
        sys.stdout.write(display_str)
        sys.stdout.flush()
        time.sleep(interval)
    # Final display to ensure the full ellipsis is visible.
    sys.stdout.write(f'\rExiting{"." * max_dots}\n')
    sys.stdout.flush()

    return


def simple_example_handler() -> None:
    print_exit_message()

    return
