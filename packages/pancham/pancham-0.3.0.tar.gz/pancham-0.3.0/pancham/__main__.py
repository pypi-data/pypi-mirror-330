from typing import Annotated, Optional

import typer
import asyncio

from .reporter_lib.halo_reporter import HaloReporter
from .reporter import get_reporter
from .runner import PanchamRunner
from .pancham_configuration import OrderedPanchamConfiguration

app = typer.Typer()

@app.command()
def run(
        configuration: Annotated[str, typer.Argument(help = "Path to the Pancham configuration file")],
        data_configuration: Annotated[Optional[str], typer.Argument(help = "Path to the data mapping if individual files are being used")] = None
):
    pancham_configuration = OrderedPanchamConfiguration(configuration)

    if pancham_configuration.reporter_name == 'spinner':
        reporter = get_reporter(pancham_configuration.debug_status, HaloReporter())
    else:
        reporter = get_reporter(pancham_configuration.debug_status)

    runner = PanchamRunner(pancham_configuration, reporter = reporter)

    if len(pancham_configuration.mapping_files) == 0:
        asyncio.run(runner.load_and_run(data_configuration))
    else:
        asyncio.run(runner.run_all())
