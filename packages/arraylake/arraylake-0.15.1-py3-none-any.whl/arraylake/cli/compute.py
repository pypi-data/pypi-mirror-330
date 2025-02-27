from enum import Enum

import typer
from rich import print_json
from rich.table import Table

from arraylake import Client
from arraylake.cli.utils import rich_console, simple_progress
from arraylake.log_util import get_logger

app = typer.Typer(help="Manage Arraylake compute services", no_args_is_help=True)
logger = get_logger(__name__)


class ListOutputType(str, Enum):
    rich = "rich"
    json = "json"


def _services_table(services, org):
    table = Table(title=f"Arraylake compute services for [bold]{org}[/bold]", min_width=80)
    table.add_column("Name", justify="left", style="cyan", no_wrap=True, min_width=10)
    table.add_column("Service Type", justify="right", style="green", min_width=10)
    table.add_column("Org", justify="right", style="green", min_width=10)
    table.add_column("Public", justify="right", style="green", min_width=10)
    table.add_column("URL", justify="right", style="green", min_width=10)
    table.add_column("Status", justify="right", style="green", min_width=10)

    status_colors = {"available": "green", "progressing": "yellow", "error": "red", "unknown": "grey"}

    for service in services:
        table.add_row(
            service.name,
            service.config.service_type,
            service.config.org,
            str(service.config.is_public),
            service.url,
            service.status,
            style=status_colors[service.status],
        )

    return table


@app.command(name="enable")
def enable_service(
    org: str = typer.Argument(..., help="The organization to enable the service for"),
    protocol: str = typer.Argument(..., help="The protocol to enable. Must be one of: dap2, edr, wms, zarr"),
    is_public: bool = typer.Option(False, help="Whether the service is public"),
):
    """**Enable** a new service

    **Examples**

    - Enable a new DAP service for _my-org_

        ```
        $ arraylake compute enable my-org dap2
        ```
    """
    with simple_progress(f"Creating [bold]{protocol}[/bold] service for [bold]{org}[/bold]..."):
        status = Client().get_services(org).enable(protocol, is_public)
    rich_console.print(status["message"])


@app.command(name="list")
def list_services(
    org: str = typer.Argument(..., help="The organization name"),
    output: ListOutputType = typer.Option(ListOutputType.rich, help="Output format"),
):
    """**List** enabled services in the specified organization

    **Examples**

    - List services in _my-org_

        ```
        $ arraylake compute list my-org
        ```
    """
    with simple_progress(f"Listing services for [bold]{org}[/bold]..."):
        services = Client().get_services(org).list_enabled()

    if output == "json":
        services = [service.dict() for service in services]  # type: ignore
        print_json(data=services)
    elif services:
        rich_console.print(_services_table(services, org))
    else:
        rich_console.print("\nNo results")


@app.command(name="status")
def get_service_status(
    org: str = typer.Argument(..., help="The organization where the service is enabled"),
    service_id: str = typer.Argument(..., help="The service ID"),
):
    """**Get** the status of a service

    **Examples**

    - Get the status of a service with ID edr-1234567

        ```
        $ arraylake compute status my-org edr-1234567
        ```
    """
    with simple_progress(f"Getting service status for [bold]{service_id}[/bold]..."):
        status = Client().get_services(org).get_status(service_id)

    rich_console.print(status)


@app.command(name="logs")
def get_service_logs(
    org: str = typer.Argument(..., help="The organization where the service is enabled"),
    service_id: str = typer.Argument(..., help="The service ID"),
):
    """**Get** the logs of a service

    **Examples**

    - Get the logs of a service with ID edr-1234567

        ```
        $ arraylake compute logs my-org edr-1234567
        ```
    """
    with simple_progress(f"Getting service logs for [bold]{service_id}[/bold]..."):
        logs = Client().get_services(org).get_logs(service_id)

    rich_console.print(logs)


@app.command(name="disable")
def disable_service(
    org: str = typer.Argument(..., help="The organization that the service belongs to"),
    service_id: str = typer.Argument(..., help="The service ID to disable"),
):
    """**Disable** a service

    **Examples**

    - Disable a service with ID edr-1234567

        ```
        $ arraylake compute disable my-org edr-1234567
        ```
    """
    with simple_progress(f"Disabling service [bold]{service_id}[/bold]..."):
        status = Client().get_services(org).disable(service_id)

    rich_console.print(status["message"])
