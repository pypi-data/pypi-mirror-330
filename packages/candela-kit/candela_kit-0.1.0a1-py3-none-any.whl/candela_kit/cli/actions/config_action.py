import click


@click.command(no_args_is_help=True)
@click.argument(
    "action",
    metavar="ACTION",
    type=click.Choice(["add-profile", "set-profile"], case_sensitive=False),
)
@click.argument("profile", metavar="PROFILE", required=False)
def config_main(action: str, profile: str):
    """Manage your Candela config.

    ACTION is the type of action to take. You can choose from 'add-profile', 'set-profile'.

    PROFILE the profile to set as the default.

    """
    from candela_kit import get_profiles
    from candela_kit.profiles import add_profile
    from candela_kit.common.common import print_subtitle, indent_str

    if action == "set-profile":
        profiles = get_profiles()
        profiles.set_current(profile)
        print_subtitle(f"Current profile: {profile}")
        print(indent_str(repr(profiles.get()), 4))

    elif action == "add-profile":
        add_profile()

    else:
        raise ValueError(action)
