"""Test helper: run the client surface against a test connection."""

import threading
import urllib.error
import urllib.request
from contextlib import contextmanager

from app import server


@contextmanager
def client_surface(conn, storage_dir):
    httpd = server.make_server(conn, storage_dir)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield server.base_url(httpd)
    finally:
        httpd.shutdown()
        httpd.server_close()


def get(url):
    with urllib.request.urlopen(url, timeout=10) as resp:
        return resp.status, resp.read().decode("utf-8")


def post_form(url, data):
    import urllib.parse
    body = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, resp.read().decode("utf-8")


def post_multipart(url, fields, filename, content):
    boundary = "----caseworkboundary"
    lines = []
    for name, value in fields.items():
        lines += [f"--{boundary}",
                  f'Content-Disposition: form-data; name="{name}"', "",
                  value]
    lines += [f"--{boundary}",
              f'Content-Disposition: form-data; name="file";'
              f' filename="{filename}"',
              "Content-Type: application/octet-stream", ""]
    head = ("\r\n".join(lines) + "\r\n").encode("utf-8")
    tail = f"\r\n--{boundary}--\r\n".encode("utf-8")
    body = head + content + tail
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type",
                   f"multipart/form-data; boundary={boundary}")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, resp.read().decode("utf-8")


def expect_error(fn, *args):
    try:
        fn(*args)
        return None
    except urllib.error.HTTPError as e:
        return e.code
