# Copyright (C) 2023-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import ssl
from typing import Callable
from typing import Mapping
from typing import NotRequired
from typing import TypedDict

import httpx
from httpx import AsyncBaseTransport
from httpx._client import EventHook
from httpx._config import Limits
from httpx._types import AuthTypes
from httpx._types import CertTypes
from httpx._types import CookieTypes
from httpx._types import HeaderTypes
from httpx._types import ProxyTypes
from httpx._types import QueryParamTypes
from httpx._types import TimeoutTypes


class AsyncClientParams(TypedDict):
    auth: NotRequired[AuthTypes | None]
    params: NotRequired[QueryParamTypes | None]
    headers: NotRequired[HeaderTypes | None]
    cookies: NotRequired[CookieTypes | None]
    verify: NotRequired[ssl.SSLContext | str | bool]
    cert: NotRequired[CertTypes | None]
    http1: NotRequired[bool]
    http2: NotRequired[bool]
    proxy: NotRequired[ProxyTypes | None]
    mounts: NotRequired[
        Mapping[str, NotRequired[AsyncBaseTransport]] | None
    ]
    timeout: NotRequired[TimeoutTypes]
    follow_redirects: NotRequired[bool]
    limits: NotRequired[Limits]
    max_redirects: NotRequired[int]
    event_hooks: NotRequired[Mapping[str, list[EventHook]] | None]
    base_url: NotRequired[httpx.URL | str]
    transport: NotRequired[AsyncBaseTransport]
    trust_env: NotRequired[bool]
    default_encoding: NotRequired[str | Callable[[bytes], str]]