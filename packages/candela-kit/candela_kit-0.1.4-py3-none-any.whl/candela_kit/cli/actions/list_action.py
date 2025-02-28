import click


list_types = [
    "apps",
    "circuits",
    "directives",
    "models",
    "sessions",
    "slots",
    "tool_modules",
    "traces",
    "profiles",
]
config_args = click.Choice(list_types, case_sensitive=False)


def list_profiles():
    from candela_kit import get_profiles
    from pandas import DataFrame

    profiles = get_profiles()

    rows = []
    for k, v in profiles.profiles.items():
        rows.append({"name": k, "active": k == profiles.current, **v.model_dump()})
    return DataFrame(rows)


@click.command(no_args_is_help=True)
@click.argument("entity_type", metavar="ENTITY_TYPE", type=config_args)
@click.option(
    "--all-versions",
    type=bool,
    is_flag=True,
    help="Show all versions of an object when listing, otherwise just show latest version.",
)
def list_main(entity_type: str, all_versions: bool):
    """List all entities of a given type in Candela.

    ENTITY_TYPE is the type of entity you want to list. Valid types are apps, circuits, directives, models, sessions,
    tools, tool_modules, traces, profiles

    """

    from candela_kit import client
    from candela_kit.common.common import print_table

    client = client()

    handlers = {
        "apps": (lambda: client.list_apps(all_versions), "App List"),
        "circuits": (lambda: client.list_circuits(all_versions), "Circuit List"),
        "directives": (lambda: client.list_directives(all_versions), "Directive List"),
        "models": (lambda: client.list_models(all_versions), "Model List"),
        "profiles": (lambda: list_profiles(), "Profile List"),
        "sessions": (lambda: client.list_sessions(), "Session List"),
        "slots": (lambda: client.list_slots(), "Slots List"),
        "tool_modules": (
            lambda: client.list_tool_modules(all_versions),
            "Tool Module List",
        ),
        "traces": (lambda: client.list_traces(), "Trace List"),
    }

    handler = handlers.get(entity_type)
    if handler is None:
        raise ValueError(f"Unknown entity type: {entity_type}")
    fn, title = handler
    print_table(fn(), title)
