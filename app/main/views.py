import datetime

from app.main import main
from app.main.schema import RegisterUrlSchema
from app.models import ShortLink
from flask import jsonify, request, logging, current_app as app
from flask_login import current_user, login_required
from mongoengine import DoesNotExist, MultipleObjectsReturned
from utils.converters import hex_to_base64
from utils.exceptions import SlugAlreadyExistsException
from werkzeug.exceptions import NotFound, InternalServerError, Unauthorized

log = logging.getLogger(__name__)


@main.route('/')
def index():
    return 'Welcome on url-shortener!'


@main.route('/register_url', methods=['POST'])
@login_required
def register_url():
    """
    :return: Short url which redirects to specified original_url
    """
    url_data = RegisterUrlSchema().load(request.get_json()).data
    url_data['created'] = datetime.datetime.now()
    url_data['user_id'] = str(current_user.id)
    link = ShortLink(**url_data)

    if 'slug' in url_data:
        if ShortLink.objects(slug=link.slug):
            log.error('Slug already exists in database')
            raise SlugAlreadyExistsException()
    else:
        # save to generate objectId
        link.save()
        while ShortLink.objects(slug=hex_to_base64(str(link.id))):
            link.delete()
            link = ShortLink(**url_data)
            link.save()
        link.slug = hex_to_base64(str(link.id))
    link.save()
    short_url = '{}/{}'.format(app.config['URL_PREFIX'], link.slug)
    return jsonify(dict(short_url=short_url))


@main.route('/<slug>', methods=['GET'])
def get_url(slug):
    # TODO: use objects.get() instead
    short_links = ShortLink.objects(slug=slug)
    if len(short_links) >= 2:
        raise InternalServerError()
    if not short_links:
        raise NotFound()
    return jsonify(dict(original_url=short_links[0].original_url))


@main.route('/url_info/<slug>', methods=['GET'])
@login_required
def get_url_info(slug):
    try:
        short_link = ShortLink.objects.get(slug=slug)
        if short_link.user_id != str(current_user.id):
            raise Unauthorized()
        return jsonify({
            'original_url': short_link.original_url,
            'created': short_link.id.generation_time
        })
    except DoesNotExist as e:
        log.error(e)
        raise NotFound()
    except MultipleObjectsReturned as e:
        log.error(e)
        raise InternalServerError()
