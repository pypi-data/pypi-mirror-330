import os
import pathlib
import shutil
import time
import typing as t

import toml
import typer
from rich import box, print
from rich.live import Live
from rich.prompt import Prompt
from rich.table import Table

from dreadnode_cli import api
from dreadnode_cli.agent import docker
from dreadnode_cli.agent.config import AgentConfig
from dreadnode_cli.agent.docker import get_registry
from dreadnode_cli.agent.format import (
    format_agent,
    format_agent_versions,
    format_run,
    format_run_groups,
    format_runs,
    format_strike_models,
    format_strikes,
)
from dreadnode_cli.agent.templates import cli as templates_cli
from dreadnode_cli.agent.templates.format import format_templates
from dreadnode_cli.agent.templates.manager import TemplateManager
from dreadnode_cli.api import Client
from dreadnode_cli.config import UserConfig
from dreadnode_cli.model.config import UserModels
from dreadnode_cli.model.format import format_user_models
from dreadnode_cli.profile.cli import switch as switch_profile
from dreadnode_cli.types import GithubRepo
from dreadnode_cli.utils import download_and_unzip_archive, get_repo_archive_source_path, pretty_cli

cli = typer.Typer(no_args_is_help=True)

cli.add_typer(templates_cli, name="templates", help="Manage Agent templates")


def ensure_profile(agent_config: AgentConfig, *, user_config: UserConfig | None = None) -> None:
    """Ensure the active agent link matches the current server profile."""

    user_config = user_config or UserConfig.read()

    if not user_config.active_profile_name:
        raise Exception("No server profile is set, use [bold]dreadnode login[/] to authenticate")

    if agent_config.links and not agent_config.has_link_to_profile(user_config.active_profile_name):
        linked_profiles = ", ".join(agent_config.linked_profiles)
        plural = "s" if len(agent_config.linked_profiles) > 1 else ""
        raise Exception(
            f"This agent is linked to the [magenta]{linked_profiles}[/] server profile{plural}, "
            f"but the current server profile is [yellow]{user_config.active_profile_name}[/], "
            "use [bold]dreadnode agent push[/] to create a new link with this profile."
        )

    if agent_config.active_link.profile != user_config.active_profile_name:
        if (
            Prompt.ask(
                f"Current agent link points to the [yellow]{agent_config.active_link.profile}[/] server profile, "
                f"would you like to switch to it?",
                choices=["y", "n"],
                default="y",
            )
            == "n"
        ):
            print()
            raise Exception(
                f"Current agent link ([yellow]{agent_config.active_link.profile}[/]) does not match "
                f"the current server profile ([magenta]{user_config.active_profile_name}[/]). "
                "Use [bold]dreadnode agent switch[/] or [bold]dreadnode profile switch[/]."
            )

        switch_profile(agent_config.active_link.profile)


@cli.command(help="Initialize a new agent project", no_args_is_help=True)
@pretty_cli
def init(
    strike: t.Annotated[str, typer.Argument(help="The target strike")],
    directory: t.Annotated[
        pathlib.Path,
        typer.Option("--dir", "-d", help="The directory to initialize", file_okay=False, resolve_path=True),
    ] = pathlib.Path("."),
    name: t.Annotated[
        str | None, typer.Option("--name", "-n", help="The project name (used for container naming)")
    ] = None,
    template: t.Annotated[
        str | None, typer.Option("--template", "-t", help="The template to use for the agent")
    ] = None,
    source: t.Annotated[
        str | None,
        typer.Option(
            "--source",
            "-s",
            help="Initialize the agent using a custom template from a github repository, ZIP archive URL or local folder",
        ),
    ] = None,
    path: t.Annotated[
        str | None,
        typer.Option(
            "--path",
            "-p",
            help="If --source has been provided, use --path to specify a subfolder to initialize from",
        ),
    ] = None,
) -> None:
    try:
        AgentConfig.read(directory)
        if Prompt.ask(":axe: Agent config exists, overwrite?", choices=["y", "n"], default="n") == "n":
            return
        print()
    except Exception:
        pass

    print(f":coffee: Fetching strike '{strike}' ...")

    client = api.create_client()

    try:
        strike_response = client.get_strike(strike)
    except Exception as e:
        raise Exception(f"Failed to find strike '{strike}': {e}") from e

    print(f":crossed_swords: Linking to strike '{strike_response.name}' ({strike_response.type})")
    print()

    project_name = Prompt.ask(":toolbox: Project name?", default=name or directory.name)
    print()

    directory.mkdir(exist_ok=True)

    template_manager = TemplateManager()
    context = {"project_name": project_name, "strike": strike_response}

    if source is None:
        # get the templates that match the strike
        available_templates = template_manager.get_templates_for_strike(strike_response.name, strike_response.type)
        available: list[str] = list(available_templates.keys())

        # none available
        if not available:
            if not template_manager.templates:
                raise Exception(
                    "No templates installed, use [bold]dreadnode agent templates install[/] to install some."
                )
            else:
                raise Exception("No templates found for the given strike.")

        # ask the user if the template has not been passed via command line
        if template is None:
            print(":notebook: Compatible templates:\n")
            print(format_templates(available_templates, with_index=True))
            print()

            choice = Prompt.ask("Choice ", choices=[str(i + 1) for i in range(len(available))])
            template = available[int(choice) - 1]

        # validate the template
        if template not in available:
            raise Exception(
                f"Template '{template}' not found, use [bold]dreadnode agent templates show[/] to see available templates."
            )

        # install the template
        template_manager.install(template, directory, context)
    else:
        source_dir = pathlib.Path(source)
        cleanup = False

        if not source_dir.exists():
            # source is not a local folder, so it can be:
            # - full ZIP archive URL
            # - github compatible reference

            try:
                github_repo = GithubRepo(source)

                # Check if the repo is accessible
                if github_repo.exists:
                    source_dir = download_and_unzip_archive(github_repo.zip_url)

                # This could be a private repo that the user can access
                # by getting an access token from our API
                elif github_repo.namespace == "dreadnode":
                    github_access_token = client.get_github_access_token([github_repo.repo])
                    print(":key: Accessed private repository")
                    source_dir = download_and_unzip_archive(
                        github_repo.api_zip_url, headers={"Authorization": f"Bearer {github_access_token.token}"}
                    )

                else:
                    raise Exception(f"Repository '{github_repo}' not found or inaccessible")

                # github repos zip archives usually contain a single branch folder, the real source dir,
                # and the path is not known beforehand
                source_dir = get_repo_archive_source_path(source_dir)

            except ValueError:
                # not a repo, download and unzip as a ZIP archive URL
                source_dir = download_and_unzip_archive(source)

            # make sure the temporary directory is cleaned up
            cleanup = True

        try:
            # add subpath if specified
            if path is not None:
                source_dir = source_dir / path

            # install the template
            template_manager.install_from_dir(source_dir, directory, context)
        except Exception:
            if cleanup and source_dir.exists():
                shutil.rmtree(source_dir)
            raise

    # Wait to write this until after the template is installed
    AgentConfig(project_name=project_name, strike=strike).write(directory=directory)

    print()
    print(f"Initialized [b]{directory}[/]")


@cli.command(help="Push a new version of the active agent")
@pretty_cli
def push(
    directory: t.Annotated[
        pathlib.Path,
        typer.Option("--dir", "-d", help="The agent directory", file_okay=False, resolve_path=True),
    ] = pathlib.Path("."),
    tag: t.Annotated[str | None, typer.Option("--tag", "-t", help="The tag to use for the image")] = None,
    env_vars: t.Annotated[
        list[str] | None,
        typer.Option("--env-var", "-e", help="Environment vars to use when executing the image (key=value)"),
    ] = None,
    new: t.Annotated[bool, typer.Option("--new", "-n", help="Create a new agent instead of a new version")] = False,
    notes: t.Annotated[str | None, typer.Option("--message", "-m", help="Notes for the new version")] = None,
    rebuild: t.Annotated[bool, typer.Option("--rebuild", "-r", help="Force rebuild the agent image")] = False,
) -> None:
    env = {env_var.split("=")[0]: env_var.split("=")[1] for env_var in env_vars or []}

    agent_config = AgentConfig.read(directory)
    user_config = UserConfig.read()

    if not user_config.active_profile_name:
        raise Exception("No server profile is set, use [bold]dreadnode login[/] to authenticate")

    if agent_config.links and not agent_config.has_link_to_profile(user_config.active_profile_name):
        print(f":link: Linking as a fresh agent to the current profile [magenta]{user_config.active_profile_name}[/]")
        print()
        new = True
    elif agent_config.active and agent_config.active_link.profile != user_config.active_profile_name:
        raise Exception(
            f"Current agent link ([yellow]{agent_config.active_link.profile}[/]) does not match "
            f"the current server profile ([magenta]{user_config.active_profile_name}[/]). "
            "Use [bold]dreadnode agent switch[/] or [bold]dreadnode profile switch[/]."
        )

    server_config = user_config.get_server_config()

    registry = get_registry(server_config)

    print(f":key: Authenticating with [bold]{registry}[/] ...")
    docker.login(registry, server_config.username, server_config.api_key)

    print()
    print(f":wrench: Building agent from [b]{directory}[/] ...")
    image = docker.build(directory, force_rebuild=rebuild)
    agent_name = docker.sanitized_name(agent_config.project_name)
    sanitized_user_name = docker.sanitized_name(server_config.username)

    if not agent_name:
        raise Exception("Failed to sanitize agent name, please use a different name")

    elif agent_name != agent_config.project_name:
        print(f":four_leaf_clover: Agent name normalized to [bold magenta]{agent_name}[/]")

    if not sanitized_user_name:
        raise Exception("Failed to sanitize username")

    elif sanitized_user_name != server_config.username:
        print(f":four_leaf_clover: Username normalized to [bold magenta]{sanitized_user_name}[/]")

    repository = f"{registry}/{sanitized_user_name}/agents/{agent_name}"
    tag = tag or image.id[-8:]

    print()
    print(f":package: Pushing agent to [b]{repository}:{tag}[/] ...")
    docker.push(image, repository, tag)

    client = api.create_client()
    container = api.Client.Container(image=f"{repository}:{tag}", env=env, name=None)

    if new or not agent_config.links:
        print()
        print(":robot: Creating a new agent ...")
        name = Prompt.ask("Agent name?", default=agent_config.project_name)
        notes = notes or Prompt.ask("Notes?")

        agent = client.create_strike_agent(container, name, strike=agent_config.strike, notes=notes)
        agent_config.add_link(agent.key, agent.id, user_config.active_profile_name).write(directory)
    else:
        active_agent_id = agent_config.active
        if active_agent_id is None:
            raise Exception("No active agent link found. Use 'switch' command to set an active link.")

        print()
        print(":robot: Creating a new version ...")
        notes = notes or Prompt.ask("Notes?")

        try:
            agent = client.create_strike_agent_version(str(active_agent_id), container, notes)
        except Exception as e:
            # 404 is expected if the agent was created on a different server profile
            if str(e).startswith("404"):
                raise Exception(
                    f"Agent '{active_agent_id}' not found for the current server profile, create the agent again."
                ) from e
            else:
                raise e

    print(format_agent(agent))

    print()
    print(":tada: Agent pushed. use [bold]dreadnode agent deploy[/] to start a new run.")


def prepare_run_context(
    env_vars: list[str] | None, parameters: list[str] | None, command: str | None
) -> Client.StrikeRunContext | None:
    if not env_vars and not parameters and not command:
        return None

    context = Client.StrikeRunContext()

    if env_vars:
        context.environment = {env_var.split("=")[0]: env_var.split("=")[1] for env_var in env_vars}

    if parameters:
        context.parameters = {}
        for param in parameters:
            if param.startswith("@"):
                context.parameters.update(toml.load(open(param[1:])))
            else:
                context.parameters.update(toml.loads(param))

    if command:
        context.command = command

    return context


@cli.command(help="Start a new run using the latest active agent version")
@pretty_cli
def deploy(
    model: t.Annotated[
        str | None, typer.Option("--model", "-m", help="The inference model to use for this run")
    ] = None,
    directory: t.Annotated[
        pathlib.Path,
        typer.Option("--dir", "-d", help="The agent directory", file_okay=False, resolve_path=True),
    ] = pathlib.Path("."),
    env_vars: t.Annotated[
        list[str] | None,
        typer.Option("--env-var", "-e", help="Environment vars to override for this run (key=value)"),
    ] = None,
    parameters: t.Annotated[
        list[str] | None,
        typer.Option(
            "--param",
            "-p",
            help="Define custom parameters for this run (key = value in toml syntax or @filename.toml for multiple values)",
        ),
    ] = None,
    command: t.Annotated[
        str | None,
        typer.Option("--command", "-c", help="Override the container command for this run."),
    ] = None,
    strike: t.Annotated[str | None, typer.Option("--strike", "-s", help="The strike to use for this run")] = None,
    watch: t.Annotated[bool, typer.Option("--watch", "-w", help="Watch the run status")] = True,
    group: t.Annotated[str | None, typer.Option("--group", "-g", help="Group to associate this run with")] = None,
) -> None:
    agent_config = AgentConfig.read(directory)
    ensure_profile(agent_config)

    user_config = UserConfig.read()
    server_config = user_config.get_server_config()

    active_link = agent_config.active_link

    client = api.create_client()
    agent = client.get_strike_agent(active_link.id)

    strike = strike or agent_config.strike
    if strike is None:
        raise Exception("No strike specified, use -s/--strike or set the strike in the agent config")

    context = prepare_run_context(env_vars, parameters, command)

    user_models = UserModels.read()
    user_model: Client.UserModel | None = None

    # Check for a user-defined model
    if model in user_models.models:
        user_model = Client.UserModel(
            key=model,
            generator_id=user_models.models[model].generator_id,
            api_key=user_models.models[model].api_key,
        )

        # Resolve the API key from env vars
        if user_model.api_key.startswith("$"):
            try:
                user_model.api_key = os.environ[user_model.api_key[1:]]
            except KeyError as e:
                raise Exception(
                    f"API key cannot be read from '{user_model.api_key}', environment variable not found."
                ) from e

    # Otherwise we'll ensure this is a valid strike-native model
    if user_model is None and model is not None:
        strike_response = client.get_strike(strike)
        if not any(m.key == model for m in strike_response.models):
            models(directory, strike=strike)
            print()
            raise Exception(
                f"Model '{model}' is not user-defined nor is it available in strike '{strike_response.name}'"
            )

    run = client.start_strike_run(
        agent.latest_version.id, strike=strike, model=model, user_model=user_model, group=group, context=context
    )
    agent_config.add_run(run.id).write(directory)
    formatted = format_run(run, server_url=server_config.url)

    if not watch:
        print(formatted)
        return

    with Live(formatted, refresh_per_second=2) as live:
        while run.is_running():
            time.sleep(1)
            run = client.get_strike_run(run.id)
            live.update(format_run(run, server_url=server_config.url))


@cli.command(help="List available models for the current (or specified) strike")
@pretty_cli
def models(
    directory: t.Annotated[
        pathlib.Path, typer.Argument(help="The agent directory", file_okay=False, resolve_path=True)
    ] = pathlib.Path("."),
    strike: t.Annotated[str | None, typer.Option("--strike", "-s", help="The strike to query")] = None,
) -> None:
    user_models = UserModels.read()
    if user_models.models:
        print("[bold]User-defined models:[/]\n")
        print(format_user_models(user_models.models))
        print()

    if strike is None:
        agent_config = AgentConfig.read(directory)
        ensure_profile(agent_config)
        strike = agent_config.strike

    if strike is None:
        raise Exception("No strike specified, use -s/--strike or set the strike in the agent config")

    strike_response = api.create_client().get_strike(strike)
    if user_models.models:
        print("\n[bold]Dreadnode-provided models:[/]\n")
    print(format_strike_models(strike_response.models))


@cli.command(help="List available strikes")
@pretty_cli
def strikes() -> None:
    client = api.create_client()
    strikes = client.list_strikes()
    print(format_strikes(strikes))


@cli.command(help="Show the latest run of the active agent")
@pretty_cli
def latest(
    directory: t.Annotated[
        pathlib.Path,
        typer.Option("--dir", "-d", help="The agent directory", file_okay=False, resolve_path=True),
    ] = pathlib.Path("."),
    verbose: t.Annotated[bool, typer.Option("--verbose", "-v", help="Show detailed run information")] = False,
    logs: t.Annotated[
        bool, typer.Option("--logs", "-l", help="Show all container logs for the run (only in verbose mode)")
    ] = False,
    raw: t.Annotated[bool, typer.Option("--raw", help="Show raw JSON output")] = False,
) -> None:
    agent_config = AgentConfig.read(directory)
    ensure_profile(agent_config)

    user_config = UserConfig.read()
    server_config = user_config.get_server_config()

    active_link = agent_config.active_link
    if not active_link.runs:
        print(":exclamation: No runs yet, use [bold]dreadnode agent deploy[/]")
        return

    client = api.create_client()
    run = client.get_strike_run(str(active_link.runs[-1]))

    if raw:
        print(run.model_dump(mode="json"))
    else:
        print(format_run(run, verbose=verbose, include_logs=logs, server_url=server_config.url))


@cli.command(help="Export all run information for the active agent")
@pretty_cli
def export(
    directory: t.Annotated[
        pathlib.Path,
        typer.Option("--dir", "-d", help="The export directory", file_okay=False, resolve_path=True),
    ] = pathlib.Path("export"),
    strike: t.Annotated[str | None, typer.Option("--strike", "-s", help="Export runs for a specific strike")] = None,
    group: t.Annotated[str | None, typer.Option("--group", "-g", help="Export runs from a specific group")] = None,
) -> None:
    agent_config = AgentConfig.read()
    ensure_profile(agent_config)

    client = api.create_client()
    run_summaries = client.list_strike_runs(
        strike=strike or agent_config.strike, group=group, agent=agent_config.active_link.id
    )

    print(f":package: Exporting {len(run_summaries)} runs to [b]{directory}[/] ...")

    directory.mkdir(exist_ok=True)
    for summary in run_summaries:
        print(f" |- {summary.key} ({summary.id}) ...")
        run = client.get_strike_run(summary.id)
        with (directory / f"{run.key}_{run.id}.json").open("w") as f:
            f.write(run.model_dump_json())


@cli.command(help="Show the status of the active agent")
@pretty_cli
def show(
    directory: t.Annotated[
        pathlib.Path,
        typer.Option("--dir", "-d", help="The agent directory", file_okay=False, resolve_path=True),
    ] = pathlib.Path("."),
) -> None:
    agent_config = AgentConfig.read(directory)
    ensure_profile(agent_config)

    client = api.create_client()
    agent = client.get_strike_agent(agent_config.active_link.id)
    print(format_agent(agent))


@cli.command(help="List historical versions of the active agent")
@pretty_cli
def versions(
    directory: t.Annotated[
        pathlib.Path, typer.Argument(help="The agent directory", file_okay=False, resolve_path=True)
    ] = pathlib.Path("."),
) -> None:
    agent_config = AgentConfig.read(directory)
    ensure_profile(agent_config)

    client = api.create_client()
    agent = client.get_strike_agent(agent_config.active_link.id)
    print(format_agent_versions(agent))


@cli.command(help="List runs for the active agent")
@pretty_cli
def runs(
    directory: t.Annotated[
        pathlib.Path, typer.Argument(help="The agent directory", file_okay=False, resolve_path=True)
    ] = pathlib.Path("."),
) -> None:
    agent_config = AgentConfig.read(directory)
    ensure_profile(agent_config)

    client = api.create_client()
    runs = [
        run for run in client.list_strike_runs() if run.id in agent_config.active_link.runs and run.start is not None
    ]
    runs = sorted(runs, key=lambda r: r.start or 0, reverse=True)

    if not runs:
        print(":exclamation: No runs yet, use [bold]dreadnode agent deploy[/]")
        return

    print(format_runs(runs))


@cli.command(help="List available agent links")
@pretty_cli
def links(
    directory: t.Annotated[
        pathlib.Path, typer.Argument(help="The agent directory", file_okay=False, resolve_path=True)
    ] = pathlib.Path("."),
) -> None:
    agent_config = AgentConfig.read(directory)
    user_config = UserConfig.read()
    _ = agent_config.active_link

    table = Table(box=box.ROUNDED)
    table.add_column("Key", style="magenta")
    table.add_column("Name", style="cyan")
    table.add_column("Profile")
    table.add_column("ID")

    for key, link in agent_config.links.items():
        active_link = key == agent_config.active
        mismatched_profile = active_link and user_config.active_profile_name != link.profile
        client = api.create_client(profile=agent_config.links[key].profile)
        agent = client.get_strike_agent(link.id)
        table.add_row(
            agent.key + ("*" if active_link else ""),
            agent.name or "N/A",
            link.profile + ("[bold red]* (not-active)[/]" if mismatched_profile else ""),
            f"[dim]{agent.id}[/]",
            style="bold" if active_link else None,
        )

    print(table)


@cli.command(help="Switch to a different agent link", no_args_is_help=True)
@pretty_cli
def switch(
    agent_or_profile: t.Annotated[str, typer.Argument(help="Agent key/id or profile name")],
    directory: t.Annotated[
        pathlib.Path, typer.Argument(help="The agent directory", file_okay=False, resolve_path=True)
    ] = pathlib.Path("."),
) -> None:
    agent_config = AgentConfig.read(directory)

    for key, link in agent_config.links.items():
        if agent_or_profile in (key, link.id) or agent_or_profile == link.profile:
            print(
                f":robot: Switched to link [bold magenta]{key}[/] for profile [cyan]{link.profile}[/] ([dim]{link.id}[/])"
            )
            agent_config.active = key
            agent_config.write(directory)
            return

    print(f":exclamation: '{agent_or_profile}' not found, use [bold]dreadnode agent links[/]")


@cli.command(help="List strike run groups")
@pretty_cli
def run_groups() -> None:
    client = api.create_client()
    groups = client.list_strike_run_groups()
    print(format_run_groups(groups))


@cli.command(help="Clone a github repository", no_args_is_help=True)
@pretty_cli
def clone(
    repo: t.Annotated[str, typer.Argument(help="Repository name or URL")],
    target: t.Annotated[
        pathlib.Path | None, typer.Argument(help="The target directory", file_okay=False, resolve_path=True)
    ] = None,
) -> None:
    github_repo = GithubRepo(repo)

    # Check if the target directory exists
    target = target or pathlib.Path(github_repo.repo)
    if target.exists():
        if Prompt.ask(f":axe: Overwrite {target.absolute()}?", choices=["y", "n"], default="n") == "n":
            return
        print()
        shutil.rmtree(target)

    # Check if the repo is accessible
    if github_repo.exists:
        temp_dir = download_and_unzip_archive(github_repo.zip_url)

    # This could be a private repo that the user can access
    # by getting an access token from our API
    elif github_repo.namespace == "dreadnode":
        github_access_token = api.create_client().get_github_access_token([github_repo.repo])
        print(":key: Accessed private repository")
        temp_dir = download_and_unzip_archive(
            github_repo.api_zip_url, headers={"Authorization": f"Bearer {github_access_token.token}"}
        )

    else:
        raise Exception(f"Repository '{github_repo}' not found or inaccessible")

    # We assume the repo download results in a single
    # child folder which is the real target
    sub_dirs = list(temp_dir.iterdir())
    if len(sub_dirs) == 1 and sub_dirs[0].is_dir():
        temp_dir = sub_dirs[0]

    shutil.move(temp_dir, target)

    print()
    print(f":tada: Cloned [b]{repo}[/] to [b]{target.absolute()}[/]")
