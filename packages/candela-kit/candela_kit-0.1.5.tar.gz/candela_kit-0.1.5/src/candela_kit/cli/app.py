import click
from .actions.list_action import list_main
from .actions.chat_action import chat_main
from .actions.config_action import config_main
from .actions.delete_action import delete_main
from .actions.show_action import show_main


@click.group(no_args_is_help=True)
def cli():
    """Welcome to the candela-kit CLI"""
    pass


cli.add_command(list_main, "list")
cli.add_command(chat_main, "chat")
cli.add_command(config_main, "config")
cli.add_command(delete_main, "delete")
cli.add_command(show_main, "show")

if __name__ == "__main__":
    cli()
