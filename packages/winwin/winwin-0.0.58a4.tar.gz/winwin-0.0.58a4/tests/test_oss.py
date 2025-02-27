from os import environ as env

from winwin.oss import OssFs


def test_oss():
    fs = OssFs(
        access_id=env["OSS_ACCESS_KEY_ID"],
        access_key=env["OSS_ACCESS_KEY_SECRET"],
        endpoint=env["OSS_ENDPOINT"],
        bucket=env["OSS_BUCKET"],
    )
    assert fs.endpoint == "https://oss-cn-hangzhou.aliyuncs.com"
    assert fs.external_endpoint == "https://oss-cn-hangzhou.aliyuncs.com"

    fs.write("test/test.txt", "hello world")
    assert fs.bucket.get_object("test/test.txt").read() == b"hello world"
