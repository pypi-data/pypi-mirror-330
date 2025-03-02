from chibi_requests import Response
from .serializers import Get_base as Get_serializer


class Get( Response ):
    serializer = Get_serializer


class Create( Get ):
    @property
    def ok( self ):
        return self.status_code == 201


class Delete( Get ):
    @property
    def ok( self ):
        return self.status_code == 204
