from static_qualname.core import get_imports


def test_no_imports(tmp_path):
    f = tmp_path / "foo.py"
    f.write_text("")
    assert get_imports(f) == {}


def test_normal_import(tmp_path):
    f = tmp_path / "foo.py"
    f.write_text("import a\nimport b.c\n")
    assert get_imports(f) == {"a": "a", "b.c": "b.c"}


def test_as_import(tmp_path):
    f = tmp_path / "foo.py"
    f.write_text("from a import b as c\n")
    assert get_imports(f) == {"c": "a.b"}


def test_mixed_imports_last_one_wins(tmp_path):
    f = tmp_path / "foo.py"
    f.write_text("import a\nfrom foo.bar import a\n")
    assert get_imports(f) == {"a": "foo.bar.a"}
    f.write_text("from foo.bar import a\nimport a\n")
    assert get_imports(f) == {"a": "a"}
