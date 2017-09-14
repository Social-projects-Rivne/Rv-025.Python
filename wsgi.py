import backend.restaurant.wsgi as _my_example_1_wsgi
import client.run as _my_example_2_wsgi


def application(environ, start_response):

    pathinfo = environ.get('PATH_INFO', '')
    selected_application = _my_example_2_wsgi.application
    # start_response('200 OK', [('Content-Type', 'text/html')])
    print "\tGet Pathinfo: %s !!!\n" % pathinfo

    if pathinfo == "/admin":
        selected_application = _my_example_1_wsgi.application
    else:
        selected_application = _my_example_2_wsgi.app

    return selected_application(environ, start_response)
