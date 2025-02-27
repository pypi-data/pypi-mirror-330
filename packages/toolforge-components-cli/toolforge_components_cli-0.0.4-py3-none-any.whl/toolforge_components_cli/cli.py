#!/usr/bin/env python3
from __future__ import annotations

import json
import logging
import os
import subprocess
import sys

import click
import yaml
from toolforge_weld.errors import (
    ToolforgeError,
    ToolforgeUserError,
    print_error_context,
)

from toolforge_components_cli.components import (
    ComponentsClient,
    ComponentsClientUserError,
)
from toolforge_components_cli.config import get_loaded_config

LOGGER = logging.getLogger("toolforge" if __name__ == "__main__" else __name__)

MISSING_CONFIG_MSG = "No CONFIG_FILE provided and no data in stdin. Please provide a config file or pipe data."
ERROR_REPORT_MSG = "Please report this issue to the Toolforge admins if it persists: https://w.wiki/6Zuu"
DELETE_CONFIRM_MSG = (
    "Are you sure you want to delete the configuration? This cannot be undone."
)
DELETE_TOKEN_CONFIRM_MSG = (
    "Are you sure you want to delete the deployment token? This cannot be undone."
)
ABORT_MSG = "Aborting at user's request."
TOKEN_EXISTS_MSG = """A valid deployment token already exists. You can:
- Use 'deploy-token show' to see the current token
- Use 'deploy-token refresh' to create a new token (this will invalidate the current one)
- Use 'deploy-token delete' to remove the current token"""


def handle_error(e: Exception, debug: bool = False) -> None:
    user_error = isinstance(e, ToolforgeUserError)
    prefix = "Error: " if user_error else f"{e.__class__.__name__}: "
    click.echo(click.style(f"{prefix}{e}", fg="red"), err=True)

    if debug:
        LOGGER.exception(e)
        if isinstance(e, ToolforgeError):
            print_error_context(e)
    elif not user_error:
        click.echo(click.style(ERROR_REPORT_MSG, fg="red"), err=True)


def _should_prompt() -> bool:
    return sys.stdin.isatty()


def _display_config(config_data: dict, as_json: bool) -> None:
    if as_json:
        click.echo(json.dumps(config_data, indent=4))
    else:
        yaml_str = yaml.dump(
            data=config_data,
            stream=None,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
        click.echo(yaml_str)


def _display_token(token_data: dict, as_json: bool, prefix: str = "") -> None:
    if as_json:
        click.echo(json.dumps(token_data, indent=4))
    else:
        if prefix:
            click.echo(prefix)
        if token_data:
            click.echo(f"Token: {token_data.get('token')}")
            click.echo(f"Created: {token_data.get('creation_date')}")
        else:
            click.echo("No deployment token found")


def _display_deployment(deployment_data: dict, as_json: bool, prefix: str = "") -> None:
    if as_json:
        click.echo(json.dumps(deployment_data, indent=4))
    else:
        if prefix:
            click.echo(prefix)
        click.echo(f"Deployment ID: {deployment_data.get('deploy_id')}")
        click.echo(f"Created: {deployment_data.get('creation_time')}")
        if deployment_data.get("builds"):
            click.echo("\nBuilds:" if not prefix else "Builds:")
            for component, build in deployment_data["builds"].items():
                click.echo(f"  {component}: {build.get('build_id')}")


@click.version_option(prog_name="Toolforge Components CLI")
@click.group(
    name="toolforge-components", help="Toolforge Components command line interface"
)
@click.option(
    "-v",
    "--verbose",
    help="Show extra verbose output. NOTE: Do not rely on the format of the verbose output.",
    is_flag=True,
    default=(os.environ.get("TOOLFORGE_VERBOSE", "0") == "1"),
    hidden=(os.environ.get("TOOLFORGE_CLI", "0") == "1"),
)
@click.option(
    "-d",
    "--debug",
    help="Show logs to debug the toolforge-components-* packages. For extra verbose output for build or job, see --verbose.",
    is_flag=True,
    default=(os.environ.get("TOOLFORGE_DEBUG", "0") == "1"),
    hidden=(os.environ.get("TOOLFORGE_CLI", "0") == "1"),
)
@click.pass_context
def toolforge_components(ctx, verbose: bool, debug: bool) -> None:
    ctx.ensure_object(dict)
    ctx.obj.update(
        {
            "verbose": verbose,
            "debug": debug,
            "config": get_loaded_config(),
            "components_client": ComponentsClient.from_config(
                config=get_loaded_config()
            ),
        }
    )


@toolforge_components.group(name="config", help="Manage component configurations")
def config():
    """Manage component configurations."""


@config.command(name="create", help="Create or update the tool's configuration.")
@click.argument("CONFIG_FILE", type=click.Path(exists=True), required=False)
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="If set, will output in JSON format",
)
@click.pass_context
def config_create(ctx, config_file: str | None, as_json: bool) -> None:
    components_client = ctx.obj["components_client"]
    display_messages = not as_json

    if config_file is None:
        if _should_prompt():
            click.echo(MISSING_CONFIG_MSG, err=True)
            sys.exit(1)
        config_data = json.load(sys.stdin)
    else:
        with open(config_file) as f:
            config_data = yaml.safe_load(f)

    response = components_client.post(
        "/config", json=config_data, display_messages=display_messages
    )

    if as_json:
        click.echo(json.dumps(response, indent=4))


@config.command(name="show", help="Show the tool's configuration.")
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="If set, will output in JSON format",
)
@click.pass_context
def config_show(ctx, as_json: bool) -> None:
    components_client = ctx.obj["components_client"]
    response = components_client.get("/config", display_messages=(not as_json))
    _display_config(response.get("data", {}), as_json)


@config.command(name="delete", help="Delete the tool's configuration.")
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="If set, will output in JSON format",
)
@click.option(
    "--yes-im-sure",
    help="If set, will not ask for confirmation",
    is_flag=True,
)
@click.pass_context
def config_delete(ctx, as_json: bool, yes_im_sure: bool) -> None:
    components_client = ctx.obj["components_client"]
    display_messages = not as_json

    check_response = components_client.get("/config", display_messages=False)
    if not check_response.get("data"):
        components_client.delete("/config", display_messages=display_messages)
        return

    if not yes_im_sure and not click.confirm(DELETE_CONFIRM_MSG):
        click.echo(ABORT_MSG)
        sys.exit(1)

    response = components_client.delete("/config", display_messages=display_messages)
    _display_config(response.get("data", {}), as_json)


@toolforge_components.group(name="deploy-token", help="Manage deployment tokens")
def deploy_token():
    """Manage deployment tokens."""


@deploy_token.command(
    name="create",
    help="Create a new deployment token. This will fail if a valid token already exists.",
)
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="If set, will output in JSON format",
)
@click.pass_context
def deploy_token_create(ctx, as_json: bool) -> None:
    components_client = ctx.obj["components_client"]

    try:
        response = components_client.post("/deployment/token", display_messages=False)
        _display_token(response.get("data", {}), as_json)
    except ComponentsClientUserError as e:
        if e.context.get("status_code") == 409:
            click.echo(click.style(TOKEN_EXISTS_MSG, fg="red"), err=True)
            sys.exit(1)
        raise


@deploy_token.command(
    name="refresh",
    help="Refresh the existing deployment token. This will invalidate the old token.",
)
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="If set, will output in JSON format",
)
@click.option(
    "--yes-im-sure",
    help="If set, will not ask for confirmation",
    is_flag=True,
)
@click.pass_context
def deploy_token_refresh(ctx, as_json: bool, yes_im_sure: bool) -> None:
    components_client = ctx.obj["components_client"]
    display_messages = not as_json

    if not yes_im_sure and not click.confirm(
        "Are you sure you want to refresh the deployment token? This will invalidate the existing token."
    ):
        click.echo(ABORT_MSG)
        sys.exit(1)

    response = components_client.put(
        "/deployment/token", display_messages=display_messages
    )
    _display_token(response.get("data", {}), as_json, prefix="New deployment token:")


@deploy_token.command(name="show", help="Show the current deployment token.")
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="If set, will output in JSON format",
)
@click.pass_context
def deploy_token_show(ctx, as_json: bool) -> None:
    components_client = ctx.obj["components_client"]
    response = components_client.get(
        "/deployment/token", display_messages=(not as_json)
    )
    _display_token(response.get("data", {}), as_json)


@deploy_token.command(name="delete", help="Delete the current deployment token.")
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="If set, will output in JSON format",
)
@click.option(
    "--yes-im-sure",
    help="If set, will not ask for confirmation",
    is_flag=True,
)
@click.pass_context
def deploy_token_delete(ctx, as_json: bool, yes_im_sure: bool) -> None:
    components_client = ctx.obj["components_client"]
    display_messages = not as_json

    check_response = components_client.get("/deployment/token", display_messages=False)
    if not check_response.get("data"):
        components_client.delete("/deployment/token", display_messages=display_messages)
        return

    if not yes_im_sure and not click.confirm(DELETE_TOKEN_CONFIRM_MSG):
        click.echo(ABORT_MSG)
        sys.exit(1)

    response = components_client.delete(
        "/deployment/token", display_messages=display_messages
    )
    _display_token(
        response.get("data", {}), as_json, prefix="Deleted deployment token:"
    )


@toolforge_components.group(name="deployment", help="Manage deployments")
def deployment():
    """Manage deployments."""


@deployment.command(name="create", help="Create a new deployment.")
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="If set, will output in JSON format",
)
@click.pass_context
def deployment_create(ctx, as_json: bool) -> None:
    components_client = ctx.obj["components_client"]
    display_messages = not as_json

    response = components_client.post("/deployment", display_messages=display_messages)

    if as_json:
        click.echo(json.dumps(response, indent=4))
    else:
        deployment_data = response.get("data", {})
        click.echo(f"Deployment ID: {deployment_data.get('deploy_id')}")
        click.echo(f"Created: {deployment_data.get('creation_time')}")
        if deployment_data.get("builds"):
            click.echo("\nBuilds:")
            for component, build in deployment_data["builds"].items():
                click.echo(f"  {component}: {build.get('build_id')}")


@deployment.command(name="list", help="List all deployments.")
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="If set, will output in JSON format",
)
@click.pass_context
def deployment_list(ctx, as_json: bool) -> None:
    components_client = ctx.obj["components_client"]
    display_messages = not as_json

    response = components_client.get("/deployment", display_messages=display_messages)

    if as_json:
        click.echo(json.dumps(response, indent=4))
        return

    deployments = response.get("data", {}).get("deployments", [])
    for deployment in deployments:
        click.echo(f"\nDeployment ID: {deployment.get('deploy_id')}")
        click.echo(f"Created: {deployment.get('creation_time')}")
        if deployment.get("builds"):
            click.echo("Builds:")
            for component, build in deployment["builds"].items():
                click.echo(f"  {component}: {build.get('build_id')}")


@deployment.command(name="show", help="Show details of a specific deployment.")
@click.argument("deployment_id")
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="If set, will output in JSON format",
)
@click.pass_context
def deployment_show(ctx, deployment_id: str, as_json: bool) -> None:
    components_client = ctx.obj["components_client"]
    response = components_client.get(
        f"/deployment/{deployment_id}", display_messages=(not as_json)
    )
    _display_deployment(response.get("data", {}), as_json)


@deployment.command(name="delete", help="Delete a specific deployment.")
@click.argument("deployment_id")
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="If set, will output in JSON format",
)
@click.option(
    "--yes-im-sure",
    help="If set, will not ask for confirmation",
    is_flag=True,
)
@click.pass_context
def deployment_delete(
    ctx, deployment_id: str, as_json: bool, yes_im_sure: bool
) -> None:
    components_client = ctx.obj["components_client"]
    display_messages = not as_json

    if not yes_im_sure and not click.confirm(
        f"Are you sure you want to delete deployment {deployment_id}? This cannot be undone."
    ):
        click.echo(ABORT_MSG)
        sys.exit(1)

    response = components_client.delete(
        f"/deployment/{deployment_id}", display_messages=display_messages
    )
    _display_deployment(response.get("data", {}), as_json, prefix="Deleted deployment:")


def main() -> int:
    try:
        args = sys.argv[1:]
        debug = "-d" in args or "--debug" in args
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
        toolforge_components(standalone_mode=False)
        return 0
    except click.exceptions.ClickException as e:
        e.show()
        return e.exit_code
    except subprocess.CalledProcessError as e:
        handle_error(e, debug=debug)
        return e.returncode
    except Exception as e:
        handle_error(e, debug=debug)
        return 1


if __name__ == "__main__":
    sys.exit(main())
