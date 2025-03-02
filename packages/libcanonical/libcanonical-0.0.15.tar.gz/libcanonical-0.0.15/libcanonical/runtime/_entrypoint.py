# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pkg_resources
import warnings
from typing import Any


def get_entrypoints(name: str):
    entrypoints = [
        (entry_point.name, entry_point.load(False))
        for entry_point
        in pkg_resources.iter_entry_points(name)
    ]
    return sorted(entrypoints, key=lambda x: getattr(x[1], 'WEIGHT', 0))


def run_entrypoints(
    name: str,
    fn: str | None = None,
    namespace: str = 'canonical',
    *args: Any,
    **kwargs: Any
) -> None:
    """Runs the entrypoints specified by `name`."""
    for _, entry_point in get_entrypoints(name):
        f = entry_point if not fn else getattr(entry_point, fn, None)
        if not callable(f):
            warnings.warn(
                f"Entrypoint {entry_point} (fn: {fn}) was not callable."
            )
            continue
        f(*args, **kwargs)