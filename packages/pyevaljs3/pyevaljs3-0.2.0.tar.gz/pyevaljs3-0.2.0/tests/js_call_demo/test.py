import json
import os
import subprocess
import tempfile
import time
import weakref
from _program import NODE_PROGRAM


class JSException(Exception):
    pass


class RunTimeNotFoundException(Exception):
    pass


class RunTime:

    def __init__(self):
        self._node = None
        self._path = None
        self._initialize = False
        self._finalizer = None

    def init(self):
        self._node = subprocess.Popen(
            ['node', self._path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            encoding='utf-8'
        )
        self._finalizer = weakref.finalize(self, self._close)
        self._initialize = True

    def compile(self, source: str):
        fd, path = tempfile.mkstemp(suffix='.js', dir='.')
        with open(fd, 'w', encoding='utf-8') as fp:
            fp.write(NODE_PROGRAM.format(source=source))
        self._path = path

    def call(self, func: str, *args, arg_list: list = None):
        if arg_list is not None:
            args = arg_list
        else:
            args = [arg for arg in args]

        return self._call(func, args)

    def _call(self, func: str, args: list):
        if not self._initialize:
            self.init()

        self._node.stdin.write("{func}.apply(this, {args})".format(func=func, args=args))
        self._node.stdin.flush()
        result = self._get_result()
        if result["exception"]:
            raise JSException(result['exception'])

        return result['result']

    def _get_result(self):
        _result = {'result': None, 'exception': None}
        while True:
            out = self._node.stdout.readline()
            if out[:14] == "[[<<result>>]]":
                result = json.loads(out[14:])
                _result['result'] = result
            elif out[:17] == "[[<<exception>>]]":
                result = json.loads(out[17:])
                _result['exception'] = result
            else:
                continue

            return _result

    def _close(self):
        os.remove(self._path)
        self._node.stdin.close()
        self._node.stdout.close()
        self._node.wait()

    def close(self):
        self._finalizer()


if __name__ == '__main__':
    rt = RunTime()
    payload = {
        "cursor_score": "", "num": 31, "refresh_type": 1, "note_index": 35, "unread_begin_note_id": "",
        "unread_end_note_id": "", "unread_note_count": 0, "category": "homefeed_recommend", "search_key": "",
        "need_num": 6, "image_formats": ["jpg", "webp", "avif"]
    }

    cookie = 'a1=18c0436e5549rvr1aukayp8l2qjpdrh8f3wz3nlc650000328069;web_session=030037a25201ca6f3b3ef31319224af8cd067a;'
    rt.compile(open('../xhs2.js', encoding='utf-8').read())
    start = time.time()
    for _ in range(100):
        res = rt.call('getXS', "/api/sns/web/v1/homefeed", payload, cookie)
        print(res, type(res))
    print(time.time() - start)
    # res = rt.call('f', 2, 0)
    # print(res, type(res))
    rt.close()
