import warnings
from enum import Enum
from pathlib import Path
from typing import Optional, cast

import typer
from rich import print_json
from rich.table import Table

from arraylake import AsyncClient
from arraylake.cli.utils import coro, rich_console, simple_progress
from arraylake.log_util import get_logger
from arraylake.repos.icechunk.utils import _raise_if_no_icechunk
from arraylake.types import RepoKind, RepoOperationMode

app = typer.Typer(help="Manage Arraylake repositories", no_args_is_help=True)
logger = get_logger(__name__)


class ListOutputType(str, Enum):
    rich = "rich"
    json = "json"


def _repos_table(repos, org):
    table = Table(title=f"Arraylake Repositories for [bold]{org}[/bold]", min_width=80)
    table.add_column("Name", justify="left", style="cyan", no_wrap=True, min_width=45)
    table.add_column("Created", justify="right", style="green", min_width=25)
    table.add_column("Updated", justify="right", style="green", min_width=25)
    table.add_column("Kind", justify="right", style="green", min_width=10)
    table.add_column("Status", justify="right", style="green", min_width=15)

    mode_colors = {"online": "green", "maintenance": "yellow", "offline": "red"}

    for repo in repos:
        table.add_row(
            repo.name,
            repo.created.isoformat(),
            repo.updated.isoformat(),
            repo.kind,
            repo.status.mode,
            style=mode_colors[repo.status.mode],
        )

    return table


@app.command(name="list")
@coro  # type: ignore
async def list_repos(
    org: str = typer.Argument(..., help="The organization name"),
    output: ListOutputType = typer.Option("rich", help="Output formatting"),
):
    """**List** repositories in the specified organization

    **Examples**

    - List repos in _default_ org

        ```
        $ arraylake repo list my-org
        ```
    """
    with simple_progress(f"Listing repos for [bold]{org}[/bold]...", quiet=(output != "rich")):
        repos = await AsyncClient().list_repos(org)

    if output == "json":
        repos = [r._asdict() for r in repos]
        print_json(data=repos)
    elif repos:
        rich_console.print(_repos_table(repos, org))
    else:
        rich_console.print("\nNo results")


@app.command()
@coro  # type: ignore
async def create(
    repo_name: str = typer.Argument(..., help="Name of repository {ORG}/{REPO_NAME}"),
    bucket_config_nickname: Optional[str] = typer.Option(None, help="Chunkstore bucket config nickname"),
    bucket_nickname: Optional[str] = typer.Option(None, help="Chunkstore bucket config nickname (DEPRECATED)"),
    kind: Optional[RepoKind] = typer.Option(None, help="Kind of repository"),
):
    """**Create** a new repository

    **Examples**

    - Create new repository

        ```
        $ arraylake repo create my-org/example-repo --bucket-config-nickname arraylake-bucket
        ```
    """
    if bucket_nickname:
        bucket_config_nickname = bucket_nickname
        warnings.warn(
            "bucket-nickname has been renamed to bucket-config-nickname and will be removed in Arraylake 0.10",
            FutureWarning,
        )
    with simple_progress(f"Creating repo [bold]{repo_name}[/bold]..."):
        await AsyncClient().create_repo(repo_name, bucket_config_nickname=bucket_config_nickname, kind=kind)


@app.command()
@coro  # type: ignore
async def delete(
    repo_name: str = typer.Argument(..., help="Name of repository {ORG}/{REPO_NAME}"),
    confirm: bool = typer.Option(False, help="confirm deletion without prompting"),
):
    """**Delete** a repository

    **Examples**

    - Delete repository without confirmation prompt

        ```
        $ arraylake repo delete my-org/example-repo --confirm
        ```
    """
    if not confirm:
        confirm = typer.confirm(
            f"This will permanently remove the {repo_name} repo. Are you sure you want to continue?",
            abort=True,
        )

    client = AsyncClient()
    repo_obj = await client.get_repo_object(repo_name)

    with simple_progress(f"Deleting repo [bold]{repo_name}[/bold]..."):
        await client.delete_repo(repo_name, imsure=confirm, imreallysure=confirm)

    # If the repo is a icechunk repo, print message that the bucket must be deleted manually
    if repo_obj.kind == "icechunk":
        rich_console.print(
            f"Repo [bold]{repo_name}[/bold] removed from Arraylake. \n" f"The underlying Icechunk bucket must be deleted manually."
        )


@app.command()
@coro  # type: ignore
async def tree(
    repo_name: str = typer.Argument(..., help="Name of repository {ORG}/{REPO_NAME}"),
    depth: int = typer.Option(10, help="Maximum depth to descend into hierarchy."),
    prefix: str = typer.Option("", help="Path in repo to start the hierarchy, e.g. `root/foo`."),
    output: ListOutputType = typer.Option("rich", help="Output formatting"),
):
    """Show tree representation of a repository

    **Examples**

    - Show the tree representation of a repo up to level 5

        ```
        $ arraylake repo tree my-org/example-repo --depth 5
        ```
    """

    client = AsyncClient()
    repo = await client.get_repo(repo_name, checkout=False)
    repo_obj = await client.get_repo_object(repo_name)

    if repo_obj.kind == "icechunk":
        _raise_if_no_icechunk()
        import zarr
        from icechunk import Repository as IcechunkRepository

        repo = cast(IcechunkRepository, repo)
        session = repo.readonly_session(branch="main")

        try:
            root = await zarr.api.asynchronous.open_group(session.store, mode="r")
        except FileNotFoundError:
            # If the store doesnt have a root group yet, then there is no tree so it is not found
            rich_console.print("Repo is empty!")
            return

        # TODO: support prefix?
        _tree = await root.tree(level=depth)

    else:
        await repo.checkout(for_writing=False)
        _tree = await repo.tree(prefix=prefix, depth=depth)

    if output == "json":
        print_json(_tree.model_dump_json())
    else:
        if repo_obj.kind == "icechunk":
            print(_tree)
        else:
            rich_console.print(_tree._as_rich_tree(name=repo_name))


@app.command(hidden=True)
@coro  # type: ignore
async def get_status(
    repo_name: str = typer.Argument(..., help="Name of repository {ORG}/{REPO_NAME}"),
    output: ListOutputType = typer.Option("rich", help="Output formatting"),
):
    repo = await AsyncClient().get_repo_object(repo_name)
    if output == "json":
        print_json(data=repo.status.model_dump())
    else:
        print(repo.status.mode.value)


@app.command(hidden=True)
@coro  # type: ignore
async def set_status(
    repo_name: str = typer.Argument(..., help="Name of repository {ORG}/{REPO_NAME}"),
    mode: RepoOperationMode = typer.Argument(..., help="An option"),
    message: str = typer.Option(None, help="Optional message to bind to state"),
    output: ListOutputType = typer.Option("rich", help="Output formatting"),
):
    c = AsyncClient()
    await c._set_repo_status(repo_name, mode, message)
    repo = await c.get_repo_object(repo_name)
    if output == "json":
        print_json(data=repo.status.model_dump())
    else:
        print(repo.status.mode.value)


@app.command(name="export")
@coro  # type: ignore
async def export(
    repo_name: str = typer.Argument(..., help="Name of repository {ORG}/{REPO_NAME}"),
    destination: str = typer.Argument(..., help="URI of the export destination"),
    format: str = typer.Option(default="zarr2", help="Format of the export destination"),
    checksum: bool = typer.Option(default=False, help="Validate transferred data via chunk checksums"),
    concurrency: int = typer.Option(default=64, help="Maximum number of concurrent copy operations"),
    ref: Optional[str] = typer.Option(default="main", help="Commit or branch to export from (HEAD of main by default)"),
    from_ref: Optional[str] = typer.Option(default=None, help="Export only the changes between from_ref and ref"),
    extra_config: Optional[Path] = typer.Option(
        default=None,
        help="Path to a YAML file containing configuration options for the destination store",
    ),
):
    """**Export** a repository to the provided destination

    **Examples**

    - Export a repo as of a given commit (HEAD by default)

        ```
        $ arraylake repo export my-org/example-repo s3://my-bucket/my-zarr-mirror --ref abc123 --extra-config creds.yaml
        ```

    The YAML file provided to `--extra-config` may currently contain the following keys:
    - `endpoint_url`
    - `access_key_id`
    - `secret_access_key`
    """

    from arraylake.cli.export import ExportManager, ExportTarget, SupportedExportFormats

    with simple_progress(f"Initializing target at [bold]{destination}[/bold]..."):
        target = ExportTarget(destination, SupportedExportFormats(format), extra_config)

    async with ExportManager(
        repo_name,
        target,
        ref=ref,
        from_ref=from_ref,
        concurrency=concurrency,
        validate=checksum,
    ) as manager:
        await manager.copy_data()
