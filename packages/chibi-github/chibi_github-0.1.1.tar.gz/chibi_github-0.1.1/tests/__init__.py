# -*- coding: utf-8 -*-
from chibi.config import configuration


configuration.loggers[ 'vcr.cassette' ].level = 'WARNING'
configuration.loggers[ 'vcr.stubs' ].level = 'WARNING'
configuration.loggers[ 'chibi_requests.chibi_url' ].level = 'WARNING'
