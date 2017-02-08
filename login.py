import os

client_id = os.environ['FB_ID']
client_secret = os.environ['FB_SECRET']
redirect_uri = 'http://localhost:5000/process_login'
token_url = 'https://graph.facebook.com/oauth/access_token'

from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
authorization_base_url = 'https://www.facebook.com/dialog/oauth'
facebook = OAuth2Session(client_id, redirect_uri=redirect_uri)
facebook = facebook_compliance_fix(facebook)


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask import Flask, render_template, request, jsonify, session, abort
from flask_assets import Environment
from jinja2 import StrictUndefined

app = Flask(__name__)

assets = Environment(app)

app.jinja_env.undefined = StrictUndefined
assets.url = app.static_url_path
app.config['ASSETS_DEBUG'] = True


def save_created_state(state):
    pass
def is_valid_state(state):
    return True

# Basic Routes *********************************

@app.route('/')
def index_page():
    """Show index page."""

    return render_template("base.html")

@app.route('/login')
def login_page():
    """Show index page."""

    authorization_url, state = facebook.authorization_url(authorization_base_url)
    print 'Please go here and authorize,', authorization_url

    return authorization_url


@app.route('/process_login')
def process_login():

    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        # Uh-oh, this request wasn't started by us!
        abort(403)
    code = request.args.get('code')
    print 20 * '*'
    print code
    # We'll change this next line in just a moment

    facebook.fetch_token(token_url, client_secret=client_secret,
                         authorization_response=code)

    r = facebook.get('https://graph.facebook.com/me?')
    return r.content


if __name__ == "__main__":
    pass
    # app.run(host="0.0.0.0", port=5000, debug=True)
