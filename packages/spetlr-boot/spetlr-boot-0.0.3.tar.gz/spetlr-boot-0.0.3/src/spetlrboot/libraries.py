import io
import json
from contextlib import redirect_stdout

from pip._internal.cli.main import main as pip_main


class SimpleVersion(tuple):
    """To avoid dependencies, I will not use the packaging library here.
    This simple class only supports numeric 3 level versions, which is the only
    thing I have ever encountered in the wild."""

    @classmethod
    def parse(cls, version: str) -> "SimpleVersion":
        parts = version.split(".")
        major, minor, patch, *_ = *parts, 0, 0
        return SimpleVersion((int(major), int(minor), int(patch)))

    def __str__(self):
        return f"{self[0]}.{self[1]}.{self[2]}"


def pipfreeze2dict():
    f = io.StringIO()
    with redirect_stdout(f):
        pip_main(["list", "--format", "json"])
    out = f.getvalue()
    return {lib["name"]: SimpleVersion.parse(lib["version"]) for lib in json.loads(out)}


def keep_new(libs, reference):
    out = {}
    for lib, version in libs.items():
        if lib not in reference:
            out[lib] = version
        elif reference[lib] != version:
            out[lib] = version
    return out
