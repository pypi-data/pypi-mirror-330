# Copyright (C) 2023-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import NotRequired
from typing import TypedDict

from httpx._client import UseClientDefault
from httpx._types import AuthTypes
from httpx._types import CookieTypes
from httpx._types import HeaderTypes
from httpx._types import QueryParamTypes
from httpx._types import RequestExtensions
from httpx._types import RequestContent
from httpx._types import RequestData
from httpx._types import RequestFiles
from httpx._types import TimeoutTypes


class AsyncRequestParams(TypedDict):
    content: NotRequired[RequestContent | None]
    data: NotRequired[RequestData | None]
    files: NotRequired[RequestFiles | None]
    json: NotRequired[Any | None]
    params: NotRequired[QueryParamTypes | None]
    headers: NotRequired[HeaderTypes | None]
    cookies: NotRequired[CookieTypes | None]
    auth: NotRequired[AuthTypes | UseClientDefault | None]
    follow_redirects: NotRequired[bool | UseClientDefault]
    timeout: NotRequired[TimeoutTypes | UseClientDefault]
    extensions: NotRequired[RequestExtensions | None]
