from app import lm
from app.auth import auth
from app.models import User
from flask import flash, url_for
from flask import logging
from flask.ext.login import current_user, login_user
from flask.ext.login import logout_user
from utils.oauth import FacebookSignIn
from werkzeug.utils import redirect


log = logging.getLogger(__name__)


@lm.user_loader
def load_user(id):
    return User.objects(id=id)[0]


@auth.route('/oauth/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/oauth/authorize')
def oauth_authorize():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    oauth = FacebookSignIn()
    return oauth.authorize()


@auth.route('/oauth/callback')
def oauth_callback():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    oauth = FacebookSignIn()
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('main.index'))
    user = User.objects(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, username=username, email=email)
        user.save()
    login_user(user, True)
    return redirect(url_for('main.index'))
