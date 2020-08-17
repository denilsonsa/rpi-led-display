#!/usr/bin/env python3

import asyncio
from aiohttp import web


class WebApp:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.app = web.Application()
        self.app.add_routes([
            web.get('/hello', self.hello),
        ])
        self.runner = web.AppRunner(self.app)
        self.site = None

    async def run(self):
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, self.host, self.port)
        await self.site.start()

    async def close(self):
        await self.runner.cleanup()

    def hello(self, request):
        return web.Response(text="Hello!")


class RunAFewTimes:
    def __init__(self, times=5):
        self.times = times

    def run(self):
        #loop = asyncio.get_running_loop()
        loop = asyncio.get_event_loop()
        if self.times > 0:
            loop.call_later(2, self.run)
            self.times -= 1
        print('Running, {0} times remaining.'.format(self.times))
        if self.times == 0:
            loop.stop()
            print('stopping')

def main():
    print('main start')
    # This was added in Python 3.7
    #loop = asyncio.get_running_loop()
    loop = asyncio.get_event_loop()

    r = RunAFewTimes(30)
    s = RunAFewTimes(20)
    loop.call_soon(r.run)
    loop.call_soon(s.run)

    w = WebApp()
    loop.create_task(w.run())

    # TODO: Add signal handlers https://docs.python.org/3/library/asyncio-eventloop.html#set-signal-handlers-for-sigint-and-sigterm
    loop.run_forever()
    # TODO: also call shutdown_asyncgens(), or just required Python 3.7 anyway
    print('main end')

if __name__ == '__main__':
    main()
    # asyncio.run was added in Python 3.7
    #asyncio.run(main())
