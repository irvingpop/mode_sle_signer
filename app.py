#!env python3

from flask import Flask, request, redirect
from hashlib import sha256
import hmac
import base64
import time
import urllib
from opentelemetry import trace

# allow for relative importing if run directly
if __name__ == "__main__":
    from config import secrets, reports, listen_port
else:
    from .config import secrets, reports, listen_port

# Flask initialization
app = Flask(__name__)

# OTel initialization
tracer = trace.get_tracer(__name__)

@app.get('/report/<report>')
@tracer.start_as_current_span("sign_report_url")
def sign_report_url(report):
    # check for a valid token
    with tracer.start_as_current_span("security-validation") as current_span:
        provided_token = request.args.get('token') or 'missing'
        if provided_token != secrets.get('access_token'):
            current_span.set_attribute(
                "app.error", "Missing or incorrent token provided")
            return "Missing or incorrect token provided"

        # lookup report and generate URL from values
        if report in reports:
            this_report = reports.get(report)

            # Generating the embed URL
            mode_report_id = this_report.get('mode_report')
            param_name = this_report.get('param_name')
            param_value = request.args.get(
                'account_id') or this_report.get('param_default_value')
            current_span.set_attribute("params.value", param_value)
            do_iframe = request.args.get('iframe') or False
            current_span.set_attribute("params.do_iframe", do_iframe)
            timestamp = str(int(time.time()))  # current time in unix time

            url = make_url('https://app.mode.com', secrets.get('mode_team'), 'reports',
                           mode_report_id, 'embed', access_key=secrets.get('mode_access_key'),
                           max_age=3600, **{param_name: param_value}, run='now', timestamp=timestamp)
        else:
            return f"Missing report {report}"

    with tracer.start_as_current_span("sign-url") as current_span:
        request_type = 'GET'
        content_type = ''
        # the MD5 digest of an empty content body, always the same, :shrug:
        content_digest = '1B2M2Y8AsgTpgAmY7PhCfg=='

        # signature fodder
        request_string = ','.join(
            [request_type, content_type, str(content_digest), url, timestamp])
        signature = hmac.new(bytes(secrets.get('mode_access_secret'), 'utf-8'),
                             bytes(request_string, 'utf-8'), digestmod=sha256).hexdigest()

        signed_url = '%s&signature=%s' % (url, signature)

        if do_iframe is not False:
            # return the signed URL as an iframe
            return f"""
            <iframe src='{signed_url}' width='100%' height='100%' frameborder='0' </iframe>
            """
        else:
            # return the signed URL as a redirect
            return redirect(signed_url, code=302)


@tracer.start_as_current_span("make_url")
def make_url(base_url, *res, **params):
    url = base_url
    for r in res:
        url = '{}/{}'.format(url, r)
    if params:
        url = '{}?{}'.format(url, urllib.parse.urlencode(params))
    return url


@app.get('/status')
def status():
    return 'Success'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=listen_port)
