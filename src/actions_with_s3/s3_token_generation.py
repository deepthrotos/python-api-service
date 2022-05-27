from uuid import uuid4
from base64 import b64encode
from time import time


def generate_token():
    token = b64encode(bytes(str(uuid4()) + ":" + str(time()).split(".")[0] + "000", encoding="utf8")).decode("ascii")
    return token
