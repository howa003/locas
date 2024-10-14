import datetime
import eel

def get_timestamp() -> str:
    return '[' + str(datetime.datetime.now().strftime("%H:%M:%S")) + '] '


def double_print(message: str) -> None:
    print_message = get_timestamp() + message
    print(print_message)
    eel.print_status(print_message)()


def num_to_str_1_dec(number: float) -> str:
    return str(round(number, 1))


def num_to_str_4_dec(number: float) -> str:
    return str(round(number, 4))
