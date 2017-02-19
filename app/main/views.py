from flask import jsonify, request
from flask import logging

from app.main.schema import RegisterUrlSchema
from app.models import ShortLink
from . import main


log = logging.getLogger(__name__)


@main.route('/register_url', methods=['POST'])
def register_url():
    url_data = RegisterUrlSchema().load(request.get_json()).data
    link = ShortLink(**url_data)
    link.save()
    return jsonify(link)
