import pytest

from static_qualname.core import Env


@pytest.mark.parametrize(
    "sample",
    (
        # Module
        "foo",
        "foo.floof",
        # Package
        "bar",
        "bar.baz",
        "bar.baz.floof",
        "bar.floof",
        # Entirely missing
        "floof",
        "floof.dog",
    ),
)
def test_direct_reference(sample, tmp_path):
    foo = tmp_path / "foo.py"
    foo.touch()
    (tmp_path / "bar").mkdir()
    bar = tmp_path / "bar" / "__init__.py"
    bar.touch()
    baz = tmp_path / "bar" / "baz.py"
    baz.touch()

    e = Env()
    e.add_site_packages(tmp_path)
    assert e.real_qualname(sample) == sample


def test_indirect_reference(tmp_path):
    foo = tmp_path / "foo.py"
    foo.write_text("from bar import t\n")
    bar = tmp_path / "bar.py"
    bar.write_text("from sys import argv as t")
    e = Env()
    e.add_site_packages(tmp_path)
    print(e.names_to_paths)
    assert e.real_qualname("bar.x") == "bar.x"
    assert e.real_qualname("bar.t") == "sys.argv"
    assert e.real_qualname("foo.t") == "sys.argv"
