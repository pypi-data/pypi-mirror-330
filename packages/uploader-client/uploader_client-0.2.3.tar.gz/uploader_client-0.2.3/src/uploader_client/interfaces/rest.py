import traceback
from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    IO,
    Any,
    List,
    Optional,
    Tuple,
    Union,
)
from urllib.parse import (
    urljoin,
)

from pydantic.main import (
    BaseModel,
)
from requests.adapters import (
    HTTPAdapter,
    Retry,
)
from requests.exceptions import (
    RequestException,
)
from requests.models import (
    PreparedRequest,
    Request as HttpRequest,
    Response,
)
from requests.sessions import (
    Session,
)
from uploader_client.const import (
    DEFAULT_REQUEST_TIMEOUT,
)
from uploader_client.interfaces.base import (
    AbstractInterface,
)
from uploader_client.logging.base import (
    Entry,
)


class AbstractRESTRequest(ABC):
    """Абстрактный REST-запрос."""


class OpenAPIRequest(AbstractRESTRequest):

    @abstractmethod
    def get_url(self) -> str:
        """URL запроса."""

    @abstractmethod
    def get_method(self) -> str:
        """Метод запроса.

        'get', 'post', 'delete', 'patch', 'put' or 'options'.
        """

    def get_params(self) -> dict:
        """Параметры Query string (get)."""
        return {}

    def get_headers(self) -> dict:
        """Заголовки запроса."""
        return {}

    def get_data(self):
        """Тело запроса."""
        return None

    def get_files(self) -> List[Tuple['str', IO]]:
        """Файлы в запросе.

        (
            ('files', Path(name1).open('rb'),
            ('files', Path(name2).open('rb'),
        )
        """
        return []

    def get_timeout(self) -> Union[int, None]:
        """Таймаут запроса, сек."""
        return None


class Result(BaseModel):

    class Config:
        arbitrary_types_allowed = True

    request: AbstractRESTRequest
    response: Optional[Any] = None
    http_request: Optional[Any] = None
    error: Optional[str] = None
    log: Optional[Any] = None


class OpenAPIInterface(AbstractInterface):
    """Синхронный режим по спецификации OpenAPI.

    Все запросы выполняются в синхронном режиме в соответствии с загруженной спецификацией OpenAPI.
-
    Получение результата осуществляется путем выполнения HTTP-запроса.
    """

    def send(self, request: OpenAPIRequest) -> Result:
        session = Session()

        http_adapter = HTTPAdapter(
            max_retries=Retry(
                total=self._config.request_retries,
                backoff_factor=self._config.retry_factor
            )
        )

        session.mount('https://', http_adapter)
        session.mount('http://', http_adapter)

        args = (
            request.get_method().upper(),
            self._determine_request_url(request)
        )
        kwargs = dict(
            headers=request.get_headers(),
            params=request.get_params(),
            data=request.get_data(),
            files=request.get_files(),
        )

        response = error = stream = verify = cert = None
        proxies = {}

        http_request = self._prepare_http_request(session, *args, **kwargs)

        http_kwargs = dict(
            timeout=self._select_timeout(request)
        )
        http_kwargs.update(session.merge_environment_settings(
            http_request.url, proxies, stream, verify, cert
        ))

        try:
            response = self._send_request(session, http_request, **http_kwargs)
            response.raise_for_status()
        except RequestException as err:
            error = self._format_error(err)

        entry = Entry(
            request=self._format_http_request(http_request),
            response=self._format_response(response),
            error=error,
        )

        log = self._log(entry)

        return Result(
            request=request,
            http_request=http_request,
            response=response,
            error=error,
            log=log,
        )

    def _log(self, entry: Entry):
        result = self._logger.log(entry)

        return result

    def _send_request(
        self, session: Session, http_request: PreparedRequest, **http_kwargs
    ) -> Response:
        return session.send(http_request, **http_kwargs)

    def _determine_request_url(self, request):
        """Определение URL запроса.

        URL = схема + адрес + path запроса.
        """
        return urljoin(
            self._config.url,
            request.get_url(),
        )

    def _select_timeout(self, request):
        """Определение таймаута.

        Приоритет таймаутов:
            - из запроса
            - из настройки клиента
            - стандартный
        """
        return (
            request.get_timeout() or
            self._config.timeout or
            DEFAULT_REQUEST_TIMEOUT
        )

    def _prepare_http_request(
        self, session, *args, **kwargs
    ) -> PreparedRequest:
        return session.prepare_request(HttpRequest(
            *args, **kwargs
        ))

    def _format_http_request(
        self, http_request: PreparedRequest
    ) -> str:
        body = http_request.body if http_request.body else ''
        if isinstance(body, bytes):
            body = body.decode('utf-8')

        return (
            f"[{http_request.method}] {http_request.url}\n\n"
            f"{http_request.headers}\n\n"
            f"{body}"
        )

    def _format_error(self, error: Union[Exception, None]) -> str:
        return f'{str(error)}\n\n{traceback.format_exc()}' if error else ''

    def _format_response(self, response: Union[Response, None]) -> str:
        return f'[{response.status_code}] {response.url}\n\n{response.headers}\n\n{response.text}' if response else ''
