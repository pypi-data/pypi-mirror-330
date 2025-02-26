import json
import time

import pyevaljs3

payload = {
        "cursor_score": "", "num": 31, "refresh_type": 1, "note_index": 35, "unread_begin_note_id": "",
        "unread_end_note_id": "", "unread_note_count": 0, "category": "homefeed_recommend", "search_key": "",
        "need_num": 6, "image_formats": ["jpg", "webp", "avif"]
    }

cookie = 'a1=18c0436e5549rvr1aukayp8l2qjpdrh8f3wz3nlc650000328069;web_session=030037a25201ca6f3b3ef31319224af8cd067a;'

code = open("xhs2.js", encoding="utf-8").read()
code += ';return getXS("/api/sns/web/v1/homefeed", %s, "%s");' % (json.dumps(payload), cookie)
xsxt = pyevaljs3.eval_(code, True)
print(xsxt, type(xsxt))
# s = time.time()
# for _ in range(100):
#     xsxt = pyevaljs3.eval_(code, True)
#     # print(xsxt, type(xsxt))
# print(time.time() - s)
ctx = pyevaljs3.compile_('xhs2.js')
r = ctx.call('getXS', "/api/sns/web/v1/homefeed", payload, cookie)
print(r, type(r))
# s = time.time()
# for _ in range(100):
#     r = ctx.call('getXS', "/api/sns/web/v1/homefeed", payload, cookie)
#     # print(r, type(r))
# print(time.time() - s)
# import execjs
# ctx1 = execjs.compile(code)
# s = time.time()
# for _ in range(100):
#     r = ctx1.call('getXS', "/api/sns/web/v1/homefeed", payload, cookie)
#     # print(r, type(r))
# print(time.time() - s)


if __name__ == '__main__':
    async def main():
        r = await pyevaljs3.async_eval(code, True)
        print(r, type(r))
        r = await ctx.async_call('getXS', "/api/sns/web/v1/homefeed", payload, cookie)
        print(r, type(r))

    import asyncio
    asyncio.run(main())
