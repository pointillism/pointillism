import logging as log
import requests
from graphviz import Source
from point.theme import theme_inject
from werkzeug.wrappers import Response

class NotFound(Exception):
    pass

class Forbidden(Exception):
    pass

MIME_MAP = {
    'svg': 'svg+xml'
}


def get_mime(format):
    return MIME_MAP.get(format, format)


def url(host, path, **params):
    ps = "&".join([f"{k}={v}" for k, v in params.items()])
    return "{}/{}?{}".format(host, path, ps) 


def cache_control(public=False, headers=None):
    max_age = 0
    audience = 'private'
    if headers is None:
        headers = {}

    if public:
        audience = 'public'
        max_age = 60

    headers['cache-control'] = f'max-age={max_age} {audience}'
    return headers

def render(body, format='png', theme=None, headers=None):
    body = theme_inject(body, theme)
    src = Source(body)

    resp = Response(src.pipe(format=format),
                    mimetype="image/{}".format(get_mime(format)))
    resp.headers = headers
    return resp


# look up this dict method
def get_and_render(host, path, format="png", theme=None, headers={}, **params):
    org, repo, *tail = path
    path = "/".join((org, repo, 'contents', *tail))
    dot_url = url(host, path, **params)
    log.debug(f"GET: {dot_url}")
    log.debug(f'headers: {headers}')
    response = requests.get(dot_url, headers=headers)

    if response.status_code == 200:
        body = response.text
        body = theme_inject(body, theme)
        src = Source(body)
        return src.pipe(format=format)
    elif response.status_code == 401:
        raise Forbidden('Forbidden! http://pointillism.io/github/login')
    else:
        raise IOError("Problem finding: {}".format(dot_url))

