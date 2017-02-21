from flask import current_app, url_for, request, redirect
from rauth import OAuth2Service


class FacebookSignIn:
    def __init__(self):
        self.provider_name = 'facebook'
        credentials = current_app.config['OAUTH_CREDENTIALS'][self.provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=url_for('auth.oauth_callback', _external=True)
        ))

    def callback(self):
        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={
                'code': request.args['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': url_for('auth.oauth_callback', _external=True)
            }
        )
        me = oauth_session.get('me?fields=id,email').json()
        return (
            'facebook$' + me['id'],
            me.get('email').split('@')[0],  # Facebook does not provide username, so the email's user is used instead
            me.get('email')
        )
