# Simple use

```py
>>> from static_qualname import Env
>>> e = Env()
>>> e.add_site_packages(Path("/usr/lib/python3.13"))
>>> e.real_qualname("http.server.HTTPStatus")
"http.HTTPStatus"
```

or

```sh
python -m static_qualname http.server.HTTPStatus
```
