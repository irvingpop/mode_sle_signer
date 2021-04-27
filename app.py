#!env python3

from flask import Flask, request, redirect
from hashlib import md5, sha256
import hmac
import base64
import time
import os

if 'MODE_ACCESS_KEY' in os.environ and 'MODE_ACCESS_SECRET' in os.environ and 'MODE_TEAM' in os.environ:
    mode_access_key = os.getenv('MODE_ACCESS_KEY')
    mode_access_secret = os.getenv('MODE_ACCESS_SECRET')
    mode_team = os.getenv('MODE_TEAM')
else:
    print("The following environment variables must be present: MODE_ACCESS_KEY, MODE_ACCESS_SECRET and MODE_TEAM")
    exit(1)

app = Flask(__name__)


@app.route('/account_report')
def sign_account_report_url():
    # Generating the embed URL
    mode_report_id = '3a56c4ec192c'
    param1_name = 'param_account_id'
    param1_value = request.args.get('account_id') or '0011N00001g3ns7QAA'
    timestamp = str(int(time.time()))
    url = f"https://app.mode.com/{mode_team}/reports/{mode_report_id}/embed?access_key={mode_access_key}&{param1_name}={param1_value}&run=now&timestamp={timestamp}"

    # Generate the digest of an empty content body, cause who knows :shrug:
    request_type = 'GET'
    content_type = ''
    content_body = str('').encode('utf-8')
    content_hash = md5(content_body).digest()
    content_digest = base64.encodebytes(content_hash).strip()

    # signature fodder
    request_string = ','.join(
        [request_type, content_type, str(content_digest), url, timestamp])
    signature = hmac.new(bytes(mode_access_secret, 'utf-8'),
                         bytes(request_string, 'utf-8'), digestmod=sha256).hexdigest()

    signed_url = '%s&signature=%s' % (url, signature)
    # # return the signed URL as an iframe
    # return f"""
    # <iframe src='{signed_url}' width='100%' height='100%' frameborder='0' </iframe>
    # """

    # return the signed URL as a redirect
    return redirect(signed_url, code=302)


@app.route('/status')
def status():
    return 'Success'


if __name__ == "__main__":
    listen_port = 8080
    if 'PORT' in os.environ:
        listen_port = int(os.getenv('PORT'))
    app.run(host='0.0.0.0', port=listen_port)
