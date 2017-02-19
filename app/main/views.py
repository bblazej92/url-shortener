from flask import jsonify, request, logging, current_app as app

from app.main.schema import RegisterUrlSchema
from app.models import ShortLink
from utils.converters import hex_to_base64
from . import main


log = logging.getLogger(__name__)


@main.route('/register_url', methods=['POST'])
def register_url():
    """
    :return: Short url which redirects to specified destination_url
    """
    url_data = RegisterUrlSchema().load(request.get_json()).data
    link = ShortLink(**url_data)
    link.save()

    if 'slug' not in url_data:
        link.slug = hex_to_base64(str(link.id))
        link.save()

    short_url = '{}/{}'.format(app.config['URL_PREFIX'], link.slug)
    return jsonify(dict(short_url=short_url))
