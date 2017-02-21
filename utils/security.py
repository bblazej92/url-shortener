from urllib.parse import urlparse, urljoin

from flask import request


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():
    target = request.args.get('next')
    if target is None or not is_safe_url(target):
        return None
    return target
