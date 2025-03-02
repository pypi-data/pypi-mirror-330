from __future__ import annotations

import ast
from pathlib import Path
from typing import Generator, Optional, TypeVar, cast

T = TypeVar("T")


def get_imports(path: Path) -> dict[str, str]:
    tree = ast.parse(path.read_bytes())
    imports: dict[str, str] = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for subnode in node.names:
                imports[subnode.asname or subnode.name] = subnode.name
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:
                for subnode in node.names:
                    imports[subnode.asname or subnode.name] = (
                        f"{node.module}.{subnode.name}"
                    )
    return imports


class Env:
    def __init__(self) -> None:
        self.names_to_paths: dict[str, Path] = {}
        self._name_cache: dict[str, dict[str, str]] = {}

    def add_to_import_path(self, name: str, path: Path) -> None:
        self.names_to_paths[name] = path

    def add_site_packages(self, path: Path) -> None:
        for e in path.iterdir():
            # TODO also check for dashes and other stuff that makes it not importable
            if e.is_dir() and "." not in e.name:
                self.add_to_import_path(e.name, e)
            elif e.suffix == ".py":
                self.add_to_import_path(e.name[:-3], e)

    def real_qualname(self, fqn: str) -> str:
        # TODO detect cycles
        name = fqn
        try:
            while True:
                (f, mod, name) = self.resolve_to_file(name)
                if not name:
                    # Direct module reference
                    return mod
                if mod not in self._name_cache:
                    self._name_cache[mod] = get_imports(f)
                try:
                    real_fqn, mod2, remainder = _match_longest_dotted(
                        self._name_cache[mod], name
                    )
                except NoMatch:
                    # Welp, maybe it doesn't exist, but it at least should
                    return f"{mod}.{name}"
                if remainder:
                    name = f"{real_fqn}.{remainder}"
                else:
                    name = real_fqn
        except NoMatch:
            pass

        return name

    def resolve_to_file(self, fqn: str) -> tuple[Path, str, str]:
        project_path, key, remainder = _match_longest_dotted(self.names_to_paths, fqn)
        if project_path.suffix == ".py":
            return (project_path, key, remainder)

        for modname, varname in _dot_positions(remainder):
            if modname:
                tmp = project_path / modname.replace(".", "/")
            else:
                tmp = project_path

            candidate_module_path = tmp.with_suffix(".py")
            candidate_package_path = tmp / "__init__.py"
            # TODO some sort of sentinel when it's a .pyc or __pycache__ entry without a corresponding .py
            # TODO some sort of sentinel if it looks like a native lib
            if candidate_module_path.exists():
                return (candidate_module_path, join(key, modname), varname)
            elif candidate_package_path.exists():
                return (candidate_package_path, join(key, modname), varname)

        raise NoMatch


def _dot_positions(fqn: str) -> Generator[tuple[str, str], None, None]:
    if not fqn:
        yield ("", "")
        return

    # Try various dot positions from the right
    pos = len(fqn)
    yield (fqn, "")
    while (pos := fqn.rfind(".", 0, pos)) != -1:
        yield (fqn[:pos], fqn[pos + 1 :])
    yield ("", fqn)


class NoMatch(Exception):
    pass


def _match_longest_dotted(d: dict[str, T], k: str) -> tuple[T, str, str]:
    for a, b in _dot_positions(k):
        if a in d:
            return (d[a], a, b)
    raise NoMatch


def join(a: Optional[T], b: Optional[T]) -> T:
    if a and b:
        return cast(T, f"{a}.{b}")
    elif a:
        return a
    elif b:
        return b
    else:
        raise Exception
