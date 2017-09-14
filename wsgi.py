import restaurant.wsgi as _backend_wsgi
import run as _client_wsgi


def application(environ, start_response):

    pathinfo = environ.get('PATH_INFO', '')
    print pathinfo

    if pathinfo == "/admin":
        selected_application = _backend_wsgi.application
    else:
        selected_application = _client_wsgi.app

    return selected_application(environ, start_response)
