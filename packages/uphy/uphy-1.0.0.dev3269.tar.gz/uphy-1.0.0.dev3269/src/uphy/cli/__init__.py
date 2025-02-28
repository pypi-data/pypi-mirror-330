import logging
from rich.logging import RichHandler
from typer import Option, Typer

LOG = logging.getLogger(__name__)

app = Typer(
    pretty_exceptions_enable=False,
    no_args_is_help=True,
    name="controller",
    help="Run a demo modbus controller based on a model",
)


def configure_logging(level, force=False):
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(markup=True)],
        force=force,
    )


def _verbose_callback(value: bool):
    if value:
        configure_logging(level=logging.DEBUG, force=True)


VERBOSE_OPTION = Option(callback=_verbose_callback, help="Enable verbose output.")
