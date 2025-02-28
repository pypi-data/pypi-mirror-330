from os import getenv


__OBSTOOL_DEBUG = int(getenv("OBSTOOL_DEBUG", 0))


def debug_log(message: str, object: any = None, exception: Exception = None):

    if __OBSTOOL_DEBUG >= 2:
        error_log(message, object, exception, level="D")


def info_log(message: str, object: any = None, exception: Exception = None):

    if __OBSTOOL_DEBUG >= 1:
        error_log(message, object, exception, level="I")


def error_log(message: str, object: any = None, exception: Exception = None, level: str = "E"):

    from datetime import datetime
    from os import getpid
    from traceback import format_exception

    log_header = f"{datetime.now().isoformat(timespec="seconds")} {level[0]} {getpid():07d}"

    print(f"{log_header} {message}")
    if object is not None:
        print(f"{log_header} ", object, sep="| ")
    if exception is not None:
        if __OBSTOOL_DEBUG >= 2:
            print(f"{log_header} ", "".join(format_exception(exception, limit=None, chain=True)), sep="| ")
        else:
            print(f"{log_header} ", repr(exception), sep="| ")
    print()
