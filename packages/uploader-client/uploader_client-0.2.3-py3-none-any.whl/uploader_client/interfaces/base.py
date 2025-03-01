from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    TYPE_CHECKING,
)


if TYPE_CHECKING:
    from uploader_client.configurations import (
        Config,
    )
    from uploader_client.logging.base import (
        AbstractLogger,
    )


class AbstractInterface(ABC):

    _config: 'Config'
    _logger: 'AbstractLogger'

    def __init__(
        self, config: 'Config', logger: 'AbstractLogger'
    ):
        self._config = config
        self._logger = logger

    @abstractmethod
    def send(self, request):
        """Отправляет запрос, и возвращает результат отправки запроса."""
