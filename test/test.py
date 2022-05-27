import base64
from requests_toolbelt.multipart.encoder import MultipartEncoder
from uuid import UUID
from time import time
import requests
from src.config.url import test_depth_map_url
import pytest
from dotenv import load_dotenv


load_dotenv()

file = "testing.jpg"
multipart_data = MultipartEncoder(
    fields={
        "frames": ("testing.jpg", open("testing.jpg", "rb")),
    }
)


test_base_url = test_depth_map_url + "/depth-map/"


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


@pytest.fixture()
def response():
    response = requests.post(test_base_url)
    yield response


@pytest.fixture()
def jobid():
    response = requests.post(test_base_url)
    yield response.json()["data"]["token"]


class TestDepthMapApi:

    jobid = ""

    def test_post(self, response):
        response_body_test_post = response.json()
        token_decoded_ascii = base64.b64decode(response_body_test_post["data"]["token"]).decode("ascii")
        timestamp = token_decoded_ascii.split(":")[1]
        token = token_decoded_ascii.split(":")[0]
        assert response.status_code == 201
        assert response_body_test_post["meta"]["_next"]["method"] == "PUT"
        assert is_valid_uuid(token, 4) is True
        assert (int(timestamp) / 1000 + int(43200)) < time() + 43200
        assert (
            response_body_test_post["meta"]["_next"]["link"].split("/")[-1] == response_body_test_post["data"]["token"]
        )

    def test_put_status(self, jobid):
        url = test_base_url + jobid
        response = requests.put(url, files=[("frames", ("testing.jpg", open(file, "rb"), "image/jpeg"))], headers={})
        response_body_test_put = response.json()
        token_decoded_ascii = base64.b64decode(response_body_test_put["data"]["jobId"]).decode("ascii")
        timestamp = token_decoded_ascii.split(":")[1]
        token = token_decoded_ascii.split(":")[0]
        assert response.status_code == 200
        assert response_body_test_put["meta"]["_next"]["method"] == "GET"
        assert is_valid_uuid(token, 4) is True
        assert (int(timestamp) / 1000 + int(43200)) < time() + 43200
        assert response_body_test_put["meta"]["_next"]["link"] == url + "/status"

    def test_get_status(self, jobid):
        url = test_base_url + jobid + "/status"
        response = requests.get(url)
        response_body_test_get = response.json()
        assert response.status_code == 200
        assert type(response_body_test_get["meta"]["count"]) == int
        assert type(response_body_test_get["meta"]["originalFilesCount"]) == int
        assert type(response_body_test_get["meta"]["percentDone"]) == int
        assert type(response_body_test_get["data"]) == dict
