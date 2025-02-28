import click


list_types = ["app", "directive", "session", "tool_module", "profile"]
config_args = click.Choice(list_types, case_sensitive=False)


def _print_repr(obj, title):
    from candela_kit.common.common import print_subtitle, indent_str

    print_subtitle(title)
    print(indent_str(repr(obj), 4))


def _make_title(entity, identifier, scope, version):
    if entity in ("app", "circuit", "directive", "model", "tool_module"):
        version_str = ":" + version if version else " (latest version)"
        title = f"{entity} {scope}/{identifier}{version_str}"
    elif entity == "session":
        title = f"session {scope}/{identifier}"
    elif entity == "profile":
        title = f"profile {identifier}"
    else:
        raise ValueError(f"Unknown entity {entity}")

    return title[0].upper() + title[1:]


@click.command(no_args_is_help=True)
@click.argument("entity_type", metavar="ENTITY_TYPE", type=config_args)
@click.argument("identifier", metavar="IDENTIFIER")
@click.option(
    "--scope",
    help='Specify which scope the object is in, otherwise will use "default".',
    default="default",
)
@click.option(
    "--version",
    help="Specify which version to delete, otherwise will show the latest.",
    default=None,
)
def show_main(entity_type: str, identifier: str, scope: str, version: str | None):
    """Show information for a given entity type in Candela.

    ENTITY_TYPE is the type of entity you want to show information about. Valid types are app, circuit, directive,
    model, session, tool_module, trace, profile.

    IDENTIFIER is the identifier or name of the specific entity you want to show.

    """

    from candela_kit import client, get_profiles
    from candela_kit.common.common import print_model

    c = client()
    profiles = get_profiles()

    title = _make_title(entity_type, identifier, scope, version)

    handlers = {
        "app": (c.get_app, print_model),
        "directive": (c.get_directive, _print_repr),
        "session": (lambda x, y, z: c.get_session(x, y), print_model),
        "tool_module": (c.get_tool_module, _print_repr),
        "profile": (lambda x, y, z: profiles.get(x), print_model),
    }

    handler = handlers.get(entity_type)
    if handler is None:
        raise ValueError("Unknown entity type: {}".format(entity_type))

    get_obj, print_fn = handler

    obj = get_obj(identifier, scope, version)
    print_fn(obj, title)
