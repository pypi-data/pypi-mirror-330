import click
from typing import Literal


MODES = ["quiet", "debug", "developer"]


@click.command(no_args_is_help=True)
@click.argument("app", metavar="APP")
@click.option(
    "--scope",
    help='Specify which scope the object is in, otherwise will use "default".',
    default="default",
)
@click.option(
    "--mode",
    help="Display mode. Possible values are quiet, normal and developer",
    type=str,
    default="developer",
)
@click.option(
    "--app-version", help="Version of app to use. Will default to latest.", default=None
)
def chat_main(
    app: str, scope: str, mode: Literal["quiet", "debug", "developer"], app_version: str
):
    """Start a chat session with an agent.

    APP is the agent app you will run in the session.

    Hint: use the following cli command to view your available apps

        $ candela list apps

    """

    from candela_kit import manager
    from candela_kit.common.common import print_title
    from candela_kit.dtos import ObjectId

    if mode not in MODES:
        values = ", ".join(MODES)
        raise ValueError(f'Invalid mode "{mode}" valid values are {values}')

    app_obj_id = ObjectId(identifier=app, scope=scope, version=app_version)
    manager = manager()

    print_title(
        " Candela CLI",
        app=app_obj_id.label(),
        model=manager.model_id.label(),
        scope=scope,
        mode=mode,
        api_url=manager.profile.api_url,
    )

    with manager.run(app, scope=scope, version=app_version) as agent:
        agent.chat(mode)
