# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import TypedDict


LoggerConfigDict = TypedDict('LoggerConfigDict', {
    'handlers': list[str],
    'level': str,
    'propagate': bool
})


class LoggingConfigDict(TypedDict):
    version: int
    disable_existing_loggers: bool
    loggers: dict[str, LoggerConfigDict]