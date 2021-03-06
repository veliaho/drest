#  -*- coding: utf-8 -*-
# resources.py ---
#
# Created: Wed Dec 14 23:04:38 2011 (+0200)
# Author: Janne Kuuskeri
#


from decimal import Decimal

from django import forms

from drest.resource import Resource
from drest.http import Response
from drest.auth import HttpBasic
from drest.perm.acl import PermissionController


class MyPermResource(Resource):
    """ Access controlled resource """

    access_controller = PermissionController()
    allow_empty_data = True
    authentication = HttpBasic()

    def get(self, request, *args, **kw):
        return 'Hello, GET Perm!'

    def put(self, data, request, *args, **kw):
        return 'Hello, PUT Perm!'

    def delete(self, request, *args, **kw):
        return 'Hello, DELETE Perm!'


class MyAuthResource(Resource):
    """ HTTP Basic authentication """

    authentication = HttpBasic()

    def _allow_anonymous(self, request):
        return False

    def get(self, request, *args, **kw):
        return 'Hello, Auth!'

class MyAnonResource(Resource):
    """ Anonymous resource """

    authentication = HttpBasic()

    def get(self, request, *args, **kw):
        return 'Hello, anonymous Auth!'


class MyRespResource(Resource):
    """ Use drest Response """

    def get(self, request, *args, **kw):
        return Response(200, {'jedi': 'luke'})


class MyMapperResource(Resource):
    """ Define a custom datamapper """

    from drest.datamapper import DataMapper
    class ReverseMapper(DataMapper):
        def _parse_data(self, data, charset):
            return data[::-1]

        def _format_data(self, data, charset):
            return data[::-1] if data is not None else ''

    mapper = ReverseMapper()

    def get(self, request, *args, **kw):
        return 'hello, mapper'

    def put(self, data, *args, **kw):
        self.last_data = data
        return None


class MyDictResource(Resource):
    """
    Return and accept dictionaries.

    curl http://localhost:8000/simple/mapper/dict/?format=json -d '{"a": 1}' -X PUT --header "Content-Type: application/json"
    """

    def put(self, data, request, *args, **kw):
        self.mydata = data

    def get(self, request, *args, **kw):
        return {'a': 3.99, 'b': Decimal('3.99')}


class MyDecimalResource(Resource):
    """
    Return and accept decimal numbers.
    """

    def put(self, data, request, *args, **kw):
        self.mydata = data

    def get(self, request, *args, **kw):
        return {'a': 3.99, 'b': Decimal('3.99')}


class MyNoneResource(Resource):
    """ Return None """

    def get(self, request, *args, **kw):
        return None

class MyTextResource(Resource):
    """ Return plaintext """

    def get(self, request, *args, **kw):
        return 'hello text'


class MyScandicResource(Resource):
    from drest.datamapper import DataMapper

    class AsciiMapper(DataMapper):
        charset='ascii'

    mapper = AsciiMapper()

    def get(self, request):
        return 'häätö'


class MyScandicJsonResource(Resource):
    from drest.datamapper import JsonMapper

    class JsonAsciiMapper(JsonMapper):
        charset='ascii'

    mapper = JsonAsciiMapper()

    def get(self, request):
        return {'key': 'häätö'}


class MyValidationResource(Resource):
    """ Define representation for validtiaon """

    class Representation(forms.Form):
        name = forms.CharField(max_length=5)

    representation = Representation

    def put(self, data, request):
        pass

    def get(self, request, *args, **kw):
        status = request.GET.get('status', None)
        if status == 'good':
            return {'name': 'Luke'}
        elif status == 'goodlist':
            return [
                {'name': 'Luke'},
                ]
        elif status == 'badlist':
            return [
                {'name': 'Luke Skywalker'},
                ]
        elif status == 'none':
            return None
        else:
            return {'name': 'Luke Skywalker'}


class MyDefaultMapperResourceTxt(Resource):
    """ Define default mapper. """

    default_mapper = 'json'

    def get(self, request):
        return {'key': 'löyhkä'}


class MyDefaultMapperResourceObj(Resource):
    """ Define default mapper. """
    from drest.datamapper import JsonMapper

    default_mapper = JsonMapper()

    def get(self, request):
        return {'key': 'löyhkä'}


#
# resources.py ends here
