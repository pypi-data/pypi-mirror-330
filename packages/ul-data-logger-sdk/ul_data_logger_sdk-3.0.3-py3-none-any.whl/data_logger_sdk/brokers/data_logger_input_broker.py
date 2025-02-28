from ul_unipipeline.brokers.uni_amqp_py_broker import UniAmqpPyBroker

from data_logger_sdk.runtime_conf import get_broker_uri


class DataLoggerInputBroker(UniAmqpPyBroker):

    @classmethod
    def get_connection_uri(cls) -> str:
        return get_broker_uri()
