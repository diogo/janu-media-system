from flask import Response

_401 = Response('', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
_200 = Response('', 200, {'Status': 'Status: 200 OK'})