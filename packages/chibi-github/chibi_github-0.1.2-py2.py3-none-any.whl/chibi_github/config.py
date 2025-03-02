from chibi.config import configuration

if not configuration.github.host:
    configuration.github.host = 'api.github.com'
if not configuration.github.schema:
    configuration.github.schema = 'https'
