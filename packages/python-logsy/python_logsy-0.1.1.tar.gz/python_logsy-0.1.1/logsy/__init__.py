"""
One logging config to rule them all.
"""
import logging
import logging.config
from io import BytesIO
from socket import gethostname
from typing import Union

from fluent_formatter import ISO8601FluentRecordFormatter

__version__ = '0.1.1'
HOSTNAME = gethostname()
USE_FLUENT = False
USE_SENTRY = False

try:
    import msgpack
    from fluent import asynchandler as fluenthandler
except ModuleNotFoundError:
    pass
else:
    USE_FLUENT = True

try:
    import sentry_sdk
except ModuleNotFoundError:
    pass
else:
    USE_SENTRY = True




def overflow_handler(pendings):
    unpacker = msgpack.Unpacker(BytesIO(pendings))
    for unpacked in unpacker:
        print(unpacked)




def configure_logging(
    config: dict,
    tag: str=None,
    fluent_host: str=None,
    fluent_port: bool=24224,
    async_fluent: bool=True,
    environment: str=None,
    debug: bool=False,
    release: str=None,
    level: Union[str, int]=logging.INFO,
    sentry_config: dict=None,
    replace_config: bool=False,
):
    if fluent_port:
        try:
            fluent_port = int(fluent_port)
        except (ValueError, TypeError) as exc:
            raise TypeError('"fluent_port" kwarg must be an integer.')
    if not tag:
        raise ValueError('You must set a value for the "tag" kwarg.')
    if not sentry_config:
        sentry_config = {}
    if isinstance(level, str):
        level = level.upper()

    fluent_handler_class = 'fluent.asynchandler.FluentHandler'
    if not async_fluent:
        fluent_handler_class = 'fluent.handler.FluentHandler'


    #############
    # FORMATTERS
    #############
    fluent_formatter = {
        '()': 'fluent_formatter.ISO8601FluentRecordFormatter',
        'format': {
            'name': '%(name)s',
            'host': '%(hostname)s',
            'hostname': '%(hostname)s',
            'level': '%(levelno)s',
            'level_name': '%(levelname)s',
            'exc_info': '%(exc_text)s',
            'dotpath': '%(module)s.%(funcName)s',
            'pathname': '%(pathname)s',
            'environment': environment or '',
            'timestamp': '%(asctime)s',
            'pid': '%(process)d',
            'process': '%(processName)s',
            'thread_id': '%(thread)d',
            'thread': '%(threadName)s',
            'release_version': release or '',
        },
    }
    simple_formatter = {
        '()': 'logging.Formatter',
        'format': '[{asctime}] {name} | {levelname} | {message}',
        'style': '{',
    }
    formatters = {
        'simple': simple_formatter,
    }


    ###########
    # HANDLERS
    ###########
    fluent_handler = {
        'level': level,
        'class': fluent_handler_class,
        'formatter': 'fluent',
        'tag': tag,
        'host': fluent_host,
        'port': fluent_port,
        'msgpack_kwargs': {'default': str},
        'buffer_overflow_handler': overflow_handler,
    }
    log_filename = f'{tag}__{HOSTNAME}.log'
    file_handler = {
        'class': 'logging.handlers.RotatingFileHandler',
        'formatter': 'simple',
        'filename': log_filename,
        'maxBytes': 100_000_000, # 100 megabytes
        'backupCount': 5, # up to 5 logfiles: "app.log.1" thru "app.log.5"
    }
    console_handler = {
        'class': 'logging.StreamHandler',
        'formatter': 'simple',
    }
    handlers = {
        'console': console_handler,
        'file': file_handler,
    }


    ##################
    # FLUENT-SPECIFIC
    ##################
    if fluent_host and fluent_port and tag and USE_FLUENT:
        formatters['fluent'] = fluent_formatter
        handlers['fluent'] = fluent_handler


    #########
    # CONFIG
    #########
    default_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': formatters,
        'handlers': handlers,
    }
    if replace_config:
        logging.config.dictConfig(config)
    else:
        loggers = config.get('loggers', {})
        # In case the value we get is None
        if not loggers:
            loggers = {}
        default_config['loggers'] = loggers
        logging.config.dictConfig(default_config)


    #########
    # SENTRY
    #########
    if USE_SENTRY and sentry_config:
        dsn = None
        ignore_errors = [KeyboardInterrupt]
        if isinstance(sentry_config, dict):
            dsn = sentry_config.pop('dsn', None)
            traces_sample_rate = sentry_config.pop('traces_sample_rate', 1.0)
        if dsn:
            if release:
                sentry_config['release'] = release
            sentry_sdk.init(
                dsn=dsn,
                # Set traces_sample_rate to 1.0 to capture 100%
                # of transactions for performance monitoring.
                # We recommend adjusting this value in production.
                traces_sample_rate=traces_sample_rate,
                debug=debug,
                environment=environment,
                ignore_errors=ignore_errors,
                **sentry_config,
            )




def init(*args, **kwargs):
    configure_logging(*args, **kwargs)
