from data_aggregator_sdk.integration_message import IntegrationV0MessageGateway
from ul_unipipeline.modules.uni import Uni

from data_logger_sdk.constants import (
    BS_DATA_LOGGER_INPUT_WORKER_NAME,
    DATA_LOGGER_INPUT_WORKER_NAME,
    UNIVERSAL_API_DATA_LOGGER_INPUT_WORKER_NAME,
)
from data_logger_sdk.data_logger_sdk_config import DataLoggerSdkConfig
from data_logger_sdk.lib import CONFIG_FILE
from data_logger_sdk.messages.bs_data_logger_input_message import BsDataLoggerInputV0Message
from data_logger_sdk.messages.universal_api_data_logger_input_message import UniversalApiDataLoggerInputV0Message
from data_logger_sdk.runtime_conf import set_broker_uri


class DataLoggerSdk:

    def __init__(self, config: DataLoggerSdkConfig) -> None:
        self._config = config
        self._uni = Uni(str(CONFIG_FILE))
        set_broker_uri(self._config.broker_url)

    def init_data_logger_input_worker(self) -> None:
        self._uni.init_producer_worker(DATA_LOGGER_INPUT_WORKER_NAME)
        self._uni.initialize()

    def init_bs_data_logger_input_worker(self) -> None:
        self._uni.init_producer_worker(BS_DATA_LOGGER_INPUT_WORKER_NAME)
        self._uni.initialize()

    def init_universal_api_data_logger_input_worker(self) -> None:
        self._uni.init_producer_worker(UNIVERSAL_API_DATA_LOGGER_INPUT_WORKER_NAME)
        self._uni.initialize()

    def send_msg_to_data_logger_input(self, message: IntegrationV0MessageGateway) -> None:
        self._uni.send_to(DATA_LOGGER_INPUT_WORKER_NAME, message)

    def send_msg_to_bs_data_logger_input(self, message: BsDataLoggerInputV0Message) -> None:
        self._uni.send_to(BS_DATA_LOGGER_INPUT_WORKER_NAME, message)

    def send_msg_to_universal_api_data_logger_input(self, message: UniversalApiDataLoggerInputV0Message) -> None:
        self._uni.send_to(UNIVERSAL_API_DATA_LOGGER_INPUT_WORKER_NAME, message)
