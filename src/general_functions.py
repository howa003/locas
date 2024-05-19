import datetime
import eel

def get_timestamp() -> str:
    return '[' + str(datetime.datetime.now().strftime("%H:%M:%S")) + '] '


def double_print(message: str) -> None:
    print_message = get_timestamp() + message
    print(print_message)
    eel.print_status(print_message)()
