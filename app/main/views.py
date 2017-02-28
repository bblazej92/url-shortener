from http.client import CREATED

from app.main import main
from app.main.schema import RegisterUrlSchema, ShortUrlSchema
from app.models import ShortUrl
from flask import jsonify, request, logging, current_app as app
from flask import make_response
from flask import url_for
from flask_login import current_user, login_required
from mongoengine import DoesNotExist, MultipleObjectsReturned
from utils.converters import hex_to_base64
from utils.exceptions import SlugAlreadyExistsException
from werkzeug.exceptions import NotFound, InternalServerError, Unauthorized

log = logging.getLogger(__name__)


@main.route('/')
def index():
    return 'Welcome on url-shortener!'


@main.route('/v1/generate_short_url', methods=['POST'])
@login_required
def register_url():
    """Generate short url for original url given by user using custom slug if specified.

    .. :quickref: ShortUrl; Generate short url

    :reqheader Accept: application/json
    :<json string original_url: url of website to be shorten
    :<json string slug: slug to use in shortened url (optional)
    :resheader Content-Type: application/json
    :>json string short_url: short url which redirects to original url
    :status 201: ShortUrl created
    :status 500: slug already exists in db

    :returns: Short url which redirects to specified original url
    """
    url_data = RegisterUrlSchema().load(request.get_json()).data
    url_data['user_id'] = str(current_user.id)
    url = ShortUrl(**url_data)

    if 'slug' in url_data:
        if ShortUrl.objects(slug=url.slug):
            log.error('Slug already exists in database')
            raise SlugAlreadyExistsException()
    else:
        # save to generate objectId
        url.save()
        while ShortUrl.objects(slug=hex_to_base64(str(url.id))):
            url.delete()
            url = ShortUrl(**url_data)
            url.save()
        url.slug = hex_to_base64(str(url.id))
    url.save()
    short_url = url_for('main.get_url', slug=url.slug, _external=True)
    return make_response(jsonify(dict(short_url=short_url)), CREATED)


@main.route('/<slug>', methods=['GET'])
def get_url(slug):
    """Get url.

    .. :quickref: ShortUrl; Get url

    :returns: Nothing yet
    """
    try:
        short_link = ShortUrl.objects.get(slug=slug)
        short_link.access_counter += 1
        short_link.save()
        return jsonify(dict(original_url=short_link.original_url))
    except DoesNotExist as e:
        log.error(e)
        raise NotFound()
    except MultipleObjectsReturned as e:
        log.error(e)
        raise InternalServerError()


@main.route('/v1/url_info/<slug>', methods=['GET'])
@login_required
def get_url_info(slug):
    try:
        short_link = ShortUrl.objects.get(slug=slug)
        if short_link.user_id != str(current_user.id):
            raise Unauthorized()
        return jsonify(ShortUrlSchema(exclude=('slug',)).dump(short_link).data)
    except DoesNotExist as e:
        log.error(e)
        raise NotFound()
    except MultipleObjectsReturned as e:
        log.error(e)
        raise InternalServerError()


@main.route('/v1/list_urls', methods=['GET'])
@login_required
def get_list_of_user_urls():
    short_links = ShortUrl.objects(user_id=str(current_user.id))
    return jsonify({'URLs': ShortUrlSchema(many=True).dump(short_links).data})
