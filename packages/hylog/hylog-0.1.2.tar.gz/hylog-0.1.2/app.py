import time

from pathlib import Path

from hylog import get_app_logger


log = get_app_logger("app", Path(__file__).parent / "logs", stdout_level="DEBUG")

@log.func()
def test_func_decorator(arg1: str, *, kwarg1: int) -> str:
    return f"arg1: {arg1}, kwarg1: {kwarg1}"

@log.perf()
def test_perf_decorator() -> None:
    time.sleep(1)

def test_logger() -> None:
    log.debug("DEBUG message")
    log.debug("DEBUG message with extra", extra={"extra_key": "extra_value"})
    log.info("INFO message")
    log.warning("WARNING message")
    log.error("ERROR message")
    log.critical("CRITICAL message")

    log.info(Path().cwd())
    log.info(Path().home())

    try:
        1 / 0

    except ZeroDivisionError as e:
        log.exception("Exception occurred", exc_info=e)



if __name__ == "__main__":
    test_logger()
    test_func_decorator("test", kwarg1=42)
    test_perf_decorator()
