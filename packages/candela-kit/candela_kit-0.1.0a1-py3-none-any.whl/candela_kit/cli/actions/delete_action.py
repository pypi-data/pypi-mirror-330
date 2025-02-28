import click


def _label_fn(entity, identifier, scope, version):
    if entity in ("app", "circuit", "directive", "model", "tool_module"):
        version_str = ":" + version if version else " (any version)"
        return f"{entity} {scope}/{identifier}{version_str}"
    elif entity == "session":
        return f"session {scope}/{identifier}"
    elif entity == "profile":
        return f"profile {identifier}"


def _ask_confirmation(del_fn, exists_fn, entity, identifier, scope, version):

    label = _label_fn(entity, identifier, scope, version)
    if not exists_fn(identifier, scope, version):
        print(f"The {label} does not exist.")
        return

    print(f"Are you sure you want to delete {label}?")

    confirm = None
    while confirm not in ("y", "n"):
        confirm = input("  [y/n]: ").strip().strip()
        if confirm == "y":
            del_fn(identifier, scope, version)
            print("Successfully deleted.")
            break
        elif confirm == "n":
            print("Delete action cancelled.")
            break
        else:
            print("Invalid input. Please enter y or n.")


list_types = [
    "app",
    "circuit",
    "directive",
    "model",
    "session",
    "tool_module",
    "profile",
]
config_args = click.Choice(list_types, case_sensitive=False)


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
    help="Specify which version to delete, otherwise will delete all versions.",
    default=None,
)
def delete_main(entity_type: str, identifier: str, scope: str, version: str | None):
    """Delete an entity of a given type from Candela.

    ENTITY_TYPE is the type of entity you want to delete. Valid options are app, circuit, directive, model, session,
    tool_module, profile.

    IDENTIFIER is the identifier of the entity you want to delete.

    """

    from candela_kit import client, get_profiles

    profiles = get_profiles()
    c = client()

    handlers = {
        "app": (c.delete_app, c.app_exists),
        "circuit": (c.delete_circuit, c.circuit_exists),
        "directive": (c.delete_directive, c.directive_exists),
        "model": (c.delete_model, c.model_exists),
        "session": (
            lambda x, y, z: c.delete_session(x, y),
            lambda x, y, z: c.session_exists(x, y),
        ),
        "tool_module": (c.delete_tool_module, c.tool_module_exists),
        "profile": (
            lambda x, y, z: profiles.delete(x),
            lambda x, y, z: profiles.has_profile(x),
        ),
    }

    handler = handlers.get(entity_type)
    if handler is None:
        raise ValueError(f"Unknown entity type: {entity_type}")
    del_fn, exists_fn = handler
    _ask_confirmation(del_fn, exists_fn, entity_type, identifier, scope, version)
