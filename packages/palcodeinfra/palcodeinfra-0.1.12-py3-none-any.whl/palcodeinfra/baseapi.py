import logging.config
from fastapi import FastAPI
from palcodeinfra.tenantidmiddleware import TenantIdMiddleware
from asgi_correlation_id import CorrelationIdMiddleware, CorrelationIdFilter
import logging
from fastapi.middleware.cors import CORSMiddleware
from asgi_correlation_id.log_filters import CorrelationIdFilter
from palcodeinfra.tokenmiddleware import TokenMiddleware
from palcodeinfra.useridmiddleware import UserIdMiddleware
from palcodeinfra.requestloggermiddleware import RequestLoggerMiddleware
from palcodeinfra.requestidmiddleware import RequestIdMiddleware

class BaseAPI():
    _instance = None
    api = None
    logger = None

    def __init__(self):
        raise RuntimeError('Call instance() method instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)     
            cls._instance.configure()
        return cls._instance.api
    
    @classmethod
    def logger(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)     
            cls._instance.configure()
        return cls._instance.logger

    def configure(self):
        self.api = FastAPI()
        self.api.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Allows all origins
            allow_credentials=True,
            allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
            allow_headers=["*"],  # Allows all headers
        )
        self.api.add_middleware(RequestIdMiddleware)
        self.api.add_middleware(RequestLoggerMiddleware)
        self.api.add_middleware(TokenMiddleware)
        self.api.add_middleware(UserIdMiddleware)
        self.api.add_middleware(TenantIdMiddleware)
        #self.api.add_middleware(CorrelationIdMiddleware, header_name = 'X-Correlation-ID', update_request_header = True)
        
        #self.configure_advanced_logging()
        self.configure_logging()
        self.logger = logging.getLogger(__name__)

    def configure_logging(self):
        cid_filter = CorrelationIdFilter(uuid_length=32)
        console_handler = logging.StreamHandler()
        console_handler.addFilter(cid_filter)
        logging.basicConfig(
            handlers=[console_handler],
            level=logging.DEBUG,
            format='%(levelname)s: \t  %(asctime)s %(name)s:%(lineno)d [%(correlation_id)s] %(message)s'
        )

    def configure_advanced_logging(self):
        # LOGGING = {
        #             'version': 1,
        #             'disable_existing_loggers': False,
        #             'filters': {
        #                 'correlation_id': {'()': CorrelationIdFilter(uuid_length=32)},
        #             },
        #             'formatters': {
        #                 'web': {
        #                     'class': 'logging.Formatter',
        #                     'datefmt': '%H:%M:%S',
        #                     'format': '%(levelname)s ... [%(correlation_id)s] %(name)s %(message)s',
        #                 },
        #             },
        #             'handlers': {
        #                 'web': {
        #                     'class': 'logging.StreamHandler',
        #                     'filters': ['correlation_id'],
        #                     'formatter': 'web',
        #                 },
        #             },
        #             'loggers': {
        #                 'my_project': {
        #                     'handlers': ['web'],
        #                     'level': 'DEBUG',
        #                     'propagate': True,
        #                 },
        #             },
        #         }
        
        LOGGING = {
            'version': 1,
                'disable_existing_loggers': False,
                'filters': {  # correlation ID filter must be added here to make the %(correlation_id)s formatter work
                    'correlation_id': {
                        '()': 'asgi_correlation_id.CorrelationIdFilter',
                        'uuid_length': 32,
                        'default_value': '-',
                    },
                },
                'formatters': {
                    'console': {
                        'class': 'logging.Formatter',
                        'datefmt': '%H:%M:%S',
                        # formatter decides how our console logs look, and what info is included.
                        # adding %(correlation_id)s to this format is what make correlation IDs appear in our logs
                        'format': '%(levelname)s:\t\b%(asctime)s %(name)s:%(lineno)d [%(correlation_id)s] %(message)s',
                    },
                },
                'handlers': {
                    'console': {
                        'class': 'logging.StreamHandler',
                        # Filter must be declared in the handler, otherwise it won't be included
                        'filters': ['correlation_id'],
                        'formatter': 'console',
                    },
                },
                # Loggers can be specified to set the log-level to log, and which handlers to use
                'loggers': {
                    # project logger
                    'app': {'handlers': ['console'], 'level': 'INFO', 'propagate': True},
                    # third-party package loggers
                    'databases': {'handlers': ['console'], 'level': 'INFO'},
                    'httpx': {'handlers': ['console'], 'level': 'INFO'},
                    'asgi_correlation_id': {'handlers': ['console'], 'level': 'INFO'},
                }
        }
        
        logging.config.dictConfig(LOGGING)
