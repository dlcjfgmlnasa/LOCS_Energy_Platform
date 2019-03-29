# -*- coding:utf-8 -*-
from flask import Blueprint

blueprint = Blueprint('public', __name__)


@blueprint.route('/')
def test():
    return 'blueprint test'
