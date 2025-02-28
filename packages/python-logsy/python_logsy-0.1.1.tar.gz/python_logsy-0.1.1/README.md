# python-logsy

A standardised logging configuration I use for a few things.


## Quickstart

1. Install this package with optional extras:
   ```bash
   pip install python-logsy[fluent,sentry]
   ```

1. Import and configure. This package has three logging handlers available
   in the default configuration. All are relatively self-explanatory except
   that the `fluent` handler logs to a Fluentd or Fluent Bit instance and
   requires the `fluent` dependencies to be installed via the optional extras.
   Furthermore, the `file` handler uses `logging.handlers.RotatingFileHandler`.
   Log files will rollover at 100 megabytes when using the `file` handler.
   ```python
   import logging

   import logsy

   config = {
       'loggers': {
           'app': {
               'handlers': ['console', 'fluent', 'file'],
               'level': 'INFO',
               'propagate': True,
           },
       },
   }
   logsy.init(
       config,
       tag='apps.myapp', # Also used as the Fluent tag (routing)
       fluent_host='localhost',
       environment='production',
       release='2.1.1-beta',
   )
   ```

1. A complete example of `init`; including setup for Sentry:
   ```python
   logsy.init(
       config,
       tag='apps.myapp', # Also used as the Fluent tag (routing)
       replace_config=False,
       fluent_host='localhost',
       fluent_port=24224, # default
       async_fluent=True, # default
       environment='debug',
       debug=True, # default is False
       release='2.1.1-beta',
       level=logging.INFO, # default
       sentry_config={
           'dsn': 'fake-dsn-string',
           'traces_sample_rate': 1.0, # default
       },
   )
   ```

1. Log as per usual:
   ```python
   import logging

   logger = logging.getLogger(__name__)
   logger.info('Testing')
   ```

1. If needed, replace the default logging config with your own:
   ```python
   config = {
       'version': 1,
       'disable_existing_loggers': False,
       'formatters': {}, # incomplete
       'handlers': {}, # incomplete
   }
   logsy.init(
       config,
       replace_config=True,
       tag='apps.myapp',
       fluent_host='localhost',
       fluent_port=24224, # default
       environment='debug',
       debug=True, # default is False
       release='2.1.1-beta',
       level=logging.INFO, # default
   )
   ```
