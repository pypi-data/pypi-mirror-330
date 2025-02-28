from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field, SecretStr, field_serializer

from .common.common import CANDELA_DIR, CustomDumper


class UserProfile(BaseModel):
    domain: str
    user_id: str
    api_url: str
    access_token: SecretStr
    default_model: str | None
    default_slot_type: str | None = None
    description: str | None = None

    @field_serializer("access_token", when_used="json")
    def dump_secret(self, v):
        return v.get_secret_value()

    def __repr__(self):
        return yaml.dump(self.model_dump(), Dumper=CustomDumper)

    def __str__(self):
        return yaml.dump(self.model_dump(), Dumper=CustomDumper)


class UserProfiles(BaseModel):

    current: str | None = None
    profiles: dict[str, UserProfile] = Field(default_factory=dict)

    def __repr__(self):
        return yaml.dump(self.model_dump(), Dumper=CustomDumper)

    def __str__(self):
        return yaml.dump(self.model_dump(), Dumper=CustomDumper)

    def get(self, profile_name: str | None = None) -> UserProfile:
        if profile_name is None:
            return self.profiles[self.current]
        self._assert_in(profile_name)
        return self.profiles[profile_name]

    def add(self, profile_name: str, profile: UserProfile, as_current: bool = False):
        if not isinstance(profile_name, str):
            raise TypeError("Profile name must be a string.")
        if not isinstance(profile, UserProfile):
            raise TypeError("Profile object must be a UserProfile instance.")

        self.profiles[profile_name] = profile
        if as_current:
            self.current = profile_name
        self.save_cfg()

    def set_current(self, profile_name: str):
        self._assert_in(profile_name)
        self.current = profile_name
        self.save_cfg()

    def delete(self, profile_name: str):
        self._assert_in(profile_name)
        del self.profiles[profile_name]
        self.save_cfg()

    def has_profile(self, profile_name) -> bool:
        return profile_name in self.profiles

    def _assert_in(self, profile_name: str):
        if not self.has_profile(profile_name):
            raise ValueError(f'There is no profile called "{profile_name}".')

    @classmethod
    def load_cfg(cls, fpath: str | Path = None):
        if fpath is None:
            fpath = CANDELA_DIR / "user_profiles.json"
        else:
            fpath = Path(fpath)
        if not fpath.exists():
            default = UserProfiles()
            default.save_cfg(fpath)
        with open(fpath, "r") as f:
            return cls.model_validate_json(f.read())

    def save_cfg(self, fpath: str | Path = None):
        if fpath is None:
            fpath = CANDELA_DIR / "user_profiles.json"
        else:
            fpath = Path(fpath)
        fpath.parent.mkdir(parents=True, exist_ok=True)
        with open(fpath, "w") as f:
            jstr = self.model_dump_json(indent=2)
            f.write(jstr)


def import_from_lumipy():

    import lumipy as lm

    p = UserProfiles.load_cfg()

    lm_cfg = Path(lm.config.cfg_file)
    if not lm_cfg.exists():
        return

    with open(lm_cfg, "r") as f:

        active = None

        for line in f.read().split("\n"):

            if not line.startswith("#"):
                active = line.split()[0]

            line = line.lstrip("#")
            domain, token = line.split(" : ")

            profile = UserProfile(
                domain=domain,
                user_id="pass",
                api_url=f"https://{domain}.lusid.com/candela",
                access_token=token,
                default_model="llama3-8b-q6k",
                default_slot_type="gpu-medium",
                description="Imported from lumipy.",
            )
            p.add(domain, profile)

        if active:
            p.set_current(active)


def get_profiles() -> UserProfiles:

    user_profiles_path = CANDELA_DIR / "user_profiles.json"
    if not user_profiles_path.exists():
        import_from_lumipy()

    return UserProfiles.load_cfg()


def add_profile():
    from candela_kit.common.common import indent_str, print_subtitle

    print_subtitle("Candela Profile Wizard")

    name = input("    Profile name: ")
    domain = input("    Domain: ")
    token = input("    Token: ")

    profile = UserProfile(
        domain=domain,
        user_id="pass",
        api_url=f"https://{domain}.lusid.com/candela",
        access_token=token,
        default_model="llama3-8b-q6k",
        default_slot_type="gpu-medium",
    )

    print()
    print_subtitle(name)
    print(indent_str(repr(profile), 4))
    print("Is this correct?")

    confirm = None
    while confirm not in ("y", "n"):

        confirm = input("  (y/n)").strip().lower()
        if confirm == "y":
            print("Adding profile...")
            get_profiles().add(name, profile)
            break
        elif confirm == "n":
            print("Profile not added.")
            break
        else:
            print("Invalid input. Please enter y or n.")
