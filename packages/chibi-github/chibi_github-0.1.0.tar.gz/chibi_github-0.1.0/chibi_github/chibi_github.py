from chibi_github.config import configuration
from chibi_api import Chibi_api
from chibi_api.chibi_api import Chibi_inner_api
from chibi_requests.auth import Token
from chibi_requests import Response
from chibi_requests import Response
from chibi_api.chibi_api import Chibi_inner_api
from .response import Create, Delete, Get


class Github_api_inner( Chibi_inner_api ):
    response = {
        'get': Get,
        'post': Create,
        'delete': Delete,
    }


class Github_api( Chibi_api ):
    schema = 'https'
    host = 'api.github.com'
    inner_api_class = Github_api_inner

    def login( self, token=None ):
        if token is None:
            token = Token( token=configuration.github.personal_token )
        else:
            token = Token( token=token )
        self.API.auth = token

    @property
    def me( self ):
        return self.API.user
