"""
A simple Flask app to access Knowi using Okta for user registration and login.
"""

from flask import Flask, g, redirect, render_template, url_for
from flask_oidc import OpenIDConnect
from okta import UsersClient
import os
from pathlib import Path

from knowipy import Knowi

DIR = Path(__file__)

knowi = Knowi(flag='sso', customerToken=os.environ.get("KNOWI_CUSTOMER_TOKEN"))
app = Flask(__name__)

app.config.update({
    "SECRET_KEY": "this-feels-secret-enough-right!",
    "OIDC_CLIENT_SECRETS": f"{DIR.parent}/client_secrets.json",
    "OIDC_COOKIE_SECURE": False,
    "OIDC_ID_TOKEN_COOKIE_NAME": "okta-token",
    'OIDC_SCOPES': ["openid", "profile", "email"],
    "OIDC_CALLBACK_ROUTE": "/oidc/callback",
    "DEBUG": False
})

oidc = OpenIDConnect(app)
okta_client = UsersClient("https://dev-755502.okta.com", os.getenv('OKTA_AUTH_TOKEN'))


def authenticateKnowiSession(email):
    """handles user authentication with Knowi"""
    app.logger.info(f'authenticating user: {email}')
    user_token = knowi.sso_createNewUser(email=email, userGroups=["test"], updateUser=True, role="okta-test")['data']

    session_token = knowi.sso_createUserSession(email=email, userToken=user_token)['data']

    app.logger.info(f'userToken: {user_token} and sessionToken: {session_token} retrieved for {email}')

    return session_token


@app.before_request
def before_request():
    """Load a user object using the user Okta ID. This way, the `g.user` object can be used at any point."""
    if oidc.user_loggedin:
        g.user = okta_client.get_user(str(oidc.user_getfield("sub")))
        g.token = authenticateKnowiSession(g.user.profile.email)
    else:
        g.user = None


@app.route("/")
def index():
    """Render the homepage."""
    return render_template("index.html")


@app.route("/dashboard")
@oidc.require_login
def dashboard():
    """Render the dashboard page."""

    return render_template("dashboard.html")


@app.route("/login")
@oidc.require_login
def login():
    """Force the user to login, then redirect them to the dashboard."""
    return redirect(url_for(".index"))


@app.route("/logout")
def logout():
    """Log the user out of their account and terminates session on Knowi and Okta."""
    knowi.sso_logout(sessionToken=g.token)
    oidc.logout()
    return redirect(url_for(".index"))


if __name__ == "__main__":
    app.logger.info('App is up and running...')
    app.run(host='0.0.0.0', port=5000)
