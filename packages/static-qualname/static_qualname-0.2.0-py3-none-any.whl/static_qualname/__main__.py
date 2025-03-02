import sys
import zipfile
from pathlib import Path

from . import Env
from .core import get_imports

if sys.argv[1].endswith(".whl"):
    with zipfile.ZipFile(sys.argv[1]) as z:
        for n in z.namelist():
            if n.endswith(".py"):
                p = zipfile.Path(z, n)
                print(n, get_imports(p))
else:
    e = Env()
    for dir in sys.path:
        p = Path(dir)
        if p.exists():
            e.add_site_packages(p)

    print(e.real_qualname(sys.argv[1]))
