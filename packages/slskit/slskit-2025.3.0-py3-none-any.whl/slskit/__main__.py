import json
import logging
import sys
from typing import List
from unittest.mock import patch

import click
import colorlog
import salt.output
import salt.runners.fileserver
import salt.runners.saltutil
import salt.utils.yaml
from salt.state import HashableOrderedDict
from salt.utils.yamldumper import SafeOrderedDumper, represent_ordereddict

import slskit.lib.cli
import slskit.lib.logging
import slskit.pillar
import slskit.state
import slskit.template
from slskit import PACKAGE_NAME, VERSION
from slskit.opts import DEFAULT_CONFIG_PATHS, Config
from slskit.types import AnyDict, MinionDict


@click.group()
@click.version_option(version=VERSION)
@click.option(
    "-c",
    "--config",
    "config_path",
    help=(
        f"path to {PACKAGE_NAME} configuration file "
        f"(default: {' or '.join(DEFAULT_CONFIG_PATHS)})"
    ),
)
@click.option(
    "-l",
    "--log-level",
    default="WARNING",
    type=click.Choice(slskit.lib.logging.LEVEL_CHOICES),
)
@click.option(
    "--salt-output",
    help="Alternative Salt outputter, e.g. nested, json, yaml, etc.",
)
@click.pass_context
def cli(ctx: click.Context, config_path: str, log_level: str, salt_output: str) -> None:
    dynamic_overrides = {}
    if salt_output:
        dynamic_overrides["output"] = salt_output

    ctx.ensure_object(dict)
    ctx.obj["config"] = Config(config_path, dynamic_overrides)

    log_level = getattr(logging, log_level)
    colorlog.basicConfig(level=log_level, force=True)


@cli.command(help="render highstate for specified minions")
@slskit.lib.cli.minion_id_argument()
@click.pass_context
def highstate(ctx: click.Context, minion_id: List[str]) -> None:
    minion_dict = slskit.state.show_highstate(minion_id, ctx.obj["config"])
    _output(minion_dict, ctx.obj["config"])


@cli.command(help="render a given sls for specified minions")
@click.argument("sls")
@slskit.lib.cli.minion_id_argument()
@click.pass_context
def sls(ctx: click.Context, sls: str, minion_id: List[str]) -> None:
    minion_ids = minion_id or ctx.obj["config"].roster.keys()
    minion_dict = slskit.state.show_sls(minion_ids, sls, ctx.obj["config"])
    _output(minion_dict, ctx.obj["config"])


@cli.command(help="render pillar items for specified minions")
@slskit.lib.cli.minion_id_argument()
@click.pass_context
def pillars(ctx: click.Context, minion_id: List[str]) -> None:
    minion_ids = minion_id or ctx.obj["config"].roster.keys()
    minion_dict = slskit.pillar.items(minion_ids, ctx.obj["config"])
    _output(minion_dict, ctx.obj["config"])


@cli.command(help="render a file template for specified minions")
@click.argument("path")
@slskit.lib.cli.minion_id_argument()
@click.option(
    "--renderer",
    default="jinja",
    help="renderer to be used (default: jinja)",
)
@click.option(
    "--context",
    default="{}",
    type=json.loads,
    help="JSON object containing extra variables to be passed into the renderer",
)
@click.pass_context
def template(
    ctx: click.Context, path: str, minion_id: List[str], renderer: str, context: AnyDict
) -> None:
    minion_ids = minion_id or ctx.obj["config"].roster.keys()
    minion_dict = slskit.template.render(
        minion_ids, ctx.obj["config"], path, renderer, context
    )
    _output(minion_dict, ctx.obj["config"])


@cli.command(help="invoke saltutil.sync_all runner")
@click.pass_context
def refresh(ctx: click.Context) -> None:
    with patch("salt.runners.fileserver.__opts__", ctx.obj["config"].opts, create=True):
        salt.runners.fileserver.update()
    with patch("salt.runners.saltutil.__opts__", ctx.obj["config"].opts, create=True):
        salt.runners.saltutil.sync_all()


def _output(minion_dict: MinionDict, config: Config) -> None:
    # workaround for broken yaml output, see https://github.com/saltstack/salt/issues/66594
    if config.opts.get("output") == "yaml":
        SafeOrderedDumper.add_representer(HashableOrderedDict, represent_ordereddict)

    salt.output.display_output(minion_dict.output, opts=config.opts)
    if not minion_dict.all_valid:
        sys.exit(1)


cli()
