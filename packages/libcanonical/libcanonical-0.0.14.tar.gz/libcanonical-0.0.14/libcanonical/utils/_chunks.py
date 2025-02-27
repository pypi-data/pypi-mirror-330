# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Sequence
from typing import Generator
from typing import TypeVar

T = TypeVar('T')


def chunks(iterable: Sequence[T], n: int = 1) -> Generator[list[T], None, None]:
    l = len(iterable)
    for ndx in range(0, l, n):
        yield list(iterable[ndx:min(ndx + n, l)])