import datetime


def get_timestamp() -> str:
    return '[' + str(datetime.datetime.now().strftime("%H:%M:%S")) + '] '


