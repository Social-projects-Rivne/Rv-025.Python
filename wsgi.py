def application(environ, start_response):
    host = environ.get('HTTP_HOST')
    pathinfo = environ.get('PATH_INFO', '')
    uri = environ.get('REQUEST_URI')
    start_response('200 OK', [('Content-Type', 'text/html')])
    print host, uri, pathinfo
    return client/run.py(environ, start_response)
