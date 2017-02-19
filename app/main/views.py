import random
from flask import jsonify

from app.models import ShortLink
from . import main


@main.route('/')
def hello_world():
    link = ShortLink(slug='test{}'.format(random.randint(1, 1000)), destination_url='http://onet.pl')
    link.save()
    links = ShortLink.objects.all()
    return jsonify(links)
