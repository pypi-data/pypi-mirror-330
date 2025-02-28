# Copyright (C) 2023-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import logging
from typing import overload
from typing import Any
from typing import Callable
from typing import Literal
from typing import NotRequired
from typing import TypeAlias
from typing import TypeVar
from typing import Unpack

import httpx

from ._asyncrequestparams import AsyncRequestParams


RequestMethod: TypeAlias = Literal['HEAD', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'TRACE']
T = TypeVar('T')


class DefaultRequestParams(AsyncRequestParams):
    retry_status: NotRequired[set[int] | None]
    model: NotRequired[Callable[[bytes], Any] | None]
    max_attempts: NotRequired[int]
    max_wait: NotRequired[int]
    nullable: NotRequired[bool]
    suppress_exceptions: NotRequired[bool]


class AsyncClient(httpx.AsyncClient):
    logger: logging.Logger = logging.getLogger('canonical.http')

    @property
    def domain(self) -> str:
        return self.base_url.netloc.decode()

    @staticmethod
    def parse_retry_after(response: httpx.Response, max_wait: int = 10) -> int:
        v = response.headers.get('Retry-After')
        if v is None or not str.isdigit(v):
            return max_wait
        return min(int(v), max_wait)

    def can_retry_timeout(self, request: httpx.Request):
        return request.method in {'GET', 'HEAD', 'OPTIONS'}

    @overload
    async def get(
        self,
        url: httpx.URL | str,
        *,
        model: None = ...,
        max_attempts: int | None = ...,
        retry_status: set[int] | None = ...,
        **kwargs: Unpack[AsyncRequestParams]
    ) -> httpx.Response:
        ...

    @overload
    async def get(
        self,
        url: httpx.URL | str,
        *,
        model: Callable[[bytes], T],
        max_attempts: int | None = ...,
        nullable: Literal[False],
        retry_status: set[int] | None = ...,
        **kwargs: Unpack[AsyncRequestParams]
    ) -> T:
        ...

    @overload
    async def get(
        self,
        url: httpx.URL | str,
        *,
        model: Callable[[bytes], T],
        nullable: Literal[True],
        max_attempts: int | None = ...,
        retry_status: set[int] | None = ...,
        **kwargs: Unpack[AsyncRequestParams]
    ) -> T | None:
        ...

    @overload
    async def get(
        self,
        url: httpx.URL | str,
        *,
        suppress_exceptions: bool = True,
        max_attempts: int | None = ...,
        retry_status: set[int] | None = ...,
        **kwargs: Unpack[AsyncRequestParams]
    ) -> tuple[httpx.Response | None, bool, BaseException | None]:
        ...

    async def get( # type: ignore
        self,
        url: httpx.URL | str,
        **kwargs: Unpack[DefaultRequestParams]
    ) -> httpx.Response | object | tuple[httpx.Response | None, bool, BaseException | None]:
        return await self.request('GET', url, **kwargs)

    @overload
    async def request(
        self,
        method: RequestMethod,
        url: httpx.URL | str,
        *,
        model: None = ...,
        **kwargs: Unpack[AsyncRequestParams]
    ) -> httpx.Response:
        ...

    @overload
    async def request(
        self,
        method: RequestMethod,
        url: httpx.URL | str,
        *,
        model: Callable[[bytes], T],
        nullable: Literal[False],
        **kwargs: Unpack[AsyncRequestParams]
    ) -> T:
        ...


    @overload
    async def request(
        self,
        method: RequestMethod,
        url: httpx.URL | str,
        *,
        model: Callable[[bytes], T],
        nullable: Literal[True],
        **kwargs: Unpack[AsyncRequestParams]
    ) -> T | None:
        ...

    @overload
    async def request(
        self,
        method: RequestMethod,
        url: httpx.URL | str,
        *,
        suppress_exceptions: bool = True,
        **kwargs: Unpack[AsyncRequestParams]
    ) -> tuple[httpx.Response | None, bool, BaseException | None]:
        ...

    async def request( # type: ignore
        self,
        method: RequestMethod,
        url: httpx.URL | str,
        *,
        model: Callable[[bytes], T] | None = None,
        max_attempts: int = 0,
        max_wait: int = 30,
        suppress_exceptions: bool = False,
        retry_status: set[int] | None = None,
        nullable: bool = False,
        **kwargs: Unpack[AsyncRequestParams]
    ) -> httpx.Response | T | tuple[httpx.Response | None, bool, BaseException | None] | None:
        if model is not None and suppress_exceptions:
            raise ValueError(
                "The `model` and `suppress_exceptions` parameters are "
                "mutually exclusive."
            )
        retry_status = retry_status or set()
        attempts: int = 0
        delay: int = 5
        exception: BaseException | None = None
        response: httpx.Response | None = None
        must_abort: Callable[[int, int], bool] = lambda m, a: (m > 0) and a > m
        while True:
            attempts += 1
            must_log = (attempts % 3) == 0
            try:
                response = await super().request(method, url, **kwargs)
                response.raise_for_status()
                break
            except httpx.ConnectError as e:
                # We are not able to connect at all. The assumption here is that
                # this is due to (temporary) network issues.
                if must_log:
                    self.logger.warning("Network issues prevent request (url: %s)", e.request.url)
                if must_abort(max_attempts, attempts):
                    exception = e
                    break
                await asyncio.sleep(delay)
                continue
            except httpx.ConnectTimeout as e:
                # A connection timeout may occur due to intermediary issues, or
                # a booting application that has not bound its port yet.
                if must_log:
                    self.logger.warning("Connection timeout (url: %s)", e.request.url)
                if must_abort(max_attempts, attempts):
                    exception = e
                    break
                await asyncio.sleep(delay)
                continue
            except httpx.ReadTimeout as e:
                # A read timeout means that we've succesfully connected, but there
                # was a timeout reading the response. This should only be retried on
                # safe HTTP methods, because we do not know what actually caused the
                # timeout, thus any destructive operations may actually have been
                # completed succesfully.
                self.logger.warning("Caught timeout (url: %s).", e.request.url)
                if not self.can_retry_timeout(e.request) or must_abort(max_attempts, attempts):
                    exception = e
                    break
                await asyncio.sleep(delay)
                continue
            except httpx.HTTPStatusError as e:
                status_code = e.response.status_code
                if status_code != 429 and status_code not in retry_status:
                    response = e.response
                    exception = e
                    break
                if status_code == 429:
                    wait = self.parse_retry_after(e.response, max_wait)
                    if must_log:
                        self.logger.debug(
                            "Request was rate-limited, suspending %ss (url: %s)",
                            wait,
                            e.response.url
                        )
                    await asyncio.sleep(wait)
                    continue

                # In all other cases (ignored status codes) simply
                # wait with the standard delay.
                if must_abort(max_attempts, attempts):
                    exception = e
                    break
                self.logger.debug("Retrying non-2xx failed request (status: %s)", status_code)
                await asyncio.sleep(0.1)
            except httpx.RemoteProtocolError as e:
                # This is an edge condition where we might try to make a
                # request to a server that closed it ports or the remote
                # HTTP server improperly implements the protocol. This
                # request is retried if it is a safe method, else an
                # exception is raised.
                if must_log:
                    self.logger.warning("Remote protocol violation (url: %s)", e.request.url)
                if not self.can_retry_timeout(e.request) or must_abort(max_attempts, attempts):
                    exception = e
                    break
                await asyncio.sleep(delay)
            except Exception as e:
                exception = e
                break

        if exception is not None:
            if not suppress_exceptions:
                if nullable:
                    return None
                raise exception
            return response, False, exception

        assert response is not None

        # Return the correct response based on input parameters.
        if model is not None:
            return model(response.content)

        if suppress_exceptions:
            return response, True, None

        return response