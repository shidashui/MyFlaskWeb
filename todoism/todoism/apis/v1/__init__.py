from flask import Blueprint
from flask_cors import CORS

api_v1 = Blueprint('api_v1', __name__)


CORS(api_v1)


from todoism.apis.v1 import resources  #避免循环依赖