from app.main import main
from app.main.schema import RegisterUrlSchema, ShortLinkSchema
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
    try:
        short_link = ShortLink.objects.get(slug=slug)
        short_link.access_counter += 1
        short_link.save()
        return jsonify(dict(original_url=short_link.original_url))
    except DoesNotExist as e:
        log.error(e)
        raise NotFound()
    except MultipleObjectsReturned as e:
        log.error(e)
        raise InternalServerError()


@main.route('/url_info/<slug>', methods=['GET'])
@login_required
def get_url_info(slug):
    try:
        short_link = ShortLink.objects.get(slug=slug)
        if short_link.user_id != str(current_user.id):
            raise Unauthorized()
        return jsonify(ShortLinkSchema(exclude=('slug',)).dump(short_link).data)
    except DoesNotExist as e:
        log.error(e)
        raise NotFound()
    except MultipleObjectsReturned as e:
        log.error(e)
        raise InternalServerError()


@main.route('/list_urls', methods=['GET'])
@login_required
def get_list_of_user_urls():
    short_links = ShortLink.objects(user_id=str(current_user.id))
    return jsonify({'URLs': ShortLinkSchema(many=True).dump(short_links).data})
