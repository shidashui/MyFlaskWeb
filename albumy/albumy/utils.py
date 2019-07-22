
try:
    from urlparse import urlparse, urljoin
except:
    from urllib.parse import urlparse, urljoin

from flask import request, url_for, redirect, flash


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urlparse(urljoin(request.host_url, target)))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def redirect_back(default='main.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u'Error in the %s field - %s' % (getattr(form, field).label.text, error))