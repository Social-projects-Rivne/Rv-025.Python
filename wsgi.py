# from backend/restaurant import wsgi as _my_example_1_wsgi
# import my_example_2_wsgi as _my_example_2_wsgi


def application(environ, start_response):
    host = environ.get('HTTP_HOST')
    pathinfo = environ.get('PATH_INFO', '')
    uri = environ.get('REQUEST_URI')
    start_response('200 OK', [('Content-Type', 'text/html')])
    print "host: %s, uri: %s, pathinfo: %s" % (host, uri, pathinfo)
    return client.run(environ, start_response)
