from app import lm
from app.auth import auth
from app.models import User
from flask import flash, url_for, logging
from flask.ext.login import current_user, login_user, logout_user
from utils.oauth import FacebookSignIn
from utils.security import get_redirect_target
from werkzeug.utils import redirect


log = logging.getLogger(__name__)


@lm.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()


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
    redirect_target = get_redirect_target()
    return redirect(redirect_target or url_for('main.index'))
